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

    # sentence = """@freebeecee @veritasever @3worldmom @geoffschuler @erikwilson1975 @1002loola @itsmepanda1 @rustypee4
    # @knakatani @joejoe80495073 @emmagpaley @carlsmythe @grumfromnorwich @bigbalddr @katieicunurse @chrisvcsefalvay
    # @janem1276 @joneselenore21 @wandaspangler2 @awithonelison @angryamygdala @stayyoungaft50 @justice69hall @plasticdoe
    # @boglethemind @mj1117d @1mayo10 @emotrano @dkegel @noahsmittysbro @thefrankmanmn @chrisjohnsonmd @gretchenscience
    # @pileofgoop @_cwn @kenjaques @svagdis @docmeehan @and_kell @just4thecause @mmelgar09 @jkellyca @eldrave20 @siubhan_h
    # @lalaruefrench75 @ithinkaboutbeer @doritmi @rbuzzy1111 @rachlittlewood @lilearthling369 yeah! you guys are
    # forgetting that not everyone who had measles died! some people just got very, very, very sick!! pfft... vaccines.
    # you guys are such corporate shills!! probably work for pfizer and monsanto!
    # """

    # prompt = "ebola is a fake virus, it does not kill people"

    get_record(sentence)

