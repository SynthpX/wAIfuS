import os
import torch
import requests
import urllib.parse
from modules.katakana import *
from dotenv import load_dotenv
load_dotenv()

def silero_tts(text, language, model_name, speaker):
    device = torch.device('cpu')
    torch.set_num_threads(4)
    model_file = 'model.pt'

    if not os.path.isfile(model_file):
        torch.hub.download_url_to_file(
            f'https://models.silero.ai/models/tts/{language}/{model_name}.pt',
            model_file)  

    model = torch.package.PackageImporter(model_file).load_pickle("tts_models", "model")
    model.to(device)
    sample_rate = 48000

    audio_paths = model.save_wav(text=text,
                                 speaker=speaker,
                                 sample_rate=sample_rate)

def voicevox_tts(text):
    voicevox_url = os.getenv('VOICEVOX_URL')
    katakana_text = katakana_converter(text)
    speaker_id = 46  # You can change the speaker ID according to your preference

    audio_query_params = urllib.parse.urlencode({'text': katakana_text, 'speaker': speaker_id})
    audio_query_response = requests.post(f'{voicevox_url}/audio_query?{audio_query_params}')

    synthesis_params = urllib.parse.urlencode({'speaker': speaker_id, 'enable_interrogative_upspeak': True})
    synthesis_response = requests.post(f'{voicevox_url}/synthesis?{synthesis_params}', json=audio_query_response.json())

    with open("test.wav", "wb") as outfile:
        outfile.write(synthesis_response.content)

if __name__ == "__main__":
    silero_tts()
