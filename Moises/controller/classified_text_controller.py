from flask import jsonify
from Moises.model.classified import ClassifiedDAO


class ClassifiedController:

    @staticmethod
    def build_texts_dict(elements):
        result = {'text_id': elements[0],
                  't_context': elements[1],
                  'health': elements[2],
                  'misinformation': elements[3]
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
        author = [self.build_texts_dict(row) for row in author_list]
        return jsonify(author), 200

    def getTextCount(self):
        dao = ClassifiedDAO()
        total_count = dao.getTextCount()
        return jsonify({'total': total_count}), 200

    def getTextsById(self, text_id):
        dao = ClassifiedDAO()
        classified_text = dao.getTextById(text_id)
        if not classified_text:
            return jsonify(f"Text with id '{text_id}' was not found"), 404
        author = self.build_texts_dict(classified_text)
        return jsonify(author), 200

    def getTextsByPage(self, data):
        page = data['page']
        amt = data['amt']
        dao = ClassifiedDAO()
        author_list = dao.getTextsByPage(page,amt)
        author = [self.build_texts_dict(row) for row in author_list]
        return jsonify(author), 200
