# save_results.py
# This file contains the logic for saving results to a CSV file.

import csv


def save_to_csv(results, file_name):
    """
    This function takes a list of result dictionaries
    and writes them into a CSV file.
    """

    # Step 1: Define the column names (must match the keys in our dictionaries)
    fieldnames = [
        "model",
        "question",
        "answer",
        "time_taken_seconds",
        "input_tokens",
        "output_tokens",
        "total_tokens"
    ]

    # Step 2: Open the file and write the data
    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Results saved to {file_name}")