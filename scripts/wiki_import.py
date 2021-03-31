from wiki_dump_reader import Cleaner, iterate
from os import remove
import nltk
import re
nltk.download("punkt")


remove("../data/wiki_text.txt")
text_file = open("../data/wiki_text.txt", mode="a")

tokenizer = nltk.SpaceTokenizer()
paranthesis_regex = re.compile(r'\(.*\)')
allowed_chars = ["а", "б", "в", "г", "ґ", "д", "е", "є", "ж", "з", "и", "і", "ї", "й", "к", "л",
                 "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ь", "ю", "я", "-", "'"]

cleaner = Cleaner()
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

text_file.close()
