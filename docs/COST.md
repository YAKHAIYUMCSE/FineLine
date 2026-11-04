# Cost of one question (Week 2)

Measured on 3 Nov 2026 with the real model, not the fake one.

## Model and prices

- Model: `gemini-3.6-flash` (Gemini API, OpenAI-compatible endpoint)
- Pricing page: https://aistudio.google.com/docs/pricing#gemini-3.6-flash (read on 3 Nov 2026)
- Paid-tier list prices per 1M tokens, Standard: input $0.75 and output $3.75 through 31 Dec 2026;
  input $1.50 and output $7.50 from 1 Jan 2027 (output includes thinking tokens).
- My calls used the free tier, so I paid nothing. The costs below are what the same calls would cost at list price.
- Fallback model for outages: Groq `openai/gpt-oss-20b` (not used in this run).

## Method

`tools/run_questions.py` sends the 10 questions from `docs/QUESTIONS.md` to `POST /chat` and reads the
tokens and cost from each call's `event: done`. Per-question results are in `docs/cost_run.csv`.
The app logs every call to `logs/cost.jsonl` and `GET /usage` totals them per day.

## Results (10 of 10 calls succeeded)

| Measure | Value |
|---|---|
| Average input tokens | 26.0 |
| Average output tokens | 532.2 |
| Average cost per question | $0.002015 |
| Cost per 1,000 questions | $2.0152 |
| Estimated token counts used | No (the provider reported usage) |

Output tokens were about 99% of the cost. The longest answer (Q6, seat belt) used 2,048 output tokens.
Calls took between 11 and 41 seconds.

## What this does not show yet

- No documents were sent, so input tokens are tiny. From Week 3 every question carries retrieved chunks,
  so input cost will rise. I will measure again after Week 3.
- The answers come from the model's memory, with no citations and no check that they are correct.
  This run measures cost only, not accuracy.
- From 1 Jan 2027 the list prices double, so the same traffic would cost about twice as much.
- Estimates are not bills. These are provider-reported tokens multiplied by list prices.

## One way to cut the cost

Cap the answer length. Output is 99% of the bill, so I will ask the model for a short answer that names the
section, the fine and the citation, and set a maximum number of output tokens on the request. In Week 3, sending
about 4 good chunks instead of 10 will also keep input tokens down.
