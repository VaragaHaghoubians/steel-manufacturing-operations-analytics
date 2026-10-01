"""Normalize harmless formatting; reject invalid or ambiguous observations."""
import numpy as np
import pandas as pd

COUNTS = ['planned_quantity','actual_quantity','good_quantity','scrap_quantity']
NUMERIC = COUNTS + ['cycle_time_sec','ideal_cycle_time_sec','planned_production_min',
                   'setup_time_min','downtime_min']
TEXT = ['shift','machine_id','operation','product_type','downtime_reason','defect_type',
        'material_batch','steel_grade','operator_team']
REQUIRED = ['date'] + TEXT + NUMERIC

def clean_data(raw):
    frame = raw.copy()
    missing = set(REQUIRED) - set(frame.columns)
    if missing:
        raise ValueError(f'Missing columns: {sorted(missing)}')
    if frame.empty or frame[REQUIRED].isna().any().any():
        raise ValueError('Empty dataset or missing required values')
    for col in TEXT:
        frame[col] = frame[col].astype(str).str.strip()
        if frame[col].eq('').any():
            raise ValueError(f'Blank category in {col}')
    frame['date'] = pd.to_datetime(frame['date'], format='%Y-%m-%d', errors='raise')
    if frame.duplicated(['date','shift','machine_id']).any():
        raise ValueError('Duplicate date/shift/machine observation')
    for col in NUMERIC:
        frame[col] = pd.to_numeric(frame[col], errors='raise')
        if not np.isfinite(frame[col]).all() or frame[col].lt(0).any():
            raise ValueError(f'Invalid values in {col}')
    for col in COUNTS:
        if frame[col].mod(1).ne(0).any():
            raise ValueError('Unit quantities must be integers')
    if frame[['planned_quantity','planned_production_min','ideal_cycle_time_sec','cycle_time_sec']].le(0).any().any():
        raise ValueError('Plans and cycle times must be positive')
    if (frame['actual_quantity'] != frame['good_quantity']+frame['scrap_quantity']).any():
        raise ValueError('Actual must equal good plus scrap')
    frame['runtime_min'] = frame['planned_production_min']-frame['setup_time_min']-frame['downtime_min']
    if frame['runtime_min'].lt(0).any():
        raise ValueError('Setup plus downtime exceeds planned production time')
    if (frame['actual_quantity']*frame['ideal_cycle_time_sec'] > frame['runtime_min']*60 + .01).any():
        raise ValueError('Output exceeds ideal runtime capacity')
    frame['week_start'] = frame['date']-pd.to_timedelta(frame['date'].dt.dayofweek, unit='D')
    return frame.sort_values(['date','shift','machine_id']).reset_index(drop=True)
