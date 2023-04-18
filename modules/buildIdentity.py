import logging
import typing as t
import json
from pathlib import Path
from typing import Tuple
from parsing import parse_messages

logger = logging.getLogger(__name__)

history = ["You: How was your day?", "Identity name: My day was wonderful, Master."]
user_message = "What are your plans for tomorrow?"

def read_identity_file(identity_path: str) -> Tuple[str, str, str, str, str]:
    """
    Read an identity file and return the character information.

    :param identity_path: The path to the identity JSON file
    :return: A tuple containing character name, persona, greeting, example dialogue, and world scenario
    """
    try:
        with open(Path(identity_path), "r", encoding="utf-8") as f:
            identity = json.load(f)
        
        char_name = identity["char_name"]
        char_persona = identity["char_persona"]
        char_greeting = identity["char_greeting"]
        example_dialogue = identity["example_dialogue"]
        world_scenario = identity["world_scenario"]

    except FileNotFoundError:
        logger.error(f"File {identity_path} not found.")
        return None, None, None, None, None
    except KeyError as e:
        logger.error(f"Key error: {e}. Please check the JSON file format.")
        return None, None, None, None, None

    return char_name, char_persona, char_greeting, example_dialogue, world_scenario

def build_prompt(
    history: t.List[str],
    user_message: str,
    char_name: str,
    char_persona: t.Optional[str] = None,
    example_dialogue: t.Optional[str] = None,
    world_scenario: t.Optional[str] = None,
) -> str:
    """
    Constructs a prompt for the AI model.

    :param history: The dialogue history
    :param user_message: The user's message
    :param char_name: The character's name
    :param char_persona: The character's persona (optional)
    :param example_dialogue: The character's example dialogue (optional)
    :param world_scenario: The world scenario (optional)
    :return: The constructed prompt string
    """
    example_history = (
        parse_messages(example_dialogue, ["You", char_name])
        if example_dialogue
        else []
    )
    concatenated_history = [*example_history, *history]

    prompt_turns = [
        "<START>",
        *concatenated_history[-8:],
        f"You: {user_message}",
        f"{char_name}:",
    ]

    if world_scenario:
        prompt_turns.insert(0, f"Scenario: {world_scenario}")

    if char_persona:
        prompt_turns.insert(0, f"{char_name}'s Persona: {char_persona}")

    logger.debug("Constructed prompt is: `%s`", prompt_turns)
    prompt_str = "\n".join(prompt_turns)
    return prompt_str

if __name__ == "__main__":
    identity_file_path = "identity.json"
    char_name, char_persona, char_greeting, example_dialogue, world_scenario = read_identity_file(identity_file_path)
    prompt = build_prompt(history, user_message, char_name, char_persona, example_dialogue, world_scenario)
    print(prompt)