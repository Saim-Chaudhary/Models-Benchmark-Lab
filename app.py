# app.py
# Streamlit UI for the Open-Source Model Benchmark Lab.

import streamlit as st
import csv
import io
import os
import time

from benchmark import run_model
from config import PRESET_SUITES, HISTORY_FILE_NAME
from suite_loader import load_questions_from_upload
from history import load_history, save_run_to_history, build_leaderboard
from report import build_markdown_report

# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------
st.set_page_config(page_title="OSS Bench — Model Benchmark Lab", page_icon="◆", layout="wide")

# ---------------------------------------------------------
# STYLE
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --canvas: #14161A; --surface-1: #1C1F26; --surface-2: #23262E;
    --text-primary: #F4F1EA; --text-secondary: #A9ACB8; --text-muted: #6B6E78;
    --border-subtle: #2E3138; --border-strong: #3D414B;
    --action-primary: #FF8A3D; --action-primary-hover: #FFA35E;
    --status-success: #59D499; --status-danger: #FF5D5D; --accent-support: #7FE7C4;
}
.stApp {
    background-color: var(--canvas);
    background-image:
        repeating-linear-gradient(0deg, rgba(255,255,255,0.02) 0px, rgba(255,255,255,0.02) 1px, transparent 1px, transparent 48px),
        repeating-linear-gradient(90deg, rgba(255,255,255,0.02) 0px, rgba(255,255,255,0.02) 1px, transparent 1px, transparent 48px);
    font-family: 'Space Grotesk', sans-serif;
    color: var(--text-primary);
}
footer { visibility: hidden; }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; letter-spacing: -0.01em; }

.wordmark { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; letter-spacing: 0.18em; color: var(--action-primary); text-transform: uppercase; }
.mono { font-family: 'JetBrains Mono', monospace; }

div[data-testid="stVerticalBlockBorderWrapper"] { background-color: var(--surface-1); border: 1px solid var(--border-subtle) !important; border-radius: 10px; padding: 4px; }

div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea, div[data-baseweb="select"] > div {
    background-color: var(--surface-2) !important; border: 1px solid var(--border-subtle) !important;
    color: var(--text-primary) !important; border-radius: 6px !important; font-family: 'JetBrains Mono', monospace;
}
div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--action-primary) !important; box-shadow: 0 0 0 1px var(--action-primary) !important;
}

div[data-testid="stButton"] button {
    background-color: var(--action-primary); color: var(--canvas); border: none; font-weight: 600;
    letter-spacing: 0.04em; text-transform: uppercase; font-size: 0.82rem; border-radius: 6px;
    padding: 0.6rem 1rem; transition: background-color 150ms ease;
}
div[data-testid="stButton"] button:hover { background-color: var(--action-primary-hover); color: var(--canvas); }

/* Section labels */
.eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.25rem; }
.subeyebrow { font-family: 'JetBrains Mono', monospace; font-size: 0.66rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); margin-top: 14px; margin-bottom: 2px; }
.divider { border-top: 1px solid var(--border-subtle); margin: 14px 0; }

/* Tick ruler above signal bars */
.ruler { display: flex; justify-content: space-between; padding: 0 2px; margin: 4px 0 8px 0; }
.ruler span { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: var(--text-muted); text-align: center; }
.ruler span::before { content: ''; display: block; width: 1px; height: 6px; background: var(--border-strong); margin: 0 auto 4px auto; }

/* Channel card */
.channel { border: 1px solid var(--border-subtle); border-radius: 8px; padding: 14px 16px; margin-bottom: 10px; background-color: var(--surface-2); transition: border-color 150ms ease; }
.channel:hover { border-color: var(--border-strong); }
.channel-error { border-color: var(--status-danger); }
.channel-head { display: flex; align-items: baseline; justify-content: space-between; flex-wrap: wrap; gap: 6px; }
.channel-id { font-family: 'JetBrains Mono', monospace; color: var(--action-primary); font-size: 0.75rem; letter-spacing: 0.08em; }
.channel-name { font-family: 'JetBrains Mono', monospace; font-weight: 600; font-size: 0.95rem; color: var(--text-primary); word-break: break-word; }
.channel-time { font-family: 'JetBrains Mono', monospace; color: var(--text-secondary); font-size: 0.85rem; }

