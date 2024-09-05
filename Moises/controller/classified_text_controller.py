from flask import jsonify
from Moises.model.classified import ClassifiedDAO
from Moises.classifier.classification import ModelPredict

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

    def getTextsById(self, text_id):
        dao = ClassifiedDAO()
        classified_text = dao.getTextById(text_id)
        if not classified_text:
            return jsonify(f"Text with id '{text_id}' was not found"), 404
        result = self.build_texts_dict(classified_text)
        health = llm_classification(result['context'])
        result['health'] = health

        # If text is not health related finish process
        if health != 'Related':
            result['misinformation'] = 'Undetermined'
            return result

        misinfo = llm_classification(result['context'])
        result['misinformation'] = misinfo



        return jsonify(result), 200

def llm_classification(text: str):
    return
#     return ModelPredict(mname=, classtype=, num=, datatype=).evaluate_models(text)
#
