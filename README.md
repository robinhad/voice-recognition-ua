---
title: "Ukrainian Speech-to-Text"
emoji: 🐸
colorFrom: blue
colorTo: yellow
sdk: gradio
app_file: app.py
pinned: false
---

# voice-recognition-ua
This is a repository with aim to apply [Coqui STT](https://github.com/coqui-ai/STT "STT")(formerly [DeepSpeech](https://github.com/mozilla/DeepSpeech)) (state-of-the-art speech recognition model) on Ukrainian language.  
You can see online demo here: https://voice-recognition-ua.herokuapp.com (your voice is not stored).  
Source code is in this repository together with auto-deploy pipeline scripts.  
P.S. Due to small size of dataset (50 hours), don't expect production-grade performance.  
Contribute your voice to [Common Voice project](https://commonvoice.mozilla.org/uk "Common Voice") yourself, so we can improve model accuracy.  

This model is licensed under [Creative Commons Attribution-NonCommercial 4.0 International License](./LICENSE).

Checkout latest releases here: https://github.com/robinhad/voice-recognition-ua/releases/.

If you'd like to check out different models for Ukrainian language, please visit https://github.com/egorsmkv/speech-recognition-uk.

## Pre-run requirements
Make sure to download:
1. https://github.com/robinhad/voice-recognition-ua/releases/download/v0.4/uk.tflite
2. https://github.com/robinhad/voice-recognition-ua/releases/download/v0.4/kenlm.scorer

## How to launch 
```
export FLASK_APP=main.py
export TOKEN=<Telegram bot API key>
flask run
```

# How to train your own model

Guides for importing data are available in [/scripts](/scripts) folder.

Most of the guide is took from there:
https://deepspeech.readthedocs.io/en/v0.9.3/TRAINING.html

Disclaimer: if you would like to continue working on the model, use https://github.com/coqui-ai/STT (this is former DeepSpeech team, where development continues).


## Steps:

<details>
 <summary>This guide could be outdated, please be aware.</summary>
1. Create g4dn.xlarge instance on AWS, Deep Learning AMI (Ubuntu 18.04), 150 GB of space.

2. Install Python requirements:  
```
sudo apt-get install python3-dev sox libsox-fmt-mp3 # sox is used for audio reading
```
 
3. Clone DeepSpeech branch v0.9.1  
```
git clone --branch v0.9.1 https://github.com/mozilla/DeepSpeech
```
4. Go into DeepSpeech directory:  
```
cd DeepSpeech
```
5. Create virtual environment using conda (it will be easier to manage CUDA libraries):  
```
conda create --prefix $HOME/tmp/deepspeech-train-venv/ python=3.7
```
6. Activate it:  
```
conda activate /home/ubuntu/tmp/deepspeech-train-venv 
```
7. Install DeepSpeech requirements:  
```
pip3 install --upgrade pip==20.2.2 wheel==0.34.2 setuptools==49.6.0
pip3 install --upgrade -e .
```
8. Install required CUDA libraries:  
```
conda install cudnn=7.6=cuda10.1_0
pip3 install 'tensorflow-gpu==1.15.4'
```
9. Open https://commonvoice.mozilla.org/uk/datasets and copy link to Ukrainian dataset.  
```
cd ..
wget <your_link_to_dataset>
tar -xf uk.tar.gz
``` 
You'll get a folder named `cv-corpus-5.1-2020-06-22`
10. Download alphabet, used for dataset.
Alphabet is a file with all possible symbols, that are going to be in a dataset. Outputs are directly formed from alphabet. Alphabet is also used for filtering, data, that contain symbols not in alphabet, will be skipped.  
```
cd ./DeepSpeech
mkdir data_uk
cd ./data_uk
wget https://github.com/robinhad/voice-recognition-ua/releases/download/v0.2/alphabet.txt
``` 
NOTE: if you create your alphabet, make sure it's in UTF-8 format

11. Filter data, that contains symbols not in alphabet:  
```
cd .. # DeepSpeech
bin/import_cv2.py --filter_alphabet ./data_uk/alphabet.txt ../cv-corpus-5.1-2020-06-22/uk
```
12. (Optional step if you want to create model from scratch, expect low performance because of small dataset (~20 hours for Ukrainian))
```
python3 DeepSpeech.py --train_files ../data/CV/en/clips/train.csv --dev_files ../data/CV/en/clips/dev.csv --test_files ../data/CV/en/clips/test.csv
```
13. Transfer Learning  
Transfer learning is method of using existing, pre-trained model on one dataset and apply it on similar, but another. In example, if we do speech recognition, we can use a fact that with each layer model deals with more general concept. Starting layers recognize different sound and low-level patterns, whereas later layers are more involved in final output (letters). So in that case we freeze all the layers (they don't update during training) except the specified last ones, where we substitute English alphabet with Ukrainian one.  
Below we will download English model checkpoint and create folder for Ukrainian one.
```
mkdir checkpoints
cd ./checkpoints
wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.1/deepspeech-0.9.1-checkpoint.tar.gz
tar -xf deepspeech-0.9.1-checkpoint.tar.gz
mkdir uk_transfer_checkpoint
cd ..
```
14. Start a training itself. (if you want to make changes to training parameters, run `python3 DeepSpeech.py --helpfull` for list of all parameters).  
When model finishes training, there will be error due to bug in DeepSpeech that will prevent evaluating performance for now, we will fix it in the next step.
It will take a while, ~11 minutes per epoch.
```
python3 DeepSpeech.py \
    --train_cudnn \
    --drop_source_layers 2 \
    --alphabet_config_path ./data_uk/alphabet.txt \
    --save_checkpoint_dir ./checkpoints/uk_transfer_checkpoint \
    --load_checkpoint_dir ./checkpoints/deepspeech-0.9.1-checkpoint \
    --train_files  ../cv-corpus-5.1-2020-06-22/uk/clips/train.csv \
    --dev_files  ../cv-corpus-5.1-2020-06-22/uk/clips/dev.csv \
    --test_files ../cv-corpus-5.1-2020-06-22/uk/clips/test.csv \
    --epochs 10 \
```
15. Evaluate model:
```
python3 DeepSpeech.py \
    --train_cudnn \
    --alphabet_config_path ./data_uk/alphabet.txt \
    --load_checkpoint_dir ./checkpoints/uk_transfer_checkpoint \
    --train_files  ../cv-corpus-5.1-2020-06-22/uk/clips/train.csv \
    --dev_files  ../cv-corpus-5.1-2020-06-22/uk/clips/dev.csv \
    --test_files ../cv-corpus-5.1-2020-06-22/uk/clips/test.csv \
    --test_batch_size 40 \
    --epochs 0
```
It will take a while, approximately 20-30 minutes.

You will get performance report:
WER - Word Error Rate, calculates how much characters were guessed correctly.
CER - Character Error Rate, calculates how much characters were guessed correctly.
Here we have WER 95% and CER 36%.  
It is high because we don't use scorer (language model that maps chacter sequence to the closest word match) during training, you can improve performance if you create scorer for Ukrainian language. As a text corpus you can use Wikipedia articles.

<details>
<summary>Test on ../cv-corpus-5.1-2020-06-22/uk/clips/test.csv - WER: 0.950863, CER: 0.357779, loss: 59.444176</summary>

--------------------------------------------------------------------------------
Best WER: 
--------------------------------------------------------------------------------
WER: 0.000000, CER: 0.000000, loss: 2.696858
 - wav: file://../cv-corpus-5.1-2020-06-22/uk/clips/common_voice_uk_21203420.wav
 - src: "я замер"
 - res: "я замер"
--------------------------------------------------------------------------------
WER: 0.000000, CER: 0.000000, loss: 1.772630
 - wav: file://../cv-corpus-5.1-2020-06-22/uk/clips/common_voice_uk_21755897.wav
 - src: "що саме"
 - res: "що саме"
--------------------------------------------------------------------------------
WER: 0.000000, CER: 0.000000, loss: 0.269474
 - wav: file://../cv-corpus-5.1-2020-06-22/uk/clips/common_voice_uk_21350648.wav
 - src: "ні"
 - res: "ні"
--------------------------------------------------------------------------------
WER: 0.250000, CER: 0.066667, loss: 7.652889
 - wav: file://../cv-corpus-5.1-2020-06-22/uk/clips/common_voice_uk_22161067.wav
 - src: "і вухом не веде"
 - res: "і вухом не виде"
--------------------------------------------------------------------------------
WER: 0.333333, CER: 0.142857, loss: 22.727850
 - wav: file://../cv-corpus-5.1-2020-06-22/uk/clips/common_voice_uk_20894315.wav
 - src: "подробиці наразі уточнюються"
 - res: "подробиці наразі удочнвітцся"
--------------------------------------------------------------------------------
Median WER: 
--------------------------------------------------------------------------------
WER: 1.000000, CER: 0.408163, loss: 77.099953
 - wav: file://../cv-corpus-5.1-2020-06-22/uk/clips/common_voice_uk_21565481.wav
 - src: "це було висвітлено і в засобах масової інформації"
 - res: "сцеболовистітоно ів засовавнасавинсерматції"
--------------------------------------------------------------------------------
WER: 1.000000, CER: 0.304878, loss: 76.661797
 - wav: file://../cv-corpus-5.1-2020-06-22/uk/clips/common_voice_uk_21568626.wav
 - src: "всі ці зірки для тебе сказав хлопчик і ударив дівчинку металевим тазіком по голові"
 - res: "сицізяртідлетебе сказавни хлобчик юдаревдів чимкуметалевимтазіком поговолі"
--------------------------------------------------------------------------------
WER: 1.000000, CER: 0.261364, loss: 76.638161
 - wav: file://../cv-corpus-5.1-2020-06-22/uk/clips/common_voice_uk_22071941.wav
 - src: "кабінет міністрів україни складає повноваження перед новообраною верховною радою україни"
 - res: "кабіна міністрівукаїни колале повнваженя перебновообрануюварховли радийву країни"
--------------------------------------------------------------------------------
WER: 1.000000, CER: 0.403846, loss: 76.634865
 - wav: file://../cv-corpus-5.1-2020-06-22/uk/clips/common_voice_uk_21381457.wav
 - src: "механізм формування агатів остаточно не встановлений"
 - res: "махенізаформовання оатья востотачномистоновлими"
--------------------------------------------------------------------------------
WER: 1.000000, CER: 0.415094, loss: 76.133347
 - wav: file://../cv-corpus-5.1-2020-06-22/uk/clips/common_voice_uk_21567387.wav
 - src: "засідання верховної ради україни проводяться відкрито"
 - res: "засі веневорковмаградиукраїне проодізівікрипо"
--------------------------------------------------------------------------------
Worst WER: 
--------------------------------------------------------------------------------
WER: 1.500000, CER: 0.266667, loss: 18.258444
 - wav: file://../cv-corpus-5.1-2020-06-22/uk/clips/common_voice_uk_20900153.wav
 - src: "вона віддасться"
 - res: "пона віддас ця"
--------------------------------------------------------------------------------
WER: 1.500000, CER: 0.307692, loss: 15.984250
 - wav: file://../cv-corpus-5.1-2020-06-22/uk/clips/common_voice_uk_22247322.wav
 - src: "ескулап лікар"
 - res: "е скула лліка"
--------------------------------------------------------------------------------
WER: 1.500000, CER: 0.277778, loss: 15.076320
 - wav: file://../cv-corpus-5.1-2020-06-22/uk/clips/common_voice_uk_21582521.wav
 - src: "цензура заборонена"
 - res: "зан зура забороонено"
--------------------------------------------------------------------------------
WER: 1.666667, CER: 0.478261, loss: 42.762665
 - wav: file://../cv-corpus-5.1-2020-06-22/uk/clips/common_voice_uk_21568871.wav
 - src: "пегас символізує поезію"
 - res: "веляс це волі зуя поєсі"
--------------------------------------------------------------------------------
WER: 2.000000, CER: 0.333333, loss: 10.796988
 - wav: file://../cv-corpus-5.1-2020-06-22/uk/clips/common_voice_uk_21563967.wav
 - src: "легітимність"
 - res: "вегі пимнсть"
--------------------------------------------------------------------------------
</details>

16. To export model for later usage:
```
mkdir model
# export .pb file
python3 DeepSpeech.py \
    --train_cudnn \
    --alphabet_config_path ./data_uk/alphabet.txt \
    --load_checkpoint_dir ./checkpoints/uk_transfer_checkpoint \
    --export_dir ./model \
    --epochs 0
# export .tflite file for embedded usage
python3 DeepSpeech.py \
    --train_cudnn \
    --alphabet_config_path ./data_uk/alphabet.txt \
    --load_checkpoint_dir ./checkpoints/uk_transfer_checkpoint \
    --export_tflite --export_dir ./model \
    --epochs 0
```
For advanced usage please refer to https://deepspeech.readthedocs.io/en/v0.9.1/USING.html
</details>
