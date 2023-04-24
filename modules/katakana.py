import MeCab
import unidic
import pandas as pd
import alkana
import re
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

alpha_regex = re.compile(r'^[a-zA-Z]+$')


def is_alpha(string):
    return alpha_regex.match(string) is not None


def katakana_converter(text):
    wakati = MeCab.Tagger('-Owakati')
    wakati_result = wakati.parse(text)

    df = pd.DataFrame(wakati_result.split(" "), columns=["word"])
    df = df[df["word"].str.isalpha() == True]
    df["is_english_word"] = df["word"].apply(is_alpha)
    df = df[df["is_english_word"] == True]
    df["katakana"] = df["word"].apply(alkana.get_kana)

    word_to_katakana = dict(zip(df["word"], df["katakana"]))

    for word, katakana in word_to_katakana.items():
        try:
            text = text.replace(word, katakana)
        except:
            pass
    return text