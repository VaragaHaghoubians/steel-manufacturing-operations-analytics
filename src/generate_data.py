"""Seeded six-month machine-shift simulation of steel fabrication operations."""
from pathlib import Path
import numpy as np
import pandas as pd

# Machine, process, ideal cycle seconds. Values are illustrative, not OEM specs.
MACHINES = [
    ('PRESS_600T', 'Pressing', 28), ('PRESS_60T', 'Pressing', 36),
    ('WELD_01', 'Spot Welding', 65), ('WELD_10HEAD', 'Spot Welding', 45),
    ('LATHE_01', 'Machining', 34), ('INSPECT_01', 'Inspection', 20),
    ('PACK_01', 'Packaging', 25)]
REASONS = ['Tool change', 'Machine failure', 'Material shortage', 'Maintenance',
           'Quality issue', 'Operator waiting']
DEFECTS = {'Pressing': 'Press deformation', 'Spot Welding': 'Welding defect',
           'Machining': 'Dimensional defect', 'Inspection': 'Surface defect',
           'Packaging': 'Scratch'}

def generate_data(days=180, seed=42):
    if days <= 0:
        raise ValueError('days must be positive')
    # A seed makes the random example repeatable when you run it again.
    rng = np.random.default_rng(seed)
    rows = []
    for day in pd.date_range('2025-01-01', periods=days):
        for shift in ['Morning', 'Afternoon', 'Night']:
            # Same product mix across stations in a date/shift, not linked part genealogy.
            product = rng.choice(['Bracket', 'Housing', 'Support'])
            factor = {'Bracket': 1., 'Housing': 1.2, 'Support': .9}[product]
            for machine, operation, base in MACHINES:
                ideal = base * factor
                setup = int(rng.integers(10, 36))
                downtime = int(rng.integers(5, 56)) + (20 if machine == 'PRESS_600T' else 0)
                # Remove setup and other stops from planned production time.
                runtime = 450 - setup - downtime
                # Welding is intentionally modeled with greater speed loss.
                speed_loss = rng.uniform(.12, .32) if operation == 'Spot Welding' else rng.uniform(.02, .16)
                speed_loss += rng.uniform(.02, .14) if shift == 'Night' else 0
                cycle = ideal * (1 + speed_loss)
                # Convert minutes to seconds, then divide by seconds per unit.
                actual = int(runtime * 60 / cycle)
                scrap_probability = rng.uniform(.01, .025) + (.035 if operation == 'Spot Welding' else 0)
                scrap_probability += .007 if shift == 'Night' else 0
                # Randomly mark some of the produced units as rejected.
                scrap = int(rng.binomial(actual, scrap_probability))
                # The example plan targets 85% of the ideal shift capacity.
                planned = int(450 * 60 / ideal * .85)
                weights = [3, 4 if machine == 'PRESS_600T' else 2, 3, 1, 1, 1]
                reason = rng.choice(REASONS, p=np.array(weights)/sum(weights))
                defect = DEFECTS[operation] if rng.random() < .8 else 'Other'
                rows.append(dict(date=day.strftime('%Y-%m-%d'), shift=shift,
                    machine_id=machine, operation=operation, product_type=product,
                    planned_quantity=planned, actual_quantity=actual, good_quantity=actual-scrap,
                    scrap_quantity=scrap, cycle_time_sec=round(cycle, 3),
                    ideal_cycle_time_sec=round(ideal, 3), planned_production_min=450,
                    setup_time_min=setup, downtime_min=downtime,
                    downtime_reason=reason, defect_type=defect if scrap else 'No scrap',
                    material_batch=f'B{day.dayofyear:03d}',
                    steel_grade={'Bracket':'S235','Housing':'S355','Support':'S275'}[product],
                    operator_team={'Morning':'Team A','Afternoon':'Team B','Night':'Team C'}[shift]))
    return pd.DataFrame(rows)

if __name__ == '__main__':
    output = Path(__file__).resolve().parents[1] / 'data/raw/manufacturing_data.csv'
    output.parent.mkdir(parents=True, exist_ok=True)
    generate_data().to_csv(output, index=False)
    print('Saved the example manufacturing CSV.')
