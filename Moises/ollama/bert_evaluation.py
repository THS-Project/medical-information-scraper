from Moises.controller.classified_text_controller import ClassifiedController
import csv
from evaluate import load



def bert_score(predictions: str, references: str):
    bertscore = load("bertscore")
    results = bertscore.compute(predictions=predictions, references=references, lang="en")
    print(results)
    return results


def data_retrieval():
    temp = []
    for i in range(1000):
        classification = ClassifiedController().getTextClassificationById(i)
        if classification['health'] == 'Related' and classification['misinformation'] == 'Misinformation':
            bert_output = bert_score(classification['chroma_value'], classification['t_context'])
            temp.append({'original': classification['t_context'], 'rebuttal': classification['chroma_value'],
                         'precision': bert_output['precision'], 'recall': bert_output['recall'], 'f1': bert_output['f1']})
            # temp.append(bert_score(classification['chroma_value'], classification['t_context']))


def save_results(results: list[dict]):
    with open("BERTScore_test.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Original Text', 'Rebuttal', 'Precision', 'Recall', 'F1'])
        for element in results:
            writer.writerow([element['original'], element['rebuttal'], element['precision'], element['recall'],
                             element['f1']])

if __name__ == "__main__":
    # data_retrieval()
    bert_score("This is a text", "Not a text")

