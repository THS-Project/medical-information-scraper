from flask import jsonify
from Moises.chroma.read_from_chroma_script import get_data
from Moises.model.reference import ReferenceDAO
# from Moises.model.chunk
from Moises.model.chroma_records import ChromaDAO


class ChromaController:

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

    def getChromaResult(self, data: dict):
        chroma_dict = get_data(data['text'])
        output = []
        for element in chroma_dict:
            refDao = ChromaDAO()
            reference = refDao.getChromaReferences(element['ids'])
            output.extend(reference)
            break

        result = {'references': output, 'chroma_value': chroma_dict}
        print(result)
        return jsonify(result), 200

    def getTextsById(self, text_id):
        dao = ClassifiedDAO()
        classified_text = dao.getTextById(text_id)
        if not classified_text:
            return jsonify(f"Text with id '{text_id}' was not found"), 404
        author = self.build_texts_dict(classified_text)
        return jsonify(author), 200
