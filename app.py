from io import BytesIO
from typing import Tuple
import wave
import gradio as gr
import numpy as np
from pydub.audio_segment import AudioSegment
import requests
from os.path import exists
from stt import Model
from datetime import datetime
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch

# download model
version = "v0.4"
storage_url = f"https://github.com/robinhad/voice-recognition-ua/releases/download/{version}"
model_name = "uk.tflite"
scorer_name = "kenlm.scorer"
model_link = f"{storage_url}/{model_name}"
scorer_link = f"{storage_url}/{scorer_name}"

model = Wav2Vec2ForCTC.from_pretrained("robinhad/wav2vec2-xls-r-300m-uk")#.to("cuda")
processor = Wav2Vec2Processor.from_pretrained("robinhad/wav2vec2-xls-r-300m-uk")
# TODO: download config.json, pytorch_model.bin, preprocessor_config.json, tokenizer_config.json, vocab.json, added_tokens.json, special_tokens.json

def download(url, file_name):
    if not exists(file_name):
        print(f"Downloading {file_name}")
        r = requests.get(url, allow_redirects=True)
        with open(file_name, 'wb') as file:
            file.write(r.content)
    else:
        print(f"Found {file_name}. Skipping download...")


def deepspeech(audio: np.array, use_scorer=False):
    ds = Model(model_name)
    if use_scorer:
        ds.enableExternalScorer("kenlm.scorer")

    result = ds.stt(audio)

    return result

def wav2vec2(audio: np.array):
    input_dict = processor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
    with torch.no_grad():
        output = model(input_dict.input_values.float())

    logits = output.logits

    pred_ids = torch.argmax(logits, dim=-1)[0]

    return processor.decode(pred_ids)

def inference(audio: Tuple[int, np.array]):
    print("=============================")
    print(f"Time: {datetime.utcnow()}.`")

    output_audio = _convert_audio(audio[1], audio[0])

    fin = wave.open(output_audio, 'rb')
    audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
    fin.close()

    transcripts = []

    transcripts.append(wav2vec2(audio))
    print(f"Wav2Vec2: `{transcripts[-1]}`")
    transcripts.append(deepspeech(audio, use_scorer=True))
    print(f"Deepspeech with LM: `{transcripts[-1]}`")
    transcripts.append(deepspeech(audio))
    print(f"Deepspeech: `{transcripts[-1]}`")
    return tuple(transcripts)
    

def _convert_audio(audio_data: np.array, sample_rate: int):
    audio_limit = sample_rate * 60 * 2 # limit audio to 2 minutes max
    if audio_data.shape[0] > audio_limit: 
        audio_data = audio_data[0:audio_limit]
    source_audio = BytesIO()
    source_audio.write(audio_data)
    source_audio.seek(0)
    output_audio = BytesIO()
    wav_file: AudioSegment = AudioSegment.from_raw(
        source_audio,
        channels=1,
        sample_width=4,
        frame_rate=sample_rate
    )
    wav_file.export(output_audio, "wav", codec="pcm_s16le", parameters=["-ar", "16k"])
    output_audio.seek(0)
    return output_audio

with open("README.md") as file:
    article = file.read()

iface = gr.Interface(
    fn=inference,
    inputs=[
        gr.inputs.Audio(type="numpy",
                        label="Аудіо", optional=False),
    ],
    outputs=[gr.outputs.Textbox(label="Wav2Vec2"), gr.outputs.Textbox(label="DeepSpeech with LM"), gr.outputs.Textbox(label="DeepSpeech")],
    title="🇺🇦 Ukrainian Speech-to-Text models",
    theme="huggingface",
    description="Україномовний🇺🇦 Speech-to-Text за допомогою Coqui STT",
    article=article,
)

download(model_link, model_name)
download(scorer_link, scorer_name)
iface.launch()
