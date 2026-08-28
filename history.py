# history.py
# Saves benchmark runs over time and builds a leaderboard from them.

import json
import os
from datetime import datetime


def load_history(file_name):
    """Loads past runs from a JSON file. Returns an empty list if none exist yet."""
    if not os.path.exists(file_name):
        return []
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


def save_run_to_history(file_name, results):
    """Appends this run's results to the history file, tagged with a timestamp."""
    history = load_history(file_name)

    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": results,
    })

    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)


def build_leaderboard(history):
    """
    Combines every past run into one leaderboard: for each model,
    the average speed, average tokens/sec, average cost, and how
    many answers we've recorded for it in total.
    """

    model_stats = {}

    for run_entry in history:
        for result in run_entry["results"]:
            if result.get("error"):
                continue  # skip failed calls

            model_name = result["model"]
            if model_name not in model_stats:
                model_stats[model_name] = {"times": [], "tps": [], "costs": [], "count": 0}

            model_stats[model_name]["times"].append(result["time_taken_seconds"])
            model_stats[model_name]["tps"].append(result["tokens_per_second"])
            if result.get("cost_usd") is not None:
                model_stats[model_name]["costs"].append(result["cost_usd"])
            model_stats[model_name]["count"] += 1

    leaderboard = []
    for model_name, stats in model_stats.items():
        leaderboard.append({
            "model": model_name,
            "avg_time_seconds": round(sum(stats["times"]) / len(stats["times"]), 2),
            "avg_tokens_per_second": round(sum(stats["tps"]) / len(stats["tps"]), 2),
            "avg_cost_usd": round(sum(stats["costs"]) / len(stats["costs"]), 6) if stats["costs"] else None,
            "total_answers_recorded": stats["count"],
        })

    leaderboard.sort(key=lambda x: x["avg_time_seconds"])
    return leaderboard