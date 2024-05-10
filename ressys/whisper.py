import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import warnings
warnings.filterwarnings("ignore")


def load_model_processor():

    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-large-v3"
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )

    processor = AutoProcessor.from_pretrained(model_id)

    return model, processor, torch_dtype


def transcribe(filepath: str):

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
        # device=device,
    )

    result = pipe(filepath,
                  generate_kwargs={"language": "russian"},
                  return_timestamps=True)
    return result
