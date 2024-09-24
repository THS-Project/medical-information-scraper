import json
import requests


def evaluate_records(text: str, context: list[str] = None) -> str:
    # Define the prompt template
    if context:
        prompt = f"""You are a epidemiology expert evaluating texts that has been classified as misinformation.
        Your goal is to explain why the text (Misinformation Text) is factually inaccurate or misleading,
        using simple, non-technical language. If the provided Medical Information is insufficient, indicate that
        more context is needed to fully evaluate the text.

        Your response should be at a maximum of 4 sentences long, written in clear, human-like language. Include
        relevant data from the provided medical information to offer support, to help the reader understand why
        is misinformation. If necessary, mention numbers, statistics, or percentages to give more credibility
        to your explanation.

        Medical Information: {context}
        
        Misinformation text: {text}
        """

    else:
        prompt = f"""
        You are a medical expert evaluating misinformation in social media texts. Your task is to analyze
        the provided text to identify its topic and important keywords that are related to health. 
        Your output should be a single coherent sentence that summarizes the health topic and helps find 
        best result in a vector database that contains medical research papers. 

        Return only the vector database's query as a sentence, with no additional text. Your answer
        should be written as if it is a human writing a query.

        text: {text}
        """

    headers = {
        'Content-Type': 'application/json'
    }
    data = {'model': 'llama3.1',
            'prompt': prompt,
            'stream': False
            }
    result = requests.post('http://localhost:11434/api/generate', headers=headers, data=json.dumps(data))
    data = json.loads(result.text)
    actual = data['response']
    print(actual)
    return actual


if __name__ == "__main__":
    sentence = """#nih fauci, @cdcdirector @sgottliebfda &amp; @barda bright expected to be grilled tomorrow over
    ineffective #flu vaccine at @housecommerce #suboversight  bets on fauci saying universal #influenza vax in 5,
    maybe 10 years? my preview here: https://t.co/fsqefwhik7  #cdc #fda #vaccines"""

    evaluate_records(sentence)

