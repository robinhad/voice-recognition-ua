---
title: "Ukrainian Speech-to-Text"
emoji: 🐌
colorFrom: blue
colorTo: yellow
sdk: gradio
sdk_version: 3.41.2
app_file: app.py
pinned: false
---

# 🇺🇦🎤 Voice recognition for Ukrainian language
This is a repository with aim to apply various speech recognition models on Ukrainian language.  

You can see online demo here: https://huggingface.co/spaces/robinhad/ukrainian-stt.  
Github link: https://github.com/robinhad/voice-recognition-ua.  
Source code is in this repository together with auto-deploy pipeline scripts. 


# 🧮 Models
Model name  |  CER  |  WER  | License | Note
:-------------------------|:-------------------------|:-------------------------|:-------------------------|:-------------------------
[Wav2Vec2](https://github.com/robinhad/voice-recognition-ua/releases/tag/release%2Fwav2vec2-v0.1) | 6,01% | 27,99% | MIT | Common Voice 8 dataset, `test` set used as validation
[DeepSpeech with Wiki LM](https://github.com/robinhad/voice-recognition-ua/releases/tag/v0.4) | 12% | 30,65% | CC-BY-NC 4.0 | Common Voice 6 dataset
[DeepSpeech](https://github.com/robinhad/voice-recognition-ua/releases/tag/v0.4) | 16% | 57% | CC-BY-NC 4.0 | Common Voice 6 dataset


Checkout latest releases here: https://github.com/robinhad/voice-recognition-ua/releases/.

If you'd like to check out different models for Ukrainian language, please visit https://github.com/egorsmkv/speech-recognition-uk.

# 🤖 Training scripts
Guides for training are available in corresponding folders for each model.

# Support
If you like my work, please support here: https://send.monobank.ua/jar/48iHq4xAXm

# 🤝 Attribution
[@robinhad](https://github.com/robinhad) - model training.  
[@egorsmkv](https://github.com/egorsmkv) - organized [Ukrainian Speech recognition community](https://github.com/egorsmkv/speech-recognition-uk).  
[@tarasfrompir](https://github.com/tarasfrompir) - created synthetic 1200h Ukrainian Speech-to-Text dataset.  
[@AlexeyBoiler](https://github.com/AlexeyBoiler) - hosted Ukrainian Speech-to-Text dataset.  
