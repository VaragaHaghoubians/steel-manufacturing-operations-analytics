# Project definition

This implementation follows the user-provided manufacturing analytics plan: a steel
fabrication workflow with pressing, spot welding, machining, inspection and packaging.
The Persian planning notes are expressed here in English; no private experience claims
or personal details are embedded in the dataset.

## Business questions

- Does actual output meet the plan by day, week, shift, machine and operation?
- Which operation is a candidate capacity constraint after pooling parallel machines?
- Where is scrap concentrated by defect, machine, shift and product?
- Which attributed losses account for most downtime?
- What are machine availability, performance, quality and OEE?
- How do shifts compare in output, scrap, downtime and cycle-time variability?
- Which investigations should management prioritize?

## Simulation design

Seven machines, three shifts and 180 consecutive calendar days starting January 1, 2025.
Planned production time is 450 minutes per machine-shift, excluding a 30-minute break.
Setup is separately counted inside planned time; categorized downtime excludes setup.
Product mix changes ideal cycle times by a modeled factor. The same date/shift product
label is used across operations, but records are not linked by individual parts or WIP.
Welding receives higher modeled speed losses and scrap probability; PRESS_600T receives
extra downtime. Night shift receives greater random cycle-time loss and scrap probability.
These are disclosed simulation choices, not discoveries about an actual factory.

## Scope and deliverables

Generation, cleaning/validation, pooled metrics, four charts, seven executed notebooks,
KPI CSVs, an Excel workbook, a PDF briefing and simple checks and GitHub instructions.
Python analysis is the primary deliverable; a native Power BI dashboard is deferred as
in the plan. ML and predictive maintenance are outside version one.

## Acceptance criteria

3,780 unique default observations; valid count and time balances; reproducible seed;
known-answer KPI checks; notebooks execute; figures and PDF are inspected;
findings are generated from metrics and distinguish simulation from causal conclusions.
