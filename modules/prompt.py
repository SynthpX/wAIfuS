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

def getPrompt():
    identityContext = getIdentity()
    
    with open("conversation.json", "r") as file:
        data = json.load(file)

    # Initialize the 'prompt' list

    # Iterate through the 'history' key in the JSON data
    for conversation in data["history"]:
        role = conversation["role"]
        content = conversation["content"]

    prompt = []
    prompt.append({"role": "system", "content": f"{identityContext}\n The RP will begin.\n You will act as Yae Miko.\n Only do Yae Miko part.\n <<Begin>>"})
    # Append the content to the 'prompt' list with the correct role
    if role == "user" or role == "assistant":
        prompt.append({"role": role, "content": content})
    
    print(prompt)
    return prompt
