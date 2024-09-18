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
        eval_text = evaluate_records(data, summary=True)
        chroma_dict = get_data(eval_text)
        output = {}
        for element in chroma_dict:
            refDao = ChromaDAO()
            reference = refDao.getChromaReferences(element['ids'])
            if reference is not None:
                output[reference[0]] = reference[1]
        text = [element['context'] for element in chroma_dict]
        chroma_value = evaluate_records(data, text)
        result = {'references': list(output.values()).sort(), 'chroma_value': chroma_value}
        return result
