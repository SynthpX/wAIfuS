import streamlit as st
import json
import os
import shutil
import sys
import time
import threading
import traceback
import keyboard
from dotenv import load_dotenv
import openai
from modules.translate import *
from modules.TTS import *
from modules.prompt import *
from modules.audioProcess import record_audio, openai_answer

def create_character_page():
    st.markdown("# Waifu Builder!")
    chara_name = st.text_input(max_chars=25, label="Character Name")
    char_persona = st.text_area(label="Character persona", placeholder="Personality of your waifu")
    char_greeting = st.text_area(label="Character greeting", placeholder="Greeting of your waifu")
    example_dialogue = st.text_area(label="Example Dialogue", placeholder="Dialogue Example of your waifu")
    world_scenario = st.text_area(label="World Scenario", placeholder="World scenario for your waifu")

    create_identity = st.button('Create Identity')

    if create_identity:
        waifu_data = {
            "char_name": chara_name,
            "char_persona": char_persona,
            "char_greeting": char_greeting,
            "example_dialogue": example_dialogue,
            "world_scenario": world_scenario
        }

        with open(f"{chara_name}.json", "w") as json_file:
            json.dump(waifu_data, json_file, indent=4)
        
        st.success("Identity created and saved as JSON file.")

def chatting():
    from modules.identity import createWaifuPrompt
    st.markdown("# Start Chatting")
    file_uploader_placeholder = st.empty()
    markdown_text = st.empty()
    uploaded_file = file_uploader_placeholder.file_uploader("Import your waifu", type="json")

    if uploaded_file is not None:
        
        char_data = json.load(uploaded_file)
        json_filename = uploaded_file.name
        uploaded_file.seek(0)

        # Save the uploaded file to the main folder
        destination = os.path.join(os.getcwd(), json_filename)
        with open(destination, 'wb') as f:
            shutil.copyfileobj(uploaded_file, f)
        prompt = createWaifuPrompt(json_filename)

        # Save the prompt in a text file called identity.txt
        with open("identity.txt", "w") as text_file:
            text_file.write(prompt)
        st.success(f"Character {char_data['char_name']} imported successfully from {json_filename}!")

        # Hide the file uploader and markdown text
        file_uploader_placeholder.empty()
        markdown_text.empty()
        # Start conversation after importing JSON
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
        mode = st.selectbox("Select mode:", ["Microphone", "Experimental"], index=0)
        if mode == "Microphone":
            st.write("Press and Hold Right Shift to record audio")
            if st.button("Start"):
                while True:
                    if keyboard.is_pressed('RIGHT_SHIFT'):
                        record_audio()
        elif mode == "Experimental":
            thread = threading.Thread(target=prepare_response)
            thread.start()
            thread.start()
            thread.join()
    else:
        markdown_text.markdown("Please upload a JSON file to start the conversation.")

st.set_page_config(
    page_title="Waifu",
    page_icon="🧊",
    layout="wide"
)

st.header("Waifu Role Play Chatbot")
st.markdown("## Role Play with Your Custom Waifu with Audio!")

menu_options = ["Main Menu", "Create Character", "Chatting"]
menu_choice = st.sidebar.selectbox("Choose an option", menu_options)

if menu_choice == "Create Character":
    create_character_page()
elif menu_choice == "Chatting":
    chatting()