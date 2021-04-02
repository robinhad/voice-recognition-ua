# this script is used for importing wiki text into scorer format
from wiki_dump_reader import Cleaner, iterate
from os import remove
from os.path import exists
import nltk
import re
nltk.download("punkt")

OUT_PATH = "../data/wiki_text.txt"

if exists(OUT_PATH):
    remove(OUT_PATH)
text_file = open(OUT_PATH, mode="a")

tokenizer = nltk.SpaceTokenizer()
paranthesis_regex = re.compile(r'\(.*\)')
allowed_chars = ["а", "б", "в", "г", "ґ", "д", "е", "є", "ж", "з", "и", "і", "ї", "й", "к", "л",
                 "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ь", "ю", "я", "-", "'"]

cleaner = Cleaner()
# iter = 0
for title, text in iterate('../data/ukwiki-20210320-pages-articles-multistream.xml'):
    text = cleaner.clean_text(text)
    cleaned_text, _ = cleaner.build_links(text)
    cleaned_text = cleaned_text.lower()
    cleaned_text = cleaned_text.replace("&nbsp;", " ")
    cleaned_text = cleaned_text.replace("н. е.", "нашої ери")
    cleaned_text = cleaned_text.replace("ім.", "імені")
    cleaned_text = cleaned_text.replace("див.", "дивись")
    cleaned_text = paranthesis_regex.sub('', cleaned_text)
    cleaned_text = cleaned_text.strip()
    cleaned_text = cleaned_text.split(".")
    out_text = []
    for text in cleaned_text:
        text = text.strip()
        if text.endswith(", що вивчає"):
            continue
        if text.startswith("redirect") or text.startswith("перенаправлення"):
            continue

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
    # iter += 1
    # if iter > 5:
    #    break

text_file.close()
