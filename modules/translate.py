import requests
import json
import sys
import googletrans
import deepl
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

translator_cache = {"googletrans": None, "deepl": None}

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
        logger.error(f"Error in translate_deeplx: {e}")
        return

    data = response.json()
    translated_text = data['data']

    return translated_text

def translate_deepL(text, source, target):
    global translator_cache

    if translator_cache["deepl"] is None:
        api_key = os.getenv('DEEPL_AUTH_KEY')
        translator_cache["deepl"] = deepl.Translator(auth_key=api_key)

    translator = translator_cache["deepl"]

    translation = translator.translate_text(text, source_lang=source, target_lang=target)
    translation_str = str(translation)

    return translation_str

def translate_google(text, source, target):
    global translator_cache

    try:
        if translator_cache["googletrans"] is None:
            translator_cache["googletrans"] = googletrans.Translator()

        translator = translator_cache["googletrans"]
        result = translator.translate(text, src=source, dest=target)
        return result.text
    except:
        logger.error("Error in translate_google")
        return

def detect_google(text):
    global translator_cache

    try:
        if translator_cache["googletrans"] is None:
            translator_cache["googletrans"] = googletrans.Translator()

        translator = translator_cache["googletrans"]
        result = translator.detect(text)
        return result.lang.upper()
    except:
        logger.error("Error in detect_google")
        return