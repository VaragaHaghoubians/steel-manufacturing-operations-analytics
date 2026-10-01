# Interview questions: answers in plain English

**What did you build?**
A beginner Python analysis project using made-up steel fabrication data. I studied
production output, scrap, downtime, cycle times and OEE, then made charts and a summary.

**Why synthetic data?**
I wanted a complete example with the fields I needed without sharing company information.
The numbers are for learning, so I cannot claim they describe a real factory.

**What is one row?**
One machine, on one date, during one shift. It includes the product, quantities and time losses.

**How did you clean it?**
I checked missing values, repeated machine-shift rows, negative numbers, whole-unit counts,
time balances and whether good plus scrap equals actual output. Invalid rows stop the script.

**What is OEE?**
Availability times performance times quality. It combines time loss, speed loss and rejected
output. I can explain the 54% worked example in docs/kpi_examples.md.

**Why not average scrap percentages?**
Rows can have different production volumes. I add all scrap and divide by all actual output.

**How did you investigate bottlenecks?**
I compared good output rates by operation, adding parallel machine outputs first. This is
only a first check because the data does not track inventory or transfers between stations.

**What did the charts show?**
Open reports/manufacturing_summary.md and explain one computed finding. Remember that
welding speed losses and night-shift variation were deliberately included in the generator.

**What would you do with real data?**
First confirm the definitions with the plant team, check product mix and machine standards,
and collect downtime events and inventory between operations. Then repeat the analysis.

**Did you build a predictive model or achieve cost savings?**
No. This version is descriptive analysis. It does not prove causes or measure savings.

**What are you still learning?**
Answer honestly. For example: I am still practicing Pandas grouping and chart formatting,
and I am learning how to validate real manufacturing data.

**Did you use help?**
Describe the help you used truthfully. Only claim independent work or skills that you can
demonstrate. Use the practice tasks in START_HERE.md to build that understanding.
