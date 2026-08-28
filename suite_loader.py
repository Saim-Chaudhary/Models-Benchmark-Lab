# suite_loader.py
# Reads a user-uploaded CSV or JSON file and turns it into a list of questions.

import csv
import json
import io


def load_questions_from_upload(uploaded_file):
    """
    Supports:
    - JSON file: either a list of strings, or a list of {"question": "..."} objects
    - CSV file: must have a column named "question"
    """

    file_name = uploaded_file.name.lower()
    content = uploaded_file.read().decode("utf-8")

    questions = []

    if file_name.endswith(".json"):
        data = json.loads(content)
        for item in data:
            if isinstance(item, str):
                questions.append(item)
            elif isinstance(item, dict) and "question" in item:
                questions.append(item["question"])

    elif file_name.endswith(".csv"):
        reader = csv.DictReader(io.StringIO(content))
        for row in reader:
            if "question" in row and row["question"].strip() != "":
                questions.append(row["question"].strip())

    return questions