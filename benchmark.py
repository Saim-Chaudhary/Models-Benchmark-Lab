# benchmark.py
# Calls a model (possibly multiple times) and returns a full benchmark result.

from langchain.chat_models import init_chat_model
import time

from text_utils import split_reasoning_and_answer, estimate_token_split
from cost import calculate_cost


def call_model_once(model_name, question, api_key, provider):
    """Sends ONE question to ONE model, ONE time. No averaging here."""

    model = init_chat_model(model_name, model_provider=provider, api_key=api_key)

    start_time = time.time()
    response = model.invoke(question)
    end_time = time.time()

    usage = response.usage_metadata

    return {
        "raw_answer": response.content,
        "time_taken_seconds": end_time - start_time,
        "input_tokens": usage["input_tokens"],
        "output_tokens": usage["output_tokens"],
        "total_tokens": usage["total_tokens"],
    }


def run_model(model_name, question, api_key, provider, num_runs=1, pricing_table=None):
    """
    Runs a model against a question 'num_runs' times, averages the results,
    and enriches them with tokens/sec, cost, and reasoning/answer separation.

    pricing_table is optional and comes from the user (see cost.py) —
    we never hardcode prices, since they vary by provider and change over time.
    """

    if pricing_table is None:
        pricing_table = {}

    run_records = [call_model_once(model_name, question, api_key, provider) for _ in range(num_runs)]

    avg_time = sum(r["time_taken_seconds"] for r in run_records) / num_runs
    avg_input_tokens = sum(r["input_tokens"] for r in run_records) / num_runs
    avg_output_tokens = sum(r["output_tokens"] for r in run_records) / num_runs
    avg_total_tokens = sum(r["total_tokens"] for r in run_records) / num_runs

    # Use the last run's actual text to show the user
    last_answer_raw = run_records[-1]["raw_answer"]
    split_result = split_reasoning_and_answer(last_answer_raw)

    reasoning_tokens_est, answer_tokens_est = estimate_token_split(
        split_result["reasoning"], split_result["answer"], avg_output_tokens
    )

    tokens_per_second = round(avg_output_tokens / avg_time, 2) if avg_time > 0 else 0
    cost_usd = calculate_cost(model_name, avg_input_tokens, avg_output_tokens, pricing_table)

    return {
        "model": model_name,
        "question": question,
        "answer": split_result["answer"],
        "reasoning": split_result["reasoning"],
        "has_reasoning": split_result["has_reasoning"],
        "time_taken_seconds": round(avg_time, 2),
        "input_tokens": round(avg_input_tokens),
        "output_tokens": round(avg_output_tokens),
        "total_tokens": round(avg_total_tokens),
        "reasoning_tokens_est": reasoning_tokens_est,
        "answer_tokens_est": answer_tokens_est,
        "tokens_per_second": tokens_per_second,
        "cost_usd": cost_usd,
        "num_runs": num_runs,
        "error": False,
    }