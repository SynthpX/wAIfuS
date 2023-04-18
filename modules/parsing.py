import re
import typing as t

def parse_messages(string: str, names: t.List[str]) -> t.List[str]:
    """
    Parse chat history from a string into a list of individual messages.

    :param string: The chat history string
    :param names: A list of speaker names
    :return: A list of individual messages
    """
    sanitized_names = [re.escape(name) for name in names]
    speaker_regex = re.compile(rf"^({'|'.join(sanitized_names)}): ?", re.MULTILINE)

    message_start_indexes = [match.start() for match in speaker_regex.finditer(string)]

    if len(message_start_indexes) < 2:
        return [string.strip()]

    messages = extract_messages(string, message_start_indexes)
    return messages

def extract_messages(string: str, message_start_indexes: t.List[int]) -> t.List[str]:
    """
    Extract individual messages based on the start indexes.

    :param string: The chat history string
    :param message_start_indexes: A list of message start indexes
    :return: A list of individual messages
    """
    messages = []
    prev_start_idx = message_start_indexes[0]

    for start_idx in message_start_indexes[1:]:
        message = string[prev_start_idx:start_idx].strip()
        messages.append(message)
        prev_start_idx = start_idx

    messages.append(string[prev_start_idx:].strip())

    return messages

def serialize_chat_history(history: t.List[str]) -> str:
    """
    Serialize a structured chat history object into a string.

    :param history: A list of individual chat history messages
    :return: The serialized chat history string
    """
    return "\n".join(history)