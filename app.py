from io import BytesIO
from typing import Tuple
import wave
import gradio as gr
import numpy as np
from pydub.audio_segment import AudioSegment
import requests
from os.path import exists
from stt import Model


MODEL_NAMES = [
    #    "With scorer",
    "No scorer"
]

# download model
version = "v0.5"
storage_url = f"https://github.com/robinhad/voice-recognition-ua/releases/download/{version}"
model_name = "uk.tflite"
scorer_name = "kenlm.scorer"
model_link = f"{storage_url}/{model_name}"
scorer_link = f"{storage_url}/{scorer_name}"


def client(audio_data: np.array, sample_rate: int, use_scorer=False):
    output_audio = _convert_audio(audio_data, sample_rate)

    fin = wave.open(output_audio, 'rb')
    audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    fin.close()

    ds = Model(model_name)
    if use_scorer:
        ds.enableExternalScorer("kenlm.scorer")

    result = ds.stt(audio)

    return result


def download(url, file_name):
    if not exists(file_name):
        print(f"Downloading {file_name}")
        r = requests.get(url, allow_redirects=True)
        with open(file_name, 'wb') as file:
            file.write(r.content)
    else:
        print(f"Found {file_name}. Skipping download...")


def stt(audio: Tuple[int, np.array], model_name: str):
    sample_rate, audio = audio
    use_scorer = True if model_name == "With scorer" else False

    if sample_rate != 16000:
        raise ValueError("Incorrect sample rate.")

    recognized_result = client(audio, sample_rate, use_scorer)

    return recognized_result


def _convert_audio(audio_data: np.array, sample_rate: int):
    source_audio = BytesIO()
    source_audio.write(audio_data)
    source_audio.seek(0)
    output_audio = BytesIO()
    wav_file = AudioSegment.from_raw(
        source_audio,
        channels=1,
        sample_width=2,
        frame_rate=sample_rate
    )
    wav_file.set_frame_rate(16000).set_channels(
        1).export(output_audio, "wav", codec="pcm_s16le")
    output_audio.seek(0)
    return output_audio


iface = gr.Interface(
    fn=stt,
    inputs=[
        gr.inputs.Audio(type="numpy",
                        label=None, optional=False),
        gr.inputs.Radio(
            label="Виберіть Speech-to-Text модель",
            choices=MODEL_NAMES,
        ),

    ],
    outputs=gr.outputs.Textbox(label="Output"),
    title="🐸🇺🇦 - Coqui STT",
    theme="huggingface",
    description="Україномовний🇺🇦 Speech-to-Text за допомогою Coqui STT",
    article="Якщо вам подобається, підтримайте за посиланням: [SUPPORT LINK](https://send.monobank.ua/jar/48iHq4xAXm)",
)

download(model_link, model_name)
#download(scorer_link, scorer_name)
iface.launch()
