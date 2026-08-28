# get_user_input.py
# This file asks the user for their provider, API key, and models to test.

from getpass import getpass


def get_provider():
    """
    Ask the user which provider they want to use.
    """
    print("Which provider do you want to use?")
    print("Examples: groq, openai, anthropic, google_genai")
    provider = input("Provider: ").strip()
    return provider


def get_api_key():
    """
    Ask the user for their API key.
    We use getpass() instead of input() so the key doesn't show on screen.
    """
    api_key = getpass("Enter your API key (hidden while typing): ").strip()
    return api_key


def get_model_list():
    """
    Ask the user which model names they want to test.
    They can type multiple, separated by commas.
    """
    print("\nEnter the model names you want to test, separated by commas.")
    print("Example: openai/gpt-oss-20b, openai/gpt-oss-120b")
    raw_input_text = input("Models: ")

    # Split by comma, then remove extra spaces around each name
    model_list = [name.strip() for name in raw_input_text.split(",")]

    return model_list


def get_question():
    """
    Ask the user for the question they want to benchmark.
    """
    question = input("\nEnter your question: ")
    return question