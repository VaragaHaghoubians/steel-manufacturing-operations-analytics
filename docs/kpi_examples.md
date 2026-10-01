# KPI examples you can calculate yourself

Imagine one machine has these numbers for a short example period:

| Item | Value |
|---|---|
| Planned production time | 100 minutes |
| Setup | 10 minutes |
| Other downtime | 10 minutes |
| Planned output | 150 units |
| Actual output | 120 units |
| Good output | 108 units |
| Scrap | 12 units |
| Ideal cycle time | 30 seconds per unit |

Runtime = 100 − 10 − 10 = **80 minutes**.

Production attainment = 120 / 150 = **80%**. The machine made 80% of its target.

Scrap rate = 12 / 120 = **10%**. Ten percent of its output was rejected.

Availability = 80 / 100 = **80%**. It ran during 80% of its planned time.

Ideal production time = 120 × 30 / 60 = **60 minutes**.
Performance = 60 / 80 = **75%**. The actual output represents 75% of ideal speed during runtime.

Quality = 108 / 120 = **90%**. Ninety percent of output was accepted.

OEE = 0.80 × 0.75 × 0.90 = **54%**. Use decimals in the multiplication.

## Combining rows

Add counts and time first, then divide. A shift producing ten units should not carry
the same weight as a shift producing a thousand units when you calculate quality.
If products have different ideal cycle times, calculate ideal production minutes for
each row before adding them. kpi.py does this with a column multiplication and `.sum()`.

## Cycle time

Cycle time means seconds needed to complete one unit. To summarize it, multiply each
row's cycle time by its output, add those numbers, then divide by total output. This is
an output-weighted average. Rows with more output have more influence.

## Pareto chart

Put loss categories in order from largest to smallest. The bars show lost time. The line
shows the running percentage: how much of all losses the categories cover together.

## Candidate bottleneck

Welding has two machines. Add their output before comparing the welding operation with
machining or packaging. The smallest operation output rate is worth investigating.
This model does not follow parts between stations, so the ranking cannot prove a real bottleneck.
