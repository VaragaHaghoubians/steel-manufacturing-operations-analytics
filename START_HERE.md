# Start here: beginner learning path

This is a junior data analyst portfolio project. The goal is to understand the work,
explain the choices, and practice Python with a familiar manufacturing example.
It is not necessary to present yourself as an expert or claim real factory savings.

## First run

Open PowerShell in the extracted project folder:
```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\src\main.py
Start-Process .\reports\manufacturing_summary.pdf
```
A virtual environment is simply a separate folder for this project's Python libraries.
These commands use its Python directly, so you do not need to activate it.

## Learn in this order

1. Read README.md and understand what one data row means.
2. Open data/raw/manufacturing_data.csv in Excel and inspect ten rows.
3. Work through notebook 01, then 02. Practice `head`, `groupby` and column arithmetic.
4. Read docs/kpi_examples.md and calculate each example with a calculator.
5. Work through notebooks 03–06. Change one filter and explain the new result.
6. Read notebook 07 and explain one finding and one limitation in your own words.
7. Read docs/interview_questions.md before adding this project to your CV.

## What each script does

| File | Simple explanation |
|---|---|
| src/generate_data.py | Makes example factory data using repeatable random numbers |
| src/cleaning.py | Checks the numbers and adds runtime and week columns |
| src/kpi.py | Calculates production, scrap and OEE measures |
| src/visualization.py | Draws four charts |
| src/reporting.py | Formats findings into a PDF and Markdown summary |
| src/main.py | Runs these steps in order |

Reporting code is supporting code. Focus your interview explanation on the dataset,
cleaning, KPI formulas and charts. Do not claim you can explain every library's internals.

## Small practice tasks

- Filter the clean data to PRESS_600T and calculate its scrap rate.
- Compare Morning and Night availability using summed minutes.
- Change DAYS in src/main.py to 30 and run again. Explain why totals change.
- Change SEED to 7. Explain why results change but formulas stay the same.
- Change it back to DAYS = 180 and SEED = 42 before publishing the default version.

## Honest presentation

If you used AI help, explain that you used it to build and understand the project and
checked the calculations yourself. Say what you understand and what you are still learning.
Keep this project separate from your employment history.
