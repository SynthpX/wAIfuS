import openai
import sys
import time
import keyboard
import threading
import traceback
from emoji import demojize
from config import *
from modules.translate import *
from modules.TTS import *
from modules.subtitle import *
from modules.knowledgeBase import *
from utils.twitch_config import *
from dotenv import load_dotenv
from modules.liveChat import *
from modules.audioProcess import *

load_dotenv()

# to help the CLI write unicode characters to the terminal
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

# use your own API Key, you can get it from https://openai.com/. I place my API Key in a separate file called config.py
openai.api_key = os.getenv('OPENAI_API_KEY')

conversation = []
# Create a dictionary to hold the message data
history = {"history": conversation}

mode = 0
total_characters = 0
chat = ""
chat_now = ""
chat_prev = ""
is_Speaking = False

# function to get the user's input audio

def preparation():
    global conversation, chat_now, chat, chat_prev
    while True:
        try:
            # If the assistant is not speaking, and the chat is not empty, and the chat is not the same as the previous chat
            # then the assistant will answer the chat
            chat_now = chat
            if is_Speaking == False and chat_now != chat_prev:
                # Saving chat history
                conversation.append({'role': 'user', 'content': chat_now})
                chat_prev = chat_now
                openai_answer()
        except Exception as e:
            # Log the error and continue
            print(f"Error in preparation(): {e}")
            traceback.print_exc()
        time.sleep(1)

if __name__ == "__main__":
    t = None
    try:
        # You can change the mode to 1 if you want to record audio from your microphone
        # or change the mode to 2 if you want to capture livechat from youtube
        print("Select mode:")
        print(f"{1}: Microphone")
        print(f"{2}: YouTube Live")
        print(f"{3}: Twitch Live")
        mode = input("Mode : ")

        if mode == "1":
            print("Press and Hold Right Shift to record audio")
            while True:
                if keyboard.is_pressed('RIGHT_SHIFT'):
                    record_audio()
            
        elif mode == "2":
            live_id = input("Livestream ID: ")
            # Threading is used to capture livechat and answer the chat at the same time
            t = threading.Thread(target=preparation)
            t.start()
            yt_livechat(live_id)

        elif mode == "3":
            # Threading is used to capture livechat and answer the chat at the same time
            print("To use this mode, make sure to change utils/twitch_config.py to your own config")
            t = threading.Thread(target=preparation)
            t.start()
            twitch_livechat()
    except KeyboardInterrupt:
        if t is not None:
            t.join()
        print("Stopped")

