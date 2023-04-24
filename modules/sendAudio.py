from pathlib import Path
import sounddevice as sd
import soundfile as sf

TTS_WAV_PATH = Path(__file__).resolve().parents[1] / 'test.wav'

def play_voice(device_ids):
    data, fs = sf.read(TTS_WAV_PATH, dtype='float32')
    for device_id in device_ids:
        sd.play(data, fs, device=device_id)
        sd.wait()