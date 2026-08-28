# config.py

# Ready-made test suites so users can benchmark against a real task type
PRESET_SUITES = {
    "Factual Q&A": [
        "What is the capital of France?",
        "Who wrote the play Romeo and Juliet?",
        "What is the boiling point of water in Celsius?",
    ],
    "Math": [
        "What is 47 times 36?",
        "If a train travels 60 miles in 45 minutes, what is its speed in mph?",
        "What is the square root of 144?",
    ],
    "Coding": [
        "Write a Python function that checks if a number is prime.",
        "What does the 'self' keyword mean in Python classes?",
        "Explain the difference between a list and a tuple in Python.",
    ],
    "Reasoning": [
        "If all cats are animals, and some animals are pets, can we conclude all cats are pets? Explain.",
        "A farmer has 17 sheep, all but 9 die. How many are left?",
    ],
    "Creative Writing": [
        "Write a two-line poem about the ocean.",
        "Write a one-sentence story about a robot learning to paint.",
    ],
}

CSV_FILE_NAME = "benchmark_results.csv"
HISTORY_FILE_NAME = "benchmark_history.json"