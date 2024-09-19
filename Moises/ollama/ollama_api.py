import json
import requests


def get_record(text: str):
    prompt = f"""
            You are a medical expert evaluating misinformation in social media texts. Your task is to analyze
            the provided text to identify its topic and important keywords that are related to health. 
            Your output should be a single coherent sentence that summarizes the health topic and helps find the best
            result in a vector database that contains medical research papers. 

            Return only the vector database's query as a sentence, with no additional text. Your answer should be written
            as if it is a human writing a query.

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

    get_record(sentence)

