# display_table.py
# This file contains the logic for printing a comparison table.


def print_comparison_table(results):
    """
    This function takes the list of result dictionaries
    and prints them in a neat table format.
    """

    print("\n===== COMPARISON TABLE =====")

    # Step 1: Print the header row
    print(f"{'Model':<25} {'Time (s)':<10} {'Input Tok':<12} {'Output Tok':<12} {'Total Tok':<10}")
    print("-" * 75)

    # Step 2: Print one row per model
    for row in results:
        print(f"{row['model']:<25} {row['time_taken_seconds']:<10} {row['input_tokens']:<12} {row['output_tokens']:<12} {row['total_tokens']:<10}")

    print("-" * 75)