# How to prepare dataset for training

1. Download Ukrainian dataset from [https://github.com/egorsmkv/speech-recognition-uk](https://github.com/egorsmkv/speech-recognition-uk).
2. Delete Common Voice folder in dataset
3. Download [import_ukrainian.py](scripts/import_ukrainian.py) and put into DeepSpeech/bin folder.
4. Run import script
5. Download Common Voice 6.1 Ukrainian dataset
6. Convert to DeepSpeech format
7. Merge train.csv from dataset and from DeepSpeech into one file
8. Put CV files into dataset files folder
9. Put dev.csv and test.csv into folder

You have a reproducible dataset!
