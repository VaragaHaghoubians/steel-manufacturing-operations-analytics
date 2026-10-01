# Dataset schema

Grain: date × shift × machine_id. Units represent process-stage completions.
Required fields are validated; no confidential data or operator names are used.

| Field | Unit / type | Meaning |
|---|---|---|
| date | ISO date | Production shift date |
| shift | category | Morning, Afternoon, Night |
| machine_id | text | One of seven illustrative machine identifiers |
| operation | category | Pressing, Spot Welding, Machining, Inspection, Packaging |
| product_type | category | Bracket, Housing, Support |
| planned_quantity | integer units | Target based on 85% of ideal planned-time capacity |
| actual_quantity | integer units | Gross process-stage completions |
| good_quantity | integer units | Accepted completions |
| scrap_quantity | integer units | Rejected completions |
| cycle_time_sec | seconds/unit | Modeled observed cycle time |
| ideal_cycle_time_sec | seconds/unit | Product-adjusted standard cycle time |
| planned_production_min | minutes | Planned machine-shift time, excludes breaks |
| setup_time_min | minutes | Setup within planned time; excludes downtime field |
| downtime_min | minutes | Remaining attributed downtime within planned time |
| downtime_reason | text | One dominant category for downtime in the observation |
| defect_type | text | One dominant category assigned to scrap; No scrap when zero scrap |
| material_batch | text | Synthetic daily batch code |
| steel_grade | category | Synthetic S235, S355 or S275 product association |
| operator_team | category | Fixed anonymous team per shift |
| runtime_min | derived minutes | Planned minus setup minus downtime |
| week_start | derived date | Monday of observation week |

Cleaning strips category whitespace, parses ISO dates and numeric fields, rejects
missing/blank values, duplicates, non-finite or negative values and fractional quantities.
Actual must equal good plus scrap. Time losses cannot exceed planned time; output cannot
exceed ideal runtime capacity. Invalid records are reported with an error rather than
silently dropped or imputed. Valid zero output gives undefined quality and OEE.

Setup is a separate category in the combined loss Pareto. Defect attribution is a
simplified classification, not an individual defect log or verified root cause.
