from Moises.chroma.read_from_chroma_script import get_data
from Moises.chroma.rag import evaluate_records
from Moises.model.chroma_records import ChromaDAO
from Moises.ollama.ollama_api import get_record

class ChromaController:

    """
    ===========================
                GET
    ===========================
    """

    def getChromaResult(self, data: str):
        eval_text = get_record(data)
        chroma_dict = get_data(eval_text)
        output = []
        for element in chroma_dict:
            refDao = ChromaDAO()
            reference = refDao.getChromaReferences(element['ids'])
            if reference is not None:
                output.append(reference[0])
        output.sort()
        text = [element['context'] for element in chroma_dict]
        chroma_value = evaluate_records(data, text)
        result = {'references': output, 'chroma_value': chroma_value}
        return result
