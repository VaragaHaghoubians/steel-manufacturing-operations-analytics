"""A few simple checks: known-answer math and invalid-data handling."""
import sys
import unittest
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from generate_data import generate_data
from cleaning import clean_data
from kpi import summarize, operation_capacity

class BasicChecks(unittest.TestCase):
    def test_worked_oee_example(self):
        # Same example as docs/kpi_examples.md, independent of generated values.
        row = pd.DataFrame([{'planned_production_min':100, 'runtime_min':80,
            'setup_time_min':10, 'downtime_min':10, 'planned_quantity':150,
            'actual_quantity':120, 'good_quantity':108, 'scrap_quantity':12,
            'ideal_cycle_time_sec':30, 'cycle_time_sec':40}])
        result = summarize(row)
        self.assertAlmostEqual(result['oee'], .54)
        self.assertAlmostEqual(result['production_attainment'], .8)
        self.assertAlmostEqual(result['scrap_rate'], .1)

    def test_reproducible_and_valid_data(self):
        raw = generate_data(days=2, seed=42)
        pd.testing.assert_frame_equal(raw, generate_data(days=2, seed=42))
        clean = clean_data(raw)
        self.assertEqual(len(clean), 42)
        bad = raw.copy()
        bad.loc[0, 'good_quantity'] = 999999
        with self.assertRaises(ValueError):
            clean_data(bad)
        with self.assertRaises(ValueError):
            clean_data(pd.concat([raw, raw.iloc[:1]]))

    def test_parallel_welding_machines_are_added(self):
        clean = clean_data(generate_data(days=2))
        welding = clean[clean.operation == 'Spot Welding']
        expected = welding.good_quantity.sum() / 6 / 7.5
        rates = operation_capacity(clean).set_index('operation')
        self.assertAlmostEqual(rates.loc['Spot Welding','mean_good_units_per_scheduled_hour'], expected)

if __name__ == '__main__':
    unittest.main()
