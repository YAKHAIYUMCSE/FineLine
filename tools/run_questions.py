"""Send the 10 README questions to a running /chat and record tokens and cost.

Usage: python tools/run_questions.py [base_url]
Writes docs/cost_run.csv and prints totals and averages.
"""
import csv
import json
import sys
import time

import httpx

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"

QUESTIONS = [
    "What is the penalty for driving without a licence today, and what was it before September 2019?",
    "Is a pillion rider without a helmet also fined?",
    "How many road accidents did Tamil Nadu record in 2024 compared with 2022?",
    "What was the fine for no helmet in March 2019 and what is it in 2026?",
    "Drunk driving fine 2019-ku munnadi evlo, ippo evlo?",
    "I got a challan for not wearing a seat belt. Which section applies and how much is the fine?",
    "What is the fine for using a mobile phone while driving?",
    "What is the fine for driving an overloaded lorry?",
    "How many people died in road accidents in Tamil Nadu in 2022?",
    "What will the traffic fine for no helmet be in 2030?",
]


def ask(client: httpx.Client, question: str) -> dict:
    body = {"messages": [{"role": "user", "content": question}]}
    start = time.perf_counter()
    answer_parts: list[str] = []
    done: dict = {}
    error = None
    event = None
    with client.stream("POST", f"{BASE}/chat", json=body, timeout=120) as response:
        for line in response.iter_lines():
            if line.startswith("event:"):
                event = line[len("event:"):].strip()
            elif line.startswith("data:"):
                data = json.loads(line[len("data:"):].strip())
                if event == "done":
                    done = data
                elif event == "error":
                    error = data.get("error")
                elif "delta" in data:
                    answer_parts.append(data["delta"])
            elif line == "":
                event = None
    usage = done.get("usage", {})
    return {
        "ok": error is None,
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
        "estimated": usage.get("estimated", False),
        "cost_usd": done.get("cost_usd", 0.0),
        "latency_s": round(time.perf_counter() - start, 2),
        "answer_chars": len("".join(answer_parts)),
        "error": (error or "")[:120],
    }


def main() -> None:
    rows = []
    with httpx.Client() as client:
        for number, question in enumerate(QUESTIONS, start=1):
            row = {"n": number, "question": question, **ask(client, question)}
            rows.append(row)
            print(
                f"Q{number}: ok={row['ok']} in={row['input_tokens']} "
                f"out={row['output_tokens']} cost={row['cost_usd']} "
                f"time={row['latency_s']}s {row['error']}"
            )
            time.sleep(2)  # stay polite to the free tier

    with open("docs/cost_run.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    good = [r for r in rows if r["ok"]]
    if not good:
        print("No successful calls: fix the errors above first.")
        return
    n = len(good)
    avg_in = sum(r["input_tokens"] for r in good) / n
    avg_out = sum(r["output_tokens"] for r in good) / n
    avg_cost = sum(r["cost_usd"] for r in good) / n
    print(f"\nSuccessful calls: {n} of {len(rows)}")
    print(f"Average input tokens: {avg_in:.1f}")
    print(f"Average output tokens: {avg_out:.1f}")
    print(f"Average cost per question: ${avg_cost:.6f}")
    print(f"Cost per 1,000 questions: ${avg_cost * 1000:.4f}")
    print(f"Any estimated token counts: {any(r['estimated'] for r in good)}")


if __name__ == "__main__":
    main()