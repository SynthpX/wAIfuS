import requests
import json
import sys
import googletrans
import deepl
import os
from dotenv import load_dotenv

load_dotenv()

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

def translate_deeplx(text, source, target):
    url = "http://localhost:1188/translate"
    headers = {"Content-Type": "application/json"}

    params = {
        "text": text,
        "source_lang": source,
        "target_lang": target
    }

    payload = json.dumps(params)

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error in translate_deeplx: {e}")
        return

    data = response.json()
    translated_text = data['data']

    return translated_text

def translate_deepL(text, source, target):
    api_key = os.getenv('DEEPL_AUTH_KEY')
    translator = deepl.Translator(auth_key=api_key)

    translation = translator.translate_text(text, source_lang=source, target_lang=target)
    translation_str = str(translation)

    return translation_str

def translate_google(text, source, target):
    try:
        translator = googletrans.Translator()
        result = translator.translate(text, src=source, dest=target)
        return result.text
    except:
        print("Error in translate_google")
        return

def detect_google(text):
    try:
        translator = googletrans.Translator()
        result = translator.detect(text)
        return result.lang.upper()
    except:
        print("Error in detect_google")
        return

if __name__ == "__main__":
    text = "aku tidak menyukaimu"
    source = translate_deeplx(text, "ID", "ID")
    print(source)