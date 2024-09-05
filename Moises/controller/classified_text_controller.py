from flask import jsonify
from Moises.model.classified import ClassifiedDAO
from Moises.classifier.classification import ModelPredict

class ClassifiedController:

    @staticmethod
    def build_texts_dict(elements):
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
        dao = ClassifiedDAO()
        author_list = dao.getAllTexts()
        result = [self.build_texts_dict(row) for row in author_list]
        return jsonify(result), 200

    def getTextsById(self, text_id):
        dao = ClassifiedDAO()
        classified_text = dao.getTextById(text_id)
        if not classified_text:
            return jsonify(f"Text with id '{text_id}' was not found"), 404
        health = sequence_classification(classified_text[1])

        if health == 'Related':


        result = self.build_texts_dict(classified_text)
        return jsonify(result), 200


def sequence_classification(text: str):
    return ModelPredict(mname=, classtype=, num=, datatype=).sequence_classification()
