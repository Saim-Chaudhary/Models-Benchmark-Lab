# report.py
# Builds a readable Markdown report from a benchmark run.

from datetime import datetime


def build_markdown_report(results, questions):
    lines = []
    lines.append("# Benchmark Report")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"\nQuestions tested: {len(questions)}\n")

    for question in questions:
        lines.append(f"## Question: {question}\n")
        lines.append("| Model | Time (s) | Tokens/sec | Total Tokens | Cost (USD) |")
        lines.append("|---|---|---|---|---|")

        question_results = [r for r in results if r["question"] == question and not r.get("error")]

        for r in question_results:
            cost_display = f"${r['cost_usd']:.6f}" if r.get("cost_usd") is not None else "N/A"
            lines.append(
                f"| {r['model']} | {r['time_taken_seconds']} | {r['tokens_per_second']} | "
                f"{r['total_tokens']} | {cost_display} |"
            )

        lines.append("")
        for r in question_results:
            lines.append(f"**{r['model']} answer:**\n")
            lines.append(f"> {r['answer']}\n")

    return "\n".join(lines)