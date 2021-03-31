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
            words = [i for i in words if i.isalnum()]
            words = [i for i in words if not i.isdigit()]
            words = [i for i in words if len(i) > 1]
            if any([any(j not in allowed_chars for j in i) for i in words]):
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
