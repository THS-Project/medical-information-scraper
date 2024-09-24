from Moises.chroma.read_from_chroma_script import get_data
# from Moises.chroma.rag import evaluate_records
from Moises.model.chroma_records import ChromaDAO
from Moises.ollama.ollama_api import evaluate_records

class ChromaController:

    """
    ===========================
                GET
    ===========================
    """

    def getChromaResult(self, data: str):
        # Get query for chroma
        chroma_query = evaluate_records(data)
        # Get data from chroma
        chroma_dict = get_data(chroma_query)
        output = []
        # Find references based on chunks id
        for element in chroma_dict:
            refDao = ChromaDAO()
            reference = refDao.getChromaReferences(element['ids'])
            if reference is None:
                continue

            if reference[0] not in output:
                output.append(reference[0])

        output.sort()
        text = [element['context'] for element in chroma_dict]

        # Using chroma data and original text, rebut misinformation
        chroma_value = evaluate_records(data, text)
        result = {'references': output, 'chroma_value': chroma_value}
        return result
