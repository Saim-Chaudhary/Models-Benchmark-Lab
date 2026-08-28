# benchmark.py
# This file contains the logic for testing ONE model.

from langchain.chat_models import init_chat_model
import time


def run_model(model_name, question, api_key, provider):
    """
    This function:
    1. Connects to a model using the given provider
    2. Sends the question
    3. Times how long it takes
    4. Gets token usage
    5. Returns everything as a dictionary
    """

    # Step 1: Create the model connection using the chosen provider
    model = init_chat_model(
        model_name,
        model_provider=provider,
        api_key=api_key
    )

    # Step 2: Record time before sending the question
    start_time = time.time()

    # Step 3: Ask the question
    response = model.invoke(question)

    # Step 4: Record time after getting the response
    end_time = time.time()

    # Step 5: Calculate time taken
    time_taken = end_time - start_time

    # Step 6: Get token usage (if available)
    usage = response.usage_metadata
    input_tokens = usage["input_tokens"]
    output_tokens = usage["output_tokens"]
    total_tokens = usage["total_tokens"]

    # Step 7: Put everything into a dictionary
    result = {
        "model": model_name,
        "question": question,
        "answer": response.content,
        "time_taken_seconds": round(time_taken, 2),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens
    }

    return result