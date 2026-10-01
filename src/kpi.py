"""Pooled production, quality and time metrics; no unweighted OEE averaging."""
import pandas as pd

def ratio(numerator, denominator):
    # Avoid dividing by zero. None means this measure cannot be calculated.
    if denominator == 0:
        return None
    return float(numerator / denominator)

def summarize(frame):
    # Add the quantities and times before dividing.
    planned = float(frame['planned_production_min'].sum())
    runtime = float(frame['runtime_min'].sum())
    actual = int(frame['actual_quantity'].sum())
    good = int(frame['good_quantity'].sum())
    # How long the actual output would take at ideal speed.
    ideal_minutes = float((frame['actual_quantity']*frame['ideal_cycle_time_sec']/60).sum())
    availability = ratio(runtime, planned)
    performance = ratio(ideal_minutes, runtime)
    quality = ratio(good, actual)
    if availability is None or performance is None or quality is None:
        oee = None
    else:
        oee = availability * performance * quality
    return dict(planned_quantity=int(frame['planned_quantity'].sum()), actual_quantity=actual,
        good_quantity=good, scrap_quantity=int(frame['scrap_quantity'].sum()),
        production_attainment=ratio(actual, frame['planned_quantity'].sum()),
        scrap_rate=ratio(frame['scrap_quantity'].sum(), actual),
        planned_production_min=planned, runtime_min=runtime,
        setup_time_min=float(frame['setup_time_min'].sum()), downtime_min=float(frame['downtime_min'].sum()),
        availability=availability, performance=performance, quality=quality,
        oee=oee,
        weighted_cycle_time_sec=ratio((frame['cycle_time_sec']*frame['actual_quantity']).sum(), actual),
        actual_units_per_runtime_hour=ratio(actual, runtime/60),
        good_units_per_planned_machine_hour=ratio(good, planned/60))

# Example: grouped(clean, 'shift') returns one KPI row for each shift.
def grouped(frame, column):
    records = []
    for key, group in frame.groupby(column, sort=True):
        row = summarize(group)
        row[column] = key
        records.append(row)
    return pd.DataFrame(records)

# Sort biggest losses first, then add their percentage shares cumulatively.
def pareto(frame, category, weight):
    result = frame.groupby(category)[weight].sum().sort_values(ascending=False).reset_index()
    total = result[weight].sum()
    result['share'] = result[weight]/total if total else 0.
    result['cumulative_share'] = result['share'].cumsum()
    return result

def operation_capacity(frame):
    # Parallel machines are summed first for each date/shift/operation.
    observations = frame.groupby(['date','shift','operation'], as_index=False).agg(
        good_quantity=('good_quantity','sum'), actual_quantity=('actual_quantity','sum'))
    result = observations.groupby('operation').agg(mean_good_units_per_shift=('good_quantity','mean'),
        mean_actual_units_per_shift=('actual_quantity','mean')).reset_index()
    # Standard 450-minute shift in this simulator only.
    result['mean_good_units_per_scheduled_hour'] = result['mean_good_units_per_shift']/7.5
    return result.sort_values('mean_good_units_per_scheduled_hour')
