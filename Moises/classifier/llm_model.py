from peft import PeftModel
from transformers import (AutoModelForSequenceClassification, AutoModelForCausalLM, T5ForSequenceClassification,
                          AutoTokenizer, T5ForConditionalGeneration, BertForSequenceClassification, BertForMaskedLM,
                          logging)
import torch

logging.set_verbosity_error()

models = {'Bert': 'google-bert/bert-base-uncased', 'Llama': 'meta-llama/Llama-2-7b-hf', 'T5': 'google/flan-t5-base'}


def model_init(name: str, original_model: str, ctype: str, datatype: str):
    device = device_check()

    # Select tokenizer for evaluation
    token = models[original_model]
    tokenizer = AutoTokenizer.from_pretrained(token)
    tokenizer.add_tokens(['[CLS]', '[MENTION]', '[LINK]', "[PAD]"])

    # Initialize model
    model = sequence_init(name, tokenizer, datatype) if ctype == 'Seq' else causal_init(name, tokenizer)
    model.resize_token_embeddings(len(tokenizer))
    model = PeftModel.from_pretrained(model, name)

    return name, tokenizer, model, device


# Sequence classification initialization
def sequence_init(name: str, tokenizer: AutoTokenizer, datatype: str):
    num_label = 2 if datatype.lower().__contains__("misinformation") else 3
    if name.__contains__('T5'):
        model = T5ForSequenceClassification.from_pretrained(models['T5'], num_labels=num_label, load_in_8bit=True)

    elif name.__contains__('Bert'):
        model = BertForSequenceClassification.from_pretrained(models['Bert'], num_labels=num_label, load_in_8bit=True)

    else:
        # pad token needed for Llama
        model = AutoModelForSequenceClassification.from_pretrained(models['Llama'], num_labels=num_label,
                                                                   load_in_8bit=True, pad_token_id=tokenizer.eos_token_id)
        tokenizer.add_special_tokens({'pad_token': "[PAD]"})
    return model


# Word generation initialization
def causal_init(name: str, tokenizer: AutoTokenizer):
    if name.__contains__('T5'):
        model = T5ForConditionalGeneration.from_pretrained(models['T5'], load_in_8bit=True)

    elif name.__contains__('Bert'):
        model = BertForMaskedLM.from_pretrained(models['Bert'], load_in_8bit=True)

    else:
        # pad token needed for LLaMa
        model = AutoModelForCausalLM.from_pretrained(models['Llama'], load_in_8bit=True,
                                                     pad_token_id=tokenizer.eos_token_id)
        tokenizer.add_special_tokens({'pad_token': "[PAD]"})
    return model


# Check if device has CUDA, else use MPS
def device_check():
    device_count = torch.cuda.device_count()
    check_cuda = torch.cuda.is_available()
    device = torch.device("cuda") if (device_count > 0 or check_cuda) else torch.device("mps")
    return device

