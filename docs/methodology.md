# Methodology

For a group of observations, sum denominators before dividing. Do not average row-level
OEE, scrap percentages or cycle times without appropriate weights.

| Measure | Aggregate calculation |
|---|---|
| Attainment | sum(actual) / sum(planned quantity) |
| Scrap rate | sum(scrap) / sum(actual) |
| Runtime | planned production minutes − setup minutes − downtime minutes |
| Availability | sum(runtime) / sum(planned production minutes) |
| Performance | sum(actual × ideal cycle seconds / 60) / sum(runtime) |
| Quality | sum(good) / sum(actual) |
| OEE | pooled availability × pooled performance × pooled quality |
| Weighted cycle time | sum(cycle seconds × actual) / sum(actual) |
| Good output rate | sum(good) / sum(planned machine hours) |

Planned time excludes breaks but includes setup. OEE is undefined when runtime or gross
output is zero; counts and attainment remain available. Aggregate OEE uses a disclosed
product of pooled ratios. For differing ideal rates it need not equal sum(good × ideal
cycle time) / sum(planned time). Agree on the organization's preferred convention first.
Availability is a scheduled-time metric; calendar utilization is not modeled.

## Capacity and bottleneck screening

Sum good output across parallel machines within each date/shift/operation. Average these
operation totals and divide by 7.5 scheduled hours. Rank ascending as a capacity-screening
proxy. Do not compare average individual machines against pooled operations. The model
does not enforce downstream transfers, so the weakest stage is only a candidate constraint.
Product quantities are treated as comparable illustrative units, not equivalent workloads.

## Pareto and shifts

The lost-time Pareto combines categorized downtime with setup as a distinct category.
Categories do not overlap. The defect Pareto weights scrap counts. Dominant-category
attribution assigns all shift losses or scrap to one label; it is not an event log.
Shift analyses include descriptive mean and standard deviation of observed cycle time.
Fixed shift/team assignment and product mix preclude operator or causal conclusions.

## Real-world extension

Validate source grain, shift calendars, rate standards, product routing and event coding.
Measure WIP and end-to-end throughput before investing in a suspected constraint. Use
baseline comparisons or an experiment to assess intervention impact. No cost savings,
machine failure prediction or real employer performance is claimed in this project.
