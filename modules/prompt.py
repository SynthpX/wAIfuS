import os
import json
from dotenv import load_dotenv
from modules.identity import read_identity_file, identity

load_dotenv()

memorySize = 5
num_clusters = 5
outputNum = 20

def getIdentity(identityPath):
    #char_name, char_persona, char_greeting, example_dialogue, world_scenario = read_identity_file(identityPath)
    #identityContext = identity(char_name, char_persona, char_greeting, example_dialogue, world_scenario)
    identityContext = f"You are Asuna from Sword Art Online. Reply to me as im Kirito."
    return identityContext

def load_history():
    if os.path.exists("conversation.json"):
        with open("conversation.json", "r") as f:
            data = json.load(f)
        return data["history"]
    else:
        return []

history = load_history()

def getPrompt():
    history = load_history()
    ident = getIdentity("identity.json")

    prompt = []
    prompt.append({"role": "system", "content": f"{ident}"})
    prompt.append(history[-1])

    def getTotalPromptLength(prompt):
        return sum(len(d['content']) for d in prompt)

    total_len = getTotalPromptLength(prompt)
    while total_len > 4000:
        try:
            prompt.pop(2)
            total_len = getTotalPromptLength(prompt)
        except:
            print("Error: Prompt too long!")
    return prompt
