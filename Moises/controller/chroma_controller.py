from flask import jsonify
from Moises.chroma.read_from_chroma_script import get_data
from Moises.chroma.rag import evaluate_records
from Moises.model.chroma_records import ChromaDAO


class ChromaController:

    @staticmethod
    def build_texts_dict(elements: tuple):
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

    def getChromaResult(self, data: str):
        chroma_dict = get_data(data)
        output = []
        for element in chroma_dict:
            refDao = ChromaDAO()
            reference = refDao.getChromaReferences(element['ids'])
            output.extend(reference)

        text = [element['context'] for element in chroma_dict]
        chroma_value = evaluate_records(text, data)
        result = {'references': output, 'chroma_value': chroma_value}
        return result
