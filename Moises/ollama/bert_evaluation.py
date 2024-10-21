import time

from dotenv import load_dotenv
import csv
import requests
import ast
from evaluate import load


def bert_score(predictions: list[str], references: list[str]):
    bertscore = load("bertscore")
    results = bertscore.compute(predictions=predictions, references=references, lang="en")
    print(results)
    return results


def data_retrieval():
    temp = []
    total = {'Elements': 0, 'precision': 0, 'recall': 0, 'f1': 0}
    req_text = requests.get('http://127.0.0.1:5000/classified/page?page=1&amt=200')
    texts = ast.literal_eval(req_text.text)
    for i in texts:
        try:
            time.sleep(0.5)
            req_classification = requests.get(f'http://127.0.0.1:5000/classified/{i["text_id"]}')
            classification = ast.literal_eval(req_classification.text)
            if classification['health'] == 'Related' and classification['misinformation'] == 'Misinformation':

                # Calculate score
                bert_output = bert_score([classification['chroma_value']], [classification['t_context']])
                precision = bert_output['precision'][0]
                recall = bert_output['recall'][0]
                f1 = bert_output['f1'][0]

                # Add to list
                temp.append({'original': classification['t_context'], 'rebuttal': classification['chroma_value'],
                             'precision': precision, 'recall': recall, 'f1': f1})
                total['Elements'] += 1
                total['precision'] += precision
                total['recall'] += recall
                total['f1'] += f1

        except Exception as E:
            pass

    temp.append(total)
    save_results(temp)

def save_results(results: list[dict]):
    with open("LlaMa3_BERTScore_test.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Original Text', 'Rebuttal', 'Precision', 'Recall', 'F1'])
        total = results.pop(-1)
        for element in results:
            writer.writerow([element['original'], element['rebuttal'], element['precision'], element['recall'],
                             element['f1']])
        writer.writerow(['Total', total['Elements'], total['precision']/total['Elements'], total['recall']/total['Elements'],
                         total['f1']/total['Elements']])


if __name__ == "__main__":
    load_dotenv()
    data_retrieval()
    # bert_score(["""what if experts could predict when and where the #flu will spread, like an oncoming
    # storm? @columbia scientists have done just that https://t.co/chvfqairns"""],
    #            ["""This text is misleading because it implies that experts can accurately predict the timing
    #            and location of flu outbreaks with a high degree of specificity, similar to predicting a weather storm.
    #            However, according to the medical information provided, while there are some studies on forecasting
    #            influenza activity, the field is still in its infancy and the accuracy of these forecasts varies
    #            greatly depending on factors such as data quality and the approach used (e.g., see Table 2 and Fig. 1).
    #            Additionally, most forecasting has been done at an individual location level, but research suggests that
    #            human travel between locations can significantly improve forecast accuracy (as mentioned in the medical
    #            information). Therefore, it's not clear if predicting flu outbreaks like a weather storm is currently
    #            possible or reliable."""])
    #