/* Winner badges */
.badge { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 0.06em; padding: 2px 6px; border-radius: 3px; text-transform: uppercase; margin-left: 6px; }
.badge-fastest { background: rgba(255,138,61,0.15); color: var(--action-primary); border: 1px solid rgba(255,138,61,0.4); }
.badge-efficient { background: rgba(127,231,196,0.15); color: var(--accent-support); border: 1px solid rgba(127,231,196,0.4); }

.bar-track { width: 100%; height: 8px; background-color: var(--surface-1); border-radius: 4px; margin: 10px 0 8px 0; overflow: hidden; }
.bar-fill { height: 100%; background-color: var(--action-primary); border-radius: 4px; }

/* Token data chips */
.token-row { display: flex; gap: 8px; flex-wrap: wrap; }
.chip {
    font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; color: var(--text-secondary);
    background-color: var(--surface-1); border: 1px solid var(--border-subtle);
    border-radius: 4px; padding: 2px 8px;
}
.chip b { color: var(--text-primary); }

.idle-box { border: 1px dashed var(--border-strong); border-radius: 8px; padding: 40px 20px; text-align: center; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; }

.stat { text-align: center; padding: 10px 6px; }
.stat-label { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted); }
.stat-value { font-family: 'JetBrains Mono', monospace; font-size: 1.05rem; font-weight: 600; word-break: break-word; }
.stat-value.fastest { color: var(--action-primary); }
.stat-value.efficient { color: var(--accent-support); }
.stat-value.neutral { color: var(--text-primary); }

