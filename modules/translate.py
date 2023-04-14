import requests
import json
import sys
import googletrans
import deepl
import os
from dotenv import load_dotenv

load_dotenv()

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

# You can use DeepL or Google Translate to translate the text
# DeepL can translate more casual text in Japanese
# DeepLx is a free and open-source DeepL API, i use this because DeepL Pro is not available in my country
# but sometimes i'm facing request limit, so i use Google Translate as a backup
def translate_deeplx(text, source, target):
    url = "http://localhost:1188/translate"
    headers = {"Content-Type": "application/json"}

    # define the parameters for the translation request
    params = {
        "text": text,
        "source_lang": source,
        "target_lang": target
    }

    # convert the parameters to a JSON string
    payload = json.dumps(params)

    # send the POST request with the JSON payload
    response = requests.post(url, headers=headers, data=payload)

    # get the response data as a JSON object
    data = response.json()

    # extract the translated text from the response
    translated_text = data['data']

    return translated_text

def translate_deepL(text, source, target):
    # Replace YOUR_DEEPL_API_KEY with your actual API key
    api_key = os.getenv('DEEPL_AUTH_KEY')

    # Initialize a DeepL Translator object with the API key
    translator = deepl.Translator(auth_key=api_key)

    # Translate the text from the source to the target language
    translation = translator.translate_text(text, source_lang=source, target_lang=target)

    # Convert the TextResult object to a string
    translation_str = str(translation)

    # Return the translated text
    return translation_str

def translate_google(text, source, target):
    try:
        translator = googletrans.Translator()
        result = translator.translate(text, src=source, dest=target)
        return result.text
    except:
        print("Error translate")
        return
    
def detect_google(text):
    try:
        translator = googletrans.Translator()
        result = translator.detect(text)
        return result.lang.upper()
    except:
        print("Error detect")
        return

if __name__ == "__main__":
    text = "aku tidak menyukaimu"
    source = translate_deeplx(text, "ID", "ID")
    print(source)
