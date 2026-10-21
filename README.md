# <Your product name>

> Fill this top section from your Examate project card on Day 1. Replace every line in angle brackets.

## Problem
Drivers in Tamil Nadu see old fine charts on social media and argue with traffic officers, because the Motor Vehicles Act has been amended many times, with a big penalty increase in 2019 and later changes. States also set their own compounding amounts. Driving school instructors who help learners, lorry drivers and auto drivers with challans cannot easily find the rule as it stood on the date of the offence. FineLine stores every section as dated versions and gives the correct rule and penalty for the challan date, in Tamil or English, with a citation and a diff of what changed.

## Who it is for
1. Driving school instructor in Salem who teaches learners and helps lorry and auto drivers understand the challans they received.
2. Lorry and auto drivers who want to check whether a challan amount matches the rule in force on the offence date.

## Signature feature
Challan checker: the user enters the offence and the challan date. FineLine shows the section, the penalty in force on that date, and what changed since.

## Hardest problem (my interview story)
Versioning: latest valid version. The Motor Vehicles Act was amended several times, so one section can have different penalties at different dates. I store each section as versions with valid_from and valid_to dates taken from the amending Acts. A question like "fine for no helmet in March 2019" must return a different, correctly dated answer than "in 2026". The retriever filters by the effective date before searching, and a diff view shows exactly how a penalty section changed across amendments. I will measure it as version accuracy on 150 date-specific penalty questions, with a target of 97%+.

## Dataset
| Source | Link | Documents | Pages | Licence / terms |
|---|---|---|---|---|
| Motor Vehicles Act 1988 with all amending Acts, and Central Motor Vehicles Rules (India Code) | https://www.indiacode.nic.in/handle/123456789/1798 | [fill after download] | [fill] | Government of India public documents, check site terms |
| Tamil Nadu Transport Department policy notes | [] | [fill] | [fill] | Government publication, check site terms |
| MoRTH "Road Accidents in India" reports 2015-2024 | [] | 10 reports | [fill] | Government publication, check site terms |
| **Target total** | | | **2,500+ pages** | |

## 10 real questions
See [docs/QUESTIONS.md](docs/QUESTIONS.md).

## Run it
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env                                 # Windows: copy .env.example .env
uvicorn app.main:app --reload
curl localhost:8000/health
```

## Live link
<Added in Week 2>
