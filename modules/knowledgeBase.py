import openai
import os
import json
import sqlite3
import datetime
import atexit
from dotenv import load_dotenv

load_dotenv()

outputNum = 20

def getIdentity(identityPath):  
    with open(identityPath, "r", encoding="utf-8") as f:
        identityContext = f.read()
    return {"role": "user", "content": identityContext}

# Ensure the "db" folder exists
db_folder = "db"
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

# Initialize SQLite database for storing knowledge
def init_database():
    db_path = os.path.join(db_folder, "knowledge.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS knowledge (
                    topic TEXT PRIMARY KEY,
                    summary TEXT,
                    date TEXT)''')  # Added date column
    conn.commit()
    conn.close()

#initialite the databse by calling previous function
init_database()

# Updated function to use SQLite for accessing knowledge
def getKnowledge():
    knowledge = {}
    db_path = os.path.join(db_folder, "knowledge.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for row in c.execute("SELECT * FROM knowledge"):
        knowledge[row[0]] = row[1]
    conn.close()
    return knowledge

# Updated function to save knowledge to a JSON file
def saveKnowledge(topic, summary):
    date_added = datetime.datetime.now().strftime('%Y-%m-%d')
    db_path = os.path.join(db_folder, "knowledge.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO knowledge (topic, summary, date) VALUES (?, ?, ?)", (topic, summary, date_added))
    conn.commit()
    conn.close()

# Function to delete knowledge based on a specific date
# Usage deleteKnowledgeByDate('2023-04-14')
def deleteKnowledgeByDate(date_to_delete):
    db_path = os.path.join(db_folder, "knowledge.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM knowledge WHERE date = ?", (date_to_delete,))
    conn.commit()
    conn.close()

def load_history():
    if os.path.exists("conversation.json"):
        with open("conversation.json", "r") as f:
            data = json.load(f)
        return data["history"]
    else:
        return []

history = load_history()

def save_history(history):
    with open("conversation.json", "w") as f:
        json.dump({"history": history}, f)

def add_message_to_history(role, content):
    global history
    history.append({"role": role, "content": content})
    save_history(history)

def end_conversation():
    if history:
        summary = " ".join([message["content"] for message in history if message["role"] == "assistant"])
        saveKnowledge("conversation_summary", summary)

atexit.register(end_conversation)

def getPrompt():
    history = load_history()
    
    prompt = []
    prompt.append(getIdentity(os.getenv('IDENTITY_FILE')))
    prompt.append({"role": "system", "content": f"Below is conversation history.\n"})

    def getLastUserMessage(history):
        for message in reversed(history):
            if message["role"] == "user":
                return message
        return None
    
    last_user_message = getLastUserMessage(history)
    if last_user_message:
        knowledge = getKnowledge()
        if last_user_message['content'] in knowledge:
            topic = knowledge[last_user_message['content']]
            prompt.append({"role": "system", "content": f"Here is some information about {last_user_message['content']}:\n\n{topic}"})
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            user_content = last_user_message['content']
            prompt_text = f"{user_content}\n\nPlease provide some information about {user_content}."
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt_text,
                temperature=1,
                max_tokens=512,
                n=1,
                stop=None,
            )
            topic = response.choices[0].text
            
            saveKnowledge(last_user_message['content'], topic)
            
            prompt.append({"role": "system", "content": f"Here is some information about {last_user_message['content']}:\n\n{topic}"})
    else:
        print("No user message found")
        knowledge = getKnowledge()
    for topic, summary in knowledge.items():
        prompt.append({"role": "system", "content": f"Here is some information about {topic}:\n\n{summary}"})
    
    prompt.append(
        {
            "role": "system",
            "content": f"Here is the latest conversation.\n*Make sure your response is inside {outputNum} characters!\n",
        }
    )
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

