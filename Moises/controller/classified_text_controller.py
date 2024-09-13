from flask import jsonify
from Moises.model.classified import ClassifiedDAO
from Moises.classifier.classification import ModelPredict
from Moises.controller.chroma_controller import ChromaController


class ClassifiedController:

    @staticmethod
    def build_texts_dict(elements) -> dict:
        result = {'text_id': elements[0],
                  'context': elements[1],
                  'seed': elements[2]
                  }
        return result

    # @staticmethod
    # def build_texts_dict(elements):
    #     result = {'text_id': elements[0],
    #               't_context': elements[1],
    #               'health': elements[2],
    #               'misinformation': elements[3]
    #               }
    #     return result

    """
    ===========================
                GET
    ===========================
    """

    def getAllTexts(self):
        dao = ClassifiedDAO()
        author_list = dao.getAllTexts()
        result = [self.build_texts_dict(row) for row in author_list]
        return jsonify(result), 200

    def getTextClassificationById(self, text_id: int):
        dao = ClassifiedDAO()
        classified_text = dao.getTextById(text_id)
        # Validate that text exists
        if not classified_text:
            return jsonify(f"Text with id '{text_id}' was not found"), 404

        result = self.build_texts_dict(classified_text)
        print(result)

        # Find health classification
        health = llm_classification(result['context'])
        result['health'] = health

        # If text is not health related finish process
        if health != 'Related':
            result['misinformation'] = 'Undetermined'
        else:
            # Find misinformation classification and reference in chroma
            misinfo = llm_classification(result['context'], datatype='misinformation')
            result['misinformation'] = misinfo
            if misinfo == 'Misinformation':
                # Receive rebuttal from Chroma and LLM
                rebuttal = ChromaController().getChromaResult(result['context'])
                result.update(rebuttal)
            else:
                result.update({"chroma_value": "No misinformation on the text"})

        return jsonify(result), 200


def llm_classification(text: str, datatype: str = 'health'):
    num = 20 if datatype == 'health' else 25
    return ModelPredict(mname='Bert', classtype='Seq', num=num, datatype=datatype).evaluate_models(text)
