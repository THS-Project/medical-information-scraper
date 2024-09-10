import numpy
import torch

from Moises.classifier.llm_model import model_init


class ModelPredict:
    def __init__(self, mname: str, classtype: str, num: int, datatype: str):
        model_name = get_pathname(mname, classtype, num)
        self.datatype = datatype
        self.classtype = classtype
        self.mname, self.tokenizer, self.model, self.device = model_init(model_name, original_model=mname, ctype=classtype,
                                                                         datatype=datatype)
        # self.mname, self.tokenizer, self.model, self.device = '', '', '', ''


    def inference(self, text: str, max_input_tokens=500, max_output_tokens=100) -> str:
        # Tokenize
        input_ids = self.tokenizer.encode(text, return_tensors="pt", truncation=True, max_length=max_input_tokens)

        # Generate
        generated_tokens_with_prompt = self.model.generate(input_ids=input_ids.to(self.device),
                                                      max_length=max_output_tokens,
                                                      num_return_sequences=1,  # Generate only one sequence
                                                      do_sample=False,  # Disable sampling to get deterministic output
                                                      output_scores=False,  # Disable outputting scores
                                                      )

        # Decode
        generated_text_with_prompt = self.tokenizer.batch_decode(generated_tokens_with_prompt, skip_special_tokens=True)

        return generated_text_with_prompt[0].strip()

    def sequence_classification(self, text: str) -> str:
        id2label = {0: 'Not Misinformation', 1: 'Misinformation'} if self.datatype == "misinfo" else {0: 'Unrelated',
                                                                                                     1: 'Related',
                                                                                                     2: 'Ambiguous'}
        # Tokenize
        encoding = self.tokenizer(text, return_tensors="pt")

        encoding = {k: v.to(self.device) for k, v in encoding.items()}
        if 'token_type_ids' in encoding and self.mname == "Llama":
            del encoding['token_type_ids']

        outputs = self.model(**encoding)

        logits = outputs.logits.to(torch.float) if self.mname == 'Bert' else  outputs.logits.detach().cpu().to(torch.float)
        # apply softmax
        softmax = torch.nn.Softmax()
        probs = softmax(logits.squeeze().cpu())
        idx = numpy.argmax(probs.detach().numpy())
        predicted_labels = id2label[idx]

        return predicted_labels


    def evaluate_models(self, text: str) -> str:
        return self.sequence_classification(text) if self.classtype == 'Seq' else (self.inference(text))


def get_pathname(mname: str, classtype: str, num: int) -> str:
    model_name = f'models/{mname}_{classtype}_LoRA_{str(num)}_epochs'
    return model_name


if __name__ == "__main__":
    text = 'This tweet is misinfo'
    mname = 'Bert'
    ctype = 'Seq'
    num = 10
    datatype = 'misinfo'
    ModelPredict(mname, ctype, num, datatype).evaluate_models(text)

