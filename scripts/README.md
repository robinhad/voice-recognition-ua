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

Note: you can also specify dataset with "," e.g. dataset1/train.csv,dataset2/train.csv.

You have a reproducible dataset!


# Scorer

1. Refer to DeepSpeech guide for further explanations.

2. Generate scorer package.
```
python3 generate_lm.py --input_txt ../../../voice-recognition-ua/data/all_text.txt --output_dir . \
  --top_k 500000 --kenlm_bins ../../../voice-recognition-ua/kenlm/build/bin \
  --arpa_order 5 --max_arpa_memory "85%" --arpa_prune "0|0|1" \
  --binary_a_bits 255 --binary_q_bits 8 --binary_type trie
```
3. Run lm_optimizer to find the best scorer value.
4. Rerun step 2 to generate new scorer.

Caution: scorer is very model-dependant, so you'll likely need to adjust it to each model.