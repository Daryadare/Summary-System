import torch
from transformers import GPT2Tokenizer, T5ForConditionalGeneration
import warnings
warnings.filterwarnings("ignore")


def make_summ(input_text: str, tokens_size: int):
    tokenizer = GPT2Tokenizer.from_pretrained('RussianNLP/FRED-T5-Summarizer',
                                              eos_token='</s>')
    model = T5ForConditionalGeneration.from_pretrained('RussianNLP/FRED-T5-Summarizer')

    input_ids = torch.tensor([tokenizer.encode(input_text)])
    outputs = model.generate(input_ids,
                             eos_token_id=tokenizer.eos_token_id,
                             num_beams=5,
                             min_new_tokens=17,
                             max_new_tokens=tokens_size,
                             do_sample=True,
                             no_repeat_ngram_size=4,
                             top_p=0.9)
    return tokenizer.decode(outputs[0][1:])
