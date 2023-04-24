import logging
import typing as t
import json
import os
from pathlib import Path
from typing import Tuple

from dotenv import load_dotenv
logger = logging.getLogger(__name__)


load_dotenv()
owner_name = os.getenv('OWNER_NAME')

def read_identity_file(identity_path: str) -> Tuple[str, str]:
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

    except FileNotFoundError:
        logger.error(f"File {identity_path} not found.")
        return None, None
    except KeyError as e:
        logger.error(f"Key error: {e}. Please check the JSON file format.")
        return None, None

    return char_name, char_persona

def identity(
    char_name: str,
    char_persona: str,
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
    #merged_string = f"Consider that the following is conversation between an AI Assistant named {char_name} and {owner_name}.\n {char_persona}\n "
    merged_string = f"You are Akagi from Azur Lane. Reply to me as im Kaga."
    return merged_string

def getIdentity(identityPath):
    char_name, char_persona = read_identity_file(identityPath)
    identityContext = identity(char_name, char_persona)
    return identityContext


