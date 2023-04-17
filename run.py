import os
import sys
import time
import threading
import traceback
from dotenv import load_dotenv
import openai
import keyboard
from config import *
from modules.translate import *
from modules.TTS import *
from modules.knowledgeBase import *
from utils.twitch_config import *
from modules.audioProcess import *

load_dotenv()

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
openai.api_key = os.getenv('OPENAI_API_KEY')

class Conversation:
    def __init__(self):
        self.conversation_history = []
        self.chat_now = ""
        self.chat_prev = ""
        self.is_speaking = False

    def update_chat(self, chat):
        if not self.is_speaking and chat != self.chat_prev:
            self.conversation_history.append({'role': 'user', 'content': chat})
            self.chat_prev = chat
            return True
        return False

def prepare_response(conversation):
    while True:
        try:
            if conversation.update_chat(conversation.chat_now):
                openai_answer(conversation)
        except Exception as e:
            print(f"Error in prepare_response(): {e}")
            traceback.print_exc()
        time.sleep(1)

def main():
    conversation = Conversation()
    mode = None
    thread = None

    try:
        print("Select mode:")
        print(f"{1}: Microphone")
        print(f"{2}: Experimental")
        mode = input("Mode : ")

        if mode == "1":
            print("Press and Hold Right Shift to record audio")
            while True:
                if keyboard.is_pressed('RIGHT_SHIFT'):
                    record_audio()
        
        elif mode == "2":
            thread = threading.Thread(target=prepare_response)
            thread.start()
            
    except KeyboardInterrupt:
        if thread is not None:
            thread.join()
        print("Stopped")

if __name__ == "__main__":
    main()