import logging
import typing as t
import json
import os
from pathlib import Path
from typing import Tuple

from modules.parsing import parse_messages
from dotenv import load_dotenv
logger = logging.getLogger(__name__)


load_dotenv()
owner_name = os.getenv('OWNER_NAME')

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

def identity(
    char_name: str,
    char_persona: str,
    char_greeting: str,
    example_dialogue: str,
    world_scenario: str,
) -> str:
    """
     Merges the character information into a single string.
    :param char_name: The character's name
    :param char_persona: The character's persona
    :param char_greeting: The character's greeting
    :param example_dialogue: The character's example dialogue
    :param world_scenario: The world scenario
    :return: The merged string
    """
    merged_string = f"Your creator name is {owner_name}.\n Your name is {char_name}.\n {char_name}'s Personality: {char_persona}.\nScenario: {world_scenario}\n\n"
    return merged_string



