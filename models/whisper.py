import re
import torch
from tools import suppress_output
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from transformers import logging
logging.set_verbosity_error()


def load_model_processor():

    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-large-v3"
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )

    processor = AutoProcessor.from_pretrained(model_id)

    return model, processor, torch_dtype


def remove_stop_words(text: str):
    stop_words = [
        "как бы", "кстати", "ну", "короче",
        "вот", "вообще", "как-то", "так сказать",
        "собственно", "таки", "еще", "вроде"
    ]
    stop_words_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(word)
                                                        for word in stop_words) +
                                    r')\b',
                                    re.IGNORECASE)

    cleaned_text = stop_words_pattern.sub('', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text


def clean_whisper_output(res_w: str) -> tuple[str, str]:
    clean_text = res_w[:res_w.find('chunks')]
    pattern = r"'text': '([^']+)'"
    matches = re.findall(pattern, clean_text)
    text_sum = ' '.join(matches)

    chunks_text = res_w[res_w.find('chunks'):res_w.rfind('}]}')]
    res_w_ts = ''
    pattern = r"'timestamp': \((\d+\.\d+), (\d+\.\d+)\), 'text': '([^']+)'"
    matches = re.findall(pattern, chunks_text)
    cleaned_strings = [f"({start}, {end}) {text}" for start, end, text in matches]
    for string in cleaned_strings:
        res_w_ts += string

    cleaned_text_sum = remove_stop_words(text_sum)
    cleaned_res_w_ts = remove_stop_words(res_w_ts)

    return cleaned_res_w_ts, cleaned_text_sum


def transcribe(filepath: str):

    with suppress_output.SuppressOutput():
        model, processor, torch_dtype = load_model_processor()

        pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=64,
            chunk_length_s=64,
            batch_size=32,
            return_timestamps=True,
            torch_dtype=torch_dtype,
        )

        result = pipe(filepath,
                      generate_kwargs={"language": "russian"},
                      return_timestamps=True)
    return result
