import torch
from tools import suppress_output
from transformers import GPT2Tokenizer, T5ForConditionalGeneration
from transformers import logging
logging.set_verbosity_error()


def make_summ(input_text: str, tokens_size: int) -> str:
    """
    Функция для получения суммаризации текста.
    :param input_text: очищенный результат работы модели Whisper-large-v3
    :param tokens_size: размер суммаризации
    :return: результат работы модели FRED-T5-Summarizer - суммаризация входного текста
    """
    with suppress_output.SuppressOutput():
        """ Полуение доступа к токенайзеру """
        tokenizer = GPT2Tokenizer.from_pretrained('RussianNLP/FRED-T5-Summarizer',
                                                  eos_token='</s>')
        """ Полуение доступа к модели """
        model = T5ForConditionalGeneration.from_pretrained('RussianNLP/FRED-T5-Summarizer')

        """ Указание задачи модели и текст для суммаризации """
        prompt = '<LM> Выдели главную информацию из текста:\n' + input_text
        input_ids = torch.tensor([tokenizer.encode(prompt)])
        outputs = model.generate(input_ids,
                                 eos_token_id=tokenizer.eos_token_id,
                                 num_beams=5,
                                 min_new_tokens=17,
                                 max_new_tokens=tokens_size,
                                 do_sample=True,
                                 no_repeat_ngram_size=4,
                                 top_p=0.9)

    return tokenizer.decode(outputs[0][1:])
