import openai
from dotenv import load_dotenv
import os
from time import time, sleep
load_dotenv()

def completion(prompt, 
                    engine="text-davinci-003",
                    temperature=1,
                    top_p=1,
                    max_tokens=1000,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    max_retries=5):
    """
    Query GPT-3 API with given prompt and return the generated text.
    
    :param prompt: Input text prompt to the GPT-3 model.
    :param engine: GPT-3 model engine name.
    :param temperature: Sampling temperature, higher values increase randomness.
    :param top_p: Nucleus sampling parameter, value between 0 and 1.
    :param max_tokens: Maximum number of tokens in generated text.
    :param frequency_penalty: Penalty for frequent tokens, higher values decrease common tokens.
    :param presence_penalty: Penalty for token repetition, higher values decrease repetitions.
    :param stop: List of stop words or phrases.
    :param max_retries: Maximum number of retries in case of API errors.
    :return: Generated text from GPT-3.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    retries = 0
    prompt = prompt.encode(encoding="ASCII", errors="ignore").decode()
    
    while retries < max_retries:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
            )
            generated_text = response.choices[0].text
            return generated_text
        except Exception as error:
            retries += 1
            print(f"Error communicating with OpenAI (attempt {retries}/{max_retries}): {error}")
            sleep(1)
    return f"GPT3 error after {max_retries} retries: {error}"