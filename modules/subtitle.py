LINE_LENGTH = 10

def generate_subtitle(chat_now, result_id):
    # Output subtitle file for OBS
    try:
        with open("output.txt", "w", encoding="utf-8") as outfile:
            words = result_id.split()
            lines = [words[i:i+LINE_LENGTH] for i in range(0, len(words), LINE_LENGTH)]
            for line in lines:
                outfile.write(f"{' '.join(line)}\n")
    except IOError as e:
        print(f"Error writing to output.txt: {e}")
        return

    # Output chat file for OBS
    try:
        with open("chat.txt", "w", encoding="utf-8") as outfile:
            words = chat_now.split()
            lines = [words[i:i+LINE_LENGTH] for i in range(0, len(words), LINE_LENGTH)]
            for line in lines:
                outfile.write(f"{' '.join(line)}\n")
    except IOError as e:
        print(f"Error writing to chat.txt: {e}")
        return