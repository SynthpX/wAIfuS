import pyaudio
import keyboard
import wave
import openai
import os
import json
import time
import winsound
from faster_whisper import WhisperModel
from dotenv import load_dotenv
from modules.translate import *
from modules.knowledgeBase import *
from modules.TTS import *
from modules.sendAudio import play_voice
from modules.emotionRecognition import emotion_recognition

# Load environment variables
load_dotenv()


# Define constants
owner_name = os.getenv('OWNER_NAME')
MIC_ID = int(os.getenv('MICROPHONE_ID'))
CABLE_ID = int(os.getenv('CABLE_INPUT_ID'))
SPEAKER_ID = int(os.getenv('VOICEMEETER_INPUT_ID'))

# Create a dictionary to hold the message data
conversation = []
history = {"history": conversation}

def record_audio():
    """Record audio while the right shift key is pressed."""
    # Audio settings
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "input.wav"

    # Initialize the PyAudio object
    p = pyaudio.PyAudio()

    # Open the audio stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=MIC_ID)

    # Initialize the list of audio frames
    frames = []

    # Record audio while the right shift key is pressed
    print("Press and hold Right Shift to record audio")
    while keyboard.is_pressed('RIGHT_SHIFT'):
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop recording
    print("Stopped recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Write the audio frames to a WAV file
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    # Transcribe the audio file
    transcribe_audio(WAVE_OUTPUT_FILENAME)

# translating is optional
def translate_text(text):
    global is_Speaking
    # subtitle will act as subtitle for the viewer
    # subtitle = translate_google(text, "ID")

    #emot recog for VtubeStudio (future)
    #emotion = emotion_recognition(text)

    # tts will be the string to be converted to audio
    detect = detect_google(text)
    tts = translate_google(text, f"{detect}", "JA")
    tts_id = translate_deepL(text, f"{detect}", "ID")
    #tts_id = translator.translate_text(eng_speech, target_lang=TARGET_LANGUAGE)
    # tts = translate_deeplx(text, f"{detect}", "JA")
    tts_en = translate_google(text, f"{detect}", "EN")    
    try:
        print("ID : " + tts_id)
        print("JP : " + tts)
        print("EN : " + tts_en)
    except Exception as e:
        print("Error printing text: {0}".format(e))
        return

    # Choose between the available TTS engines
    # Japanese TTS
    # voicevox_tts(tts)

    # Silero TTS, Silero TTS can generate English, Russian, French, Hindi, Spanish, German, etc. Uncomment the line below. Make sure the input is in that language
    silero_tts(tts_en, "en", "v3_en", "en_21")


    time.sleep(1)

    # is_Speaking is used to prevent the assistant speaking more than one audio at a time
    #is_Speaking = True
    #winsound.PlaySound("test.wav", winsound.SND_FILENAME)
    #is_Speaking = False

    audio_device_ids = [CABLE_ID]  # Replace with the IDs of your desired audio devices
    play_voice(audio_device_ids)

    # Clear the text files after the assistant has finished speaking
    time.sleep(1)
    with open ("output.txt", "w") as f:
        f.truncate(0)
    with open ("chat.txt", "w") as f:
        f.truncate(0)


def transcribe_audio(file_path):
    """Transcribe the given audio file."""
    model_size = "small"

    # Run on CPU with int8
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    global chat_now
    try:
        with open(file_path, "rb") as audio_file:
            segments, info = model.transcribe(audio_file, beam_size=5)
            chat_now = " ".join(segment.text for segment in segments)
            print(f"Question: {chat_now.strip()}")
    except openai.error.InvalidRequestError as e:
        print(f"Error transcribing audio: {e}")
        return
    result = f"{chat_now}"
    conversation.append({'role': 'user', 'content': result})
    openai_answer()

def openai_answer():
    global total_characters, conversation

    total_characters = sum(len(d['content']) for d in conversation)

    while total_characters > 4000:
        try:
            conversation.pop(2)
            total_characters = sum(len(d['content']) for d in conversation)
        except Exception as e:
            print("Error removing old messages: {0}".format(e))

    unanswered_questions = [msg for msg in conversation if msg['role'] == 'user' and not msg.get('answered')]
    if not unanswered_questions:
        return

    with open("conversation.json", "w", encoding="utf-8") as f:
        # Write the message data to the file in JSON format
        json.dump(history, f, indent=4)

    prompt = getPrompt()
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=512,
        temperature=1,
        top_p=0.9
    )
    message = response['choices'][0]['message']['content']
    conversation.append({'role': 'assistant', 'content': message})
    for msg in unanswered_questions:
        msg['answered'] = True
    translate_text(message)
