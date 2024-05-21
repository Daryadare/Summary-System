from transformers import GPT2LMHeadModel, GPT2Tokenizer


def load_tokenizer_and_model(model_name_or_path: str):
    """
    Функция для получения доступа к модели и токенайзеру.
    :param model_name_or_path: название и локальный путь к модели и токенайзеру
    :return: загруженные модель и токенайзер
    """
    return (GPT2Tokenizer.from_pretrained(model_name_or_path),
            GPT2LMHeadModel.from_pretrained(model_name_or_path))


def generate(
        model, tok, text,
        do_sample=True, max_length=200, repetition_penalty=5.0,
        top_k=5, top_p=0.95, temperature=1,
        num_beams=None,
        no_repeat_ngram_size=2
) -> list:
    """ Функция для настройки гиперпараметров модели и генерации ответа на вопрос пользователя """
    input_ids = tok.encode(text, return_tensors="pt")
    out = model.generate(
        input_ids,
        max_length=max_length,
        repetition_penalty=repetition_penalty,
        do_sample=do_sample,
        top_k=top_k, top_p=top_p, temperature=temperature,
        num_beams=num_beams, no_repeat_ngram_size=no_repeat_ngram_size
    )
    return list(map(tok.decode, out))


def answer(prompt: str) -> str:
    """
    Функция для загрузки модели и токенайзера и генерации ответа на вопрос пользователя.
    :param prompt: вопрос пользователя
    :return: сгенерирвоанный моделью ответ
    """
    tok, model = load_tokenizer_and_model("sberbank-ai/rugpt3large_based_on_gpt2")
    generated = generate(model, tok, prompt, num_beams=5)
    return generated[0]
