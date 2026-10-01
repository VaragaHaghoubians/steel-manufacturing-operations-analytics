# Validation notes

Verified on October 1, 2026 using Python 3.12.10 on Windows.

- Default script ran successfully and generated 3,780 unique observations.
- Actual quantity equals good plus scrap for every row.
- Runtime plus setup plus downtime equals planned time for every row.
- Production attainment reconciles to the raw quantity totals.
- All seven notebooks executed successfully, with outputs included.
- All three basic checks passed: the worked KPI example, reproducible/valid data,
  and adding the parallel welding machines before comparing operation capacity.
- The Excel workbook was reopened and its Clean Data sheet contains 3,780 rows.
- The one-page PDF and all four chart images were visually inspected.
- Python dependency checks reported no broken requirements.
- Python source files compiled; the ZIP file passed its integrity check.

Run the checks yourself from the repository folder:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Only Python 3.12 was tested here. Requirements allow compatible versions; exact synthetic
results may vary if NumPy's random implementation changes. Seed 42 reproduces the included
data in the tested environment. Version ranges are provided so learners can install
compatible libraries without maintaining a complex environment specification.

## Tested library versions

| Library | Version |
|---|---|
| pandas | 3.0.6 |
| numpy | 2.5.3 |
| matplotlib | 3.11.2 |
| openpyxl | 3.1.5 |
| reportlab | 5.0.1 |
| nbformat | 5.11.1 |
| nbconvert | 7.17.1 |
| ipykernel | 7.4.0 |
