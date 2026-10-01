"""Run the project. Read START_HERE.md before exploring the other scripts."""
from pathlib import Path
import json
import pandas as pd
from generate_data import generate_data
from cleaning import clean_data
from kpi import summarize, grouped, pareto, operation_capacity
from visualization import create_figures
from reporting import management_findings, write_reports

# You can change these two values and run the script again.
DAYS = 180
SEED = 42
ROOT = Path(__file__).resolve().parents[1]

def run_project(root=ROOT, days=DAYS, seed=SEED):
    root = Path(root)
    raw_folder = root / 'data/raw'
    clean_folder = root / 'data/processed'
    report_folder = root / 'reports'
    for folder in [raw_folder, clean_folder, report_folder]:
        folder.mkdir(parents=True, exist_ok=True)

    # Step 1: create the example data and save it as a CSV.
    raw = generate_data(days=days, seed=seed)
    raw.to_csv(raw_folder / 'manufacturing_data.csv', index=False)

    # Step 2: check the data and add runtime and week columns.
    clean = clean_data(raw)
    clean.to_csv(clean_folder / 'manufacturing_clean.csv', index=False, date_format='%Y-%m-%d')

    # Step 3: calculate KPIs for the whole dataset and each useful group.
    overall = summarize(clean)
    tables = {}
    for column in ['date','week_start','shift','machine_id','operation','product_type']:
        tables[column] = grouped(clean, column)
        tables[column].to_csv(clean_folder / f'kpis_by_{column}.csv', index=False)

    # Setup is separate from other downtime, so count it once as its own loss.
    losses = clean[['downtime_reason','downtime_min']].rename(columns={'downtime_min':'lost_time_min'})
    setup = pd.DataFrame({'downtime_reason':['Setup'], 'lost_time_min':[clean.setup_time_min.sum()]})
    downtime = pareto(pd.concat([losses, setup]), 'downtime_reason', 'lost_time_min')
    defects = pareto(clean[clean.scrap_quantity > 0], 'defect_type', 'scrap_quantity')
    capacity = operation_capacity(clean)
    downtime.to_csv(clean_folder / 'downtime_pareto.csv', index=False)
    defects.to_csv(clean_folder / 'scrap_pareto.csv', index=False)
    capacity.to_csv(clean_folder / 'operation_capacity.csv', index=False)

    # Step 4: create charts. Matplotlib draws and saves each chart as a PNG.
    create_figures(tables['machine_id'], tables['date'], downtime, defects, report_folder / 'figures')

    # Step 5: export to Excel and write a short management report.
    with pd.ExcelWriter(clean_folder / 'manufacturing_analytics.xlsx') as workbook:
        clean.to_excel(workbook, sheet_name='Clean Data', index=False)
        for column, table in tables.items():
            table.to_excel(workbook, sheet_name=column, index=False)
        capacity.to_excel(workbook, sheet_name='Capacity Screen', index=False)
    findings = management_findings(overall, tables['machine_id'], capacity, downtime, defects, tables['shift'])
    write_reports(root, overall, findings)
    results = {'data_type':'synthetic', 'seed':seed, 'observations':len(clean),
        'date_start':str(clean.date.min().date()), 'date_end':str(clean.date.max().date()),
        'overall':overall, 'findings':findings}
    (report_folder / 'metrics.json').write_text(json.dumps(results, indent=2, allow_nan=False), encoding='utf-8')
    return results

if __name__ == '__main__':
    results = run_project()
    print(f"Finished: {results['observations']:,} example rows.")
    print('Open reports/manufacturing_summary.pdf to see the results.')
