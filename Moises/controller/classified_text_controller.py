import os

from flask import jsonify
from Moises.model.classified import ClassifiedDAO
from Moises.classifier.classification import ModelPredict
from Moises.controller.chroma_controller import ChromaController


class ClassifiedController:

    @staticmethod
    def build_texts_dict(elements) -> dict:
        result = {'text_id': elements[0],
                  't_context': elements[1]
                  }
        return result

    """
    ===========================
                GET
    ===========================
    """

    def getAllTexts(self):
        # Get all health related texts
        health = os.getenv('HEALTH_ID')
        dao = ClassifiedDAO()
        health_texts = dao.getAllTexts(health, 1)
        result = [self.build_texts_dict(row) for row in health_texts]

        # Get all misinformation texts
        misinfo = os.getenv('MISINFO_ID')
        dao = ClassifiedDAO()
        misinformation_texts = dao.getAllTexts(misinfo, 2)
        temp_list = [self.build_texts_dict(row) for row in misinformation_texts]

        result.extend(temp_list)
        return jsonify(result), 200

    def getTextClassificationById(self, text_id: int):
        dao = ClassifiedDAO()
        classified_text = dao.getTextById(text_id)
        # Validate that text exists
        if not classified_text:
            return jsonify(f"Text with id '{text_id}' was not found"), 404

        result = self.build_texts_dict(classified_text)
        health_model, misinformation_model = self.get_model_paths()

        # Find health classification
        health = llm_classification(result['t_context'], health_model)
        result['health'] = health

        # If text is not health related finish process
        if health != 'Related':
            result['misinformation'] = 'Undetermined'
        else:
            # Find misinformation classification and reference in chroma
            misinfo = llm_classification(result['t_context'], misinformation_model)
            result['misinformation'] = misinfo
            if misinfo == 'Misinformation':
                # Receive rebuttal from Chroma and LLM
                rebuttal = ChromaController().getChromaResult(result['t_context'])
                result.update(rebuttal)
            else:
                result.update({"chroma_value": "No misinformation on the text"})

        return jsonify(result), 200

    def get_model_paths(self):
        # Get all health related texts
        health = os.getenv('HEALTH_ID')
        dao = ClassifiedDAO()
        health_model_path = dao.getModelPath(health)

        # Get all misinformation texts
        misinfo = os.getenv('MISINFO_ID')
        dao = ClassifiedDAO()
        misinformation_model_path = dao.getModelPath(misinfo)

        return health_model_path, misinformation_model_path


def llm_classification(text: str, model_path: str):
    return ModelPredict(model_path).evaluate_models(text)

