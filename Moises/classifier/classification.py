import numpy
import torch

from Moises.classifier.llm_model import model_init


class ModelPredict:
    def __init__(self, model_path: str):
        model_data = model_path.split('/')[-1]
        mname, classtype, datatype, num = model_data.split('_')[:-1]
        self.datatype = datatype
        self.classtype = classtype
        self.mname, self.tokenizer, self.model, self.device = model_init(model_path, original_model=mname,
                                                                         ctype=classtype, datatype=datatype)

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
        id2label = {0: 'Not Misinformation', 1: 'Misinformation'} if self.datatype == "misinformation" else {
                                                                                                     0: 'Unrelated',
                                                                                                     1: 'Related',
                                                                                                     2: 'Ambiguous'}
        # Tokenize
        encoding = self.tokenizer(text, return_tensors="pt")

        encoding = {k: v.to(self.device) for k, v in encoding.items()}
        if 'token_type_ids' in encoding and self.mname == "Llama":
            del encoding['token_type_ids']

        outputs = self.model(**encoding)

        logits = outputs.logits.to(torch.float) if self.mname == 'Bert' else outputs.logits.detach().cpu().to(torch.float)
        # apply softmax
        softmax = torch.nn.Softmax(dim=-1)
        probs = softmax(logits.squeeze().cpu())
        print(text, probs)
        idx = numpy.argmax(probs.detach().numpy())
        predicted_labels = id2label[idx]

        return predicted_labels

    def evaluate_models(self, text: str) -> str:
        prompt = f"""Is the text separated by triple ticks health misinformation or not.
                ---{text}---""" if self.datatype == 'misinformation' else \
                f'''Is the text separated by triple ticks related, unrelated, or ambiguous to health?
                Your answer must be a single word: related, unrelated, or ambiguous.
                ---{text}---'''

        return self.sequence_classification(prompt) if self.classtype == 'Seq' else (self.inference(prompt))


def get_pathname(mname: str, classtype: str, num: int) -> str:
    model_name = f'Moises/classifier/models/{mname}_{classtype}_LoRA_{str(num)}_epochs'
    return model_name


if __name__ == "__main__":
    text = 'This tweet is misinfo'
    mname = 'Bert'
    ctype = 'Seq'
    num = 10
    datatype = 'misinfo'
    ModelPredict(mname, ctype, num, datatype).evaluate_models(text)

