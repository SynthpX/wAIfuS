LINE_LENGTH = 10

def write_lines_to_file(filename, text, line_length):
    """Writes the given text to a file, splitting it into lines with the specified length."""
    try:
        with open(filename, "w", encoding="utf-8") as outfile:
            words = text.split()
            lines = [words[i:i + line_length] for i in range(0, len(words), line_length)]
            for line in lines:
                outfile.write(f"{' '.join(line)}\n")
    except IOError as e:
        print(f"Error writing to {filename}: {e}")

def generate_subtitle(chat_text, response_text, line_length=LINE_LENGTH):
    """
    Generates subtitle and chat files with fixed line lengths.

    :param chat_text: The text of the chat.
    :param response_text: The text of the response.
    :param line_length: The maximum number of words in a line.
    """
    write_lines_to_file("output.txt", response_text, line_length)
    write_lines_to_file("chat.txt", chat_text, line_length)