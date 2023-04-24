import os
import json
from dotenv import load_dotenv

load_dotenv()

memorySize = 5
num_clusters = 5
outputNum = 20

def getIdentity():
    with open("identity.txt", "r") as file:
        identityContext = file.read()
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
    identityContext = getIdentity()

    prompt = []
    prompt.append({"role": "system", "content": f"{identityContext}\n The RP will begin. You will act as Yae Miko. <<Begin>>"})
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
