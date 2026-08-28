# text_utils.py
# Helpers for handling reasoning-model outputs (models that show their <think> steps)

import re


def split_reasoning_and_answer(raw_text):
    """
    Some models (like Qwen) wrap their step-by-step thinking inside
    <think>...</think> tags before giving the real answer.
    This function separates the thinking from the final answer.
    """

    think_match = re.search(r"<think>(.*?)</think>", raw_text, re.DOTALL)

    if think_match:
        reasoning_text = think_match.group(1).strip()
        answer_text = raw_text.replace(think_match.group(0), "").strip()
        return {"reasoning": reasoning_text, "answer": answer_text, "has_reasoning": True}
    else:
        return {"reasoning": "", "answer": raw_text.strip(), "has_reasoning": False}


def estimate_token_split(reasoning_text, answer_text, total_output_tokens):
    """
    IMPORTANT: The API only gives us ONE combined output_tokens number.
    It does NOT tell us exactly how many tokens were reasoning vs answer.
    This function ESTIMATES the split based on text length (characters).
    Treat this as an approximation, not an exact measurement.
    """

    reasoning_chars = len(reasoning_text)
    answer_chars = len(answer_text)
    total_chars = reasoning_chars + answer_chars

    if total_chars == 0:
        return 0, 0

    reasoning_tokens_estimate = round((reasoning_chars / total_chars) * total_output_tokens)
    answer_tokens_estimate = total_output_tokens - reasoning_tokens_estimate

    return reasoning_tokens_estimate, answer_tokens_estimate