.build-tag { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: var(--text-muted); margin-top: 10px; letter-spacing: 0.06em; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
header_left, header_right = st.columns([3, 2])
with header_left:
    st.markdown('<div class="wordmark">◆ OSS BENCH</div>', unsafe_allow_html=True)
    st.markdown("## Open-Source Model Benchmark Lab")
with header_right:
    st.markdown(
        "<div style='text-align:right; color:#6B6E78; font-family:JetBrains Mono; font-size:0.75rem; margin-top:22px;'>"
        "Your API key is used only for this session.<br>It is never saved or sent anywhere else."
        "</div>", unsafe_allow_html=True
    )
st.write("")

# ---------------------------------------------------------
# SIDEBAR: connection + run settings (shared across everything)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="eyebrow">Connection</div>', unsafe_allow_html=True)
    provider = st.selectbox("Provider", options=["groq", "openai", "anthropic", "google_genai"])
    api_key = st.text_input("API key", type="password", placeholder="Paste your key here")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="eyebrow">Run Settings</div>', unsafe_allow_html=True)
    num_runs = st.slider(
        "Runs per question (averaged)", min_value=1, max_value=5, value=1,
        help="Running each question multiple times and averaging reduces noise from network/server variance."
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="build-tag">BUILD 0.4 · SIGNAL LAB</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TABS: Run Benchmark vs Leaderboard
# ---------------------------------------------------------
tab_run, tab_leaderboard = st.tabs(["🧪 Run Benchmark", "🏆 Leaderboard"])

# ===========================================================
# TAB 1: RUN BENCHMARK
# ===========================================================
with tab_run:
    config_col, results_col = st.columns([4, 7], gap="large")

    with config_col:
        with st.container(border=True):
            st.markdown('<div class="eyebrow">01 — Configure</div>', unsafe_allow_html=True)

            st.markdown('<div class="subeyebrow">Models</div>', unsafe_allow_html=True)
            models_raw = st.text_area(
                "Models to test (one per line)",
                placeholder="openai/gpt-oss-20b\nopenai/gpt-oss-120b\nqwen/qwen3.6-27b",
                height=100,
                label_visibility="collapsed",
            )

            raw_lines = models_raw.replace(",", "\n").split("\n")
            model_list = [m.strip() for m in raw_lines if m.strip() != ""]

            pricing_table = {}
            if model_list:
                with st.expander("Add pricing (optional — enables cost tracking)"):
                    st.caption("Leave at 0 if you don't know the price. Cost will show as 'n/a' for that model.")
                    for model_name in model_list:
                        p1, p2 = st.columns(2)
                        with p1:
                            input_price = st.number_input(
                                f"{model_name} — $/1M input",
                                min_value=0.0, value=0.0, step=0.01, key=f"in_{model_name}"
                            )
                        with p2:
                            output_price = st.number_input(
                                f"{model_name} — $/1M output",
                                min_value=0.0, value=0.0, step=0.01, key=f"out_{model_name}"
                            )
                        if input_price > 0 or output_price > 0:
                            pricing_table[model_name] = {"input": input_price, "output": output_price}

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="subeyebrow">Prompts</div>', unsafe_allow_html=True)

            question_source = st.radio(
                "Question source",
                ["Single question", "Preset test suite", "Type multiple questions", "Upload CSV/JSON"],
                label_visibility="collapsed",
            )

            questions_to_test = []

            if question_source == "Single question":
                q = st.text_area("Prompt", placeholder="What is the capital of France?", height=80)
                if q.strip():
                    questions_to_test = [q.strip()]

            elif question_source == "Preset test suite":
                suite_name = st.selectbox("Choose a suite", options=list(PRESET_SUITES.keys()))
                questions_to_test = PRESET_SUITES[suite_name]
                st.caption(f"{len(questions_to_test)} questions in this suite.")

            elif question_source == "Type multiple questions":
                raw = st.text_area("One question per line", height=120)
                questions_to_test = [q.strip() for q in raw.split("\n") if q.strip()]

            elif question_source == "Upload CSV/JSON":
                uploaded = st.file_uploader("Upload a .csv or .json file", type=["csv", "json"])
                if uploaded is not None:
                    questions_to_test = load_questions_from_upload(uploaded)
                    st.caption(f"Loaded {len(questions_to_test)} questions.")

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            run_clicked = st.button("Run Benchmark", use_container_width=True)

    with results_col:
        with st.container(border=True):
            st.markdown('<div class="eyebrow">02 — Signal Readout</div>', unsafe_allow_html=True)

            if not run_clicked:
                st.markdown(
                    '<div class="idle-box">// waiting for input<br>Configure a run on the left, then press RUN BENCHMARK</div>',
                    unsafe_allow_html=True
                )
            else:
                if not api_key:
                    st.error("Please enter an API key in the sidebar.")
                elif not model_list:
                    st.error("Please enter at least one model name.")
                elif not questions_to_test:
                    st.error("Please provide at least one question.")
                else:
                    all_results = []
                    overall_start = time.time()

                    for q_index, question_text in enumerate(questions_to_test):
                        with st.expander(f"Q{q_index+1}: {question_text}", expanded=(len(questions_to_test) == 1)):

                            question_results = []
                            for model_name in model_list:
                                try:
                                    result = run_model(
                                        model_name, question_text, api_key, provider,
                                        num_runs=num_runs, pricing_table=pricing_table
                                    )
                                except Exception as e:
                                    result = {
                                        "model": model_name, "question": question_text, "answer": "",
                                        "reasoning": "", "has_reasoning": False,
                                        "time_taken_seconds": 0, "input_tokens": 0, "output_tokens": 0,
                                        "total_tokens": 0, "reasoning_tokens_est": 0, "answer_tokens_est": 0,
                                        "tokens_per_second": 0, "cost_usd": None, "num_runs": num_runs,
                                        "error": True, "error_message": str(e),
                                    }
                                question_results.append(result)

                            all_results.extend(question_results)

                            successful = [r for r in question_results if not r["error"]]
                            max_time = max([r["time_taken_seconds"] for r in successful], default=1) or 1
                            fastest_model = min(successful, key=lambda r: r["time_taken_seconds"])["model"] if successful else None
                            efficient_model = min(successful, key=lambda r: r["total_tokens"])["model"] if successful else None

                            # ---- Tick ruler (signature element): shared time scale for this question ----
                            if successful:
                                ruler_html = '<div class="ruler">'
                                for fraction in [0, 0.25, 0.5, 0.75, 1.0]:
                                    ruler_html += f'<span>{round(max_time * fraction, 2)}s</span>'
                                ruler_html += '</div>'
                                st.markdown(ruler_html, unsafe_allow_html=True)

                            for i, r in enumerate(question_results):
                                if r["error"]:
                                    st.markdown(
                                        f'<div class="channel channel-error">'
                                        f'<div class="channel-head"><span class="channel-id">CH-{i+1:02d}</span> '
                                        f'<span class="channel-name">{r["model"]}</span></div>'
                                        f'<div style="color:#FF5D5D; font-family:JetBrains Mono; font-size:0.8rem; margin-top:8px;">⚠ {r["error_message"]}</div>'
                                        f'</div>', unsafe_allow_html=True
                                    )
                                    continue

                                bar_width = max(6, round((r["time_taken_seconds"] / max_time) * 100))
                                cost_display = f"${r['cost_usd']:.6f}" if r["cost_usd"] is not None else "n/a"
                                runs_note = f" (avg of {r['num_runs']})" if r["num_runs"] > 1 else ""

                                badges_html = ""
                                if r["model"] == fastest_model:
                                    badges_html += '<span class="badge badge-fastest">FASTEST</span>'
                                if r["model"] == efficient_model:
                                    badges_html += '<span class="badge badge-efficient">EFFICIENT</span>'

                                st.markdown(
                                    f'<div class="channel">'
                                    f'<div class="channel-head">'
                                    f'<span><span class="channel-id">CH-{i+1:02d}</span> <span class="channel-name">{r["model"]}</span>{badges_html}</span>'
                                    f'<span class="channel-time">{r["time_taken_seconds"]}s{runs_note}</span>'
                                    f'</div>'
                                    f'<div class="bar-track"><div class="bar-fill" style="width:{bar_width}%;"></div></div>'
                                    f'<div class="token-row">'
                                    f'<span class="chip">IN <b>{r["input_tokens"]}</b></span>'
                                    f'<span class="chip">OUT <b>{r["output_tokens"]}</b></span>'
                                    f'<span class="chip">TOK/SEC <b>{r["tokens_per_second"]}</b></span>'
                                    f'<span class="chip">COST <b>{cost_display}</b></span>'
                                    + (f'<span class="chip">THINK TOK (est) <b>{r["reasoning_tokens_est"]}</b></span>' if r["has_reasoning"] else '')
                                    + f'</div></div>', unsafe_allow_html=True
                                )

                                with st.expander(f"Show details — CH-{i+1:02d}"):
                                    if r["has_reasoning"]:
                                        st.caption("Reasoning (extracted from <think> tags):")
                                        st.text(r["reasoning"])
                                        st.caption("Final answer:")
                                    st.text(r["answer"])

                    overall_time = round(time.time() - overall_start, 2)

                    # ---- SAVE TO HISTORY (for the leaderboard tab) ----
                    save_run_to_history(HISTORY_FILE_NAME, all_results)

                    # ---- THIS RUN'S SUMMARY ----
                    st.write("")
                    st.markdown('<div class="eyebrow">This Run — Summary (averaged across all questions)</div>', unsafe_allow_html=True)
                    summary = build_leaderboard([{"results": all_results}])
                    st.dataframe(summary, use_container_width=True, hide_index=True)
                    st.caption(f"Total wall-clock time for this run: {overall_time}s")

                    # ---- EXPORTS ----
                    export_col1, export_col2 = st.columns(2)

                    with export_col1:
                        csv_buffer = io.StringIO()
                        fieldnames = ["model", "question", "answer", "time_taken_seconds", "input_tokens",
                                      "output_tokens", "total_tokens", "tokens_per_second", "cost_usd", "num_runs"]
                        writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
                        writer.writeheader()
                        for r in all_results:
                            if not r["error"]:
                                writer.writerow({k: r[k] for k in fieldnames})
                        st.download_button("Export CSV", data=csv_buffer.getvalue(),
                                            file_name="benchmark_results.csv", mime="text/csv",
                                            use_container_width=True)

                    with export_col2:
                        report_text = build_markdown_report(all_results, questions_to_test)
                        st.download_button("Export Markdown Report", data=report_text,
                                            file_name="benchmark_report.md", mime="text/markdown",
                                            use_container_width=True)

# ===========================================================
# TAB 2: LEADERBOARD
# ===========================================================
with tab_leaderboard:
    with st.container(border=True):
        st.markdown('<div class="eyebrow">All-Time Leaderboard</div>', unsafe_allow_html=True)

        history = load_history(HISTORY_FILE_NAME)

        if not history:
            st.markdown(
                '<div class="idle-box">// no history yet<br>Run a benchmark to start building your leaderboard</div>',
                unsafe_allow_html=True
            )
        else:
            leaderboard = build_leaderboard(history)
            st.dataframe(leaderboard, use_container_width=True, hide_index=True)

            st.write("")
            st.markdown('<div class="eyebrow">Average Speed by Model (seconds, lower is better)</div>', unsafe_allow_html=True)
            chart_data = {row["model"]: row["avg_time_seconds"] for row in leaderboard}
            st.bar_chart(chart_data)

            st.write("")
            if st.button("Clear History"):
                os.remove(HISTORY_FILE_NAME)
                st.rerun()