# this script is used for importing random texts from folder and converting it for scorer
import os
import nltk
import re
nltk.download("punkt")

FOLDER = "../data/текст/"
OUT_FILE = "../data/texts.txt"
text_file = open(OUT_FILE, mode="a")

tokenizer = nltk.SpaceTokenizer()
paranthesis_regex = re.compile(r'\(.*\)')
allowed_chars = ["а", "б", "в", "г", "ґ", "д", "е", "є", "ж", "з", "и", "і", "ї", "й", "к", "л",
                 "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ь", "ю", "я", "-", "'"]

for subdir, dirs, files in os.walk(FOLDER):
    for file in files:
        file_path = os.path.join(subdir, file)
        print(file_path)
        input_file = open(file_path)
        try:
            cleaned_text = input_file.read()
        except:
            input_file.close()
            input_file = open(file_path, encoding="cp1251")
            cleaned_text = input_file.read()
        cleaned_text = cleaned_text.lower()
        cleaned_text = paranthesis_regex.sub('', cleaned_text)
        cleaned_text = cleaned_text.strip()
        cleaned_text = cleaned_text.split(".")
        out_text = []
        for text in cleaned_text:
            text = text.strip()

            words = tokenizer.tokenize(text)
            words = [i for i in words if not i.isdigit()]
            new_words = []
            for word in words:
                include = True
                for letter in word:
                    if word.startswith("-"):
                        word = word[1:]
                    if letter not in allowed_chars:
                        include = False
                if include:
                    new_words.append(word)
            words = new_words
            if all([len(i) <= 1 for i in words]):
                continue
            if len(words) == 0:
                continue
            out_text.append(
                " ".join(words))
        cleaned_text = "\n".join(out_text)
        if cleaned_text == "":
            continue
        text_file.write(cleaned_text + "\n")
        input_file.close()


text_file.close()
