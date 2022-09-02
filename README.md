---
title: "Ukrainian Speech-to-Text"
emoji: 🐌
colorFrom: blue
colorTo: yellow
sdk: gradio
app_file: app.py
pinned: false
---

# 🇺🇦🎤 Voice recognition for Ukrainian language
This is a repository with aim to apply various speech recognition models on Ukrainian language.  

You can see online demo here: https://huggingface.co/spaces/robinhad/ukrainian-stt.  
Source code is in this repository together with auto-deploy pipeline scripts. 


# 🧮 Models
Model name  |  CER  |  WER  | License | Note
:-------------------------|:-------------------------|:-------------------------|:-------------------------|:-------------------------
[DeepSpeech with Wiki LM](https://github.com/robinhad/voice-recognition-ua/releases/tag/v0.4) | 12% | 30,65% | CC-BY-NC 4.0 | Common Voice 6 dataset
[DeepSpeech](https://github.com/robinhad/voice-recognition-ua/releases/tag/v0.4) | 16% | 57% | CC-BY-NC 4.0 | Common Voice 6 dataset


Checkout latest releases here: https://github.com/robinhad/voice-recognition-ua/releases/.

If you'd like to check out different models for Ukrainian language, please visit https://github.com/egorsmkv/speech-recognition-uk.

# 🤖 Training scripts
Guides for training are available in corresponding folders for each model.

# 🤝 Attribution
[@robinhad](https://github.com/robinhad) - model training. 
[@egorsmkv](https://github.com/egorsmkv) - organized [Ukrainian Speech recognition community](https://github.com/egorsmkv/speech-recognition-uk).  
[@tarasfrompir](https://github.com/tarasfrompir) - created synthetic 1200h Ukrainian Speech-to-Text dataset.  
[@AlexeyBoiler](https://github.com/AlexeyBoiler) - hosted Ukrainian Speech-to-Text dataset.  
