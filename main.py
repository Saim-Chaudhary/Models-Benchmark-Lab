# main.py
# This is the main file we run. It brings everything together.

from config import CSV_FILE_NAME
from benchmark import run_model
from save_results import save_to_csv
from display_table import print_comparison_table
from get_user_input import get_provider, get_api_key, get_model_list, get_question

# Step 1: Get provider, API key, models, and question from the user
provider = get_provider()
api_key = get_api_key()
models_to_test = get_model_list()
question = get_question()

# Step 2: Empty list to store results
results = []

# Step 3: Loop through each selected model and test it
for model_name in models_to_test:
    print("-----------------------------------")
    print(f"Model: {model_name}")

    # Call our function from benchmark.py
    result = run_model(model_name, question, api_key, provider)

    # Print the result nicely
    print("Answer:", result["answer"])
    print(f"Time taken: {result['time_taken_seconds']} seconds")
    print(f"Input tokens: {result['input_tokens']}, Output tokens: {result['output_tokens']}, Total tokens: {result['total_tokens']}")

    # Add this result to our list
    results.append(result)

print("-----------------------------------")
print("Done testing all models.")

# Step 4: Save all results using our function from save_results.py
save_to_csv(results, CSV_FILE_NAME)

# Step 5: Print a nice comparison table
print_comparison_table(results)