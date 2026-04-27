# Task_02_Descriptive_Stats

## Project Overview

This project analyzes the 2024 Facebook Political Advertising dataset using three different analytical approaches:

1. Pure Python (standard library only)
2. Pandas
3. Polars

The objective was to compute the same descriptive statistics and grouped aggregations across all three implementations, then compare how each tool handles data analysis tasks such as type inference, missing values, grouping, and statistical summaries.

This milestone builds on Task 1 by introducing:

- A third framework (Polars)
- Grouped analysis by organization and ad combinations
- Cross-tool validation of identical results
- Reflection on tradeoffs between analytical tools

---

## Dataset

Dataset used:

**2024 Facebook Political Ads Dataset**
link - Google Drive: 2024 Facebook Political Ads
Download and place the CSV file inside the `data/` folder.

Project Structure-
Task_02_Descriptive_Stats/
│── data/
│── scripts/
│   ├── pure_python_stats.py
│   ├── pandas_stats.py
│   └── polars_stats.py
│── results/
│   ├── pure_python_summary.txt
│   ├── pandas_summary.txt
│   └── polars_summary.txt
│── REFLECTION.md
│── README.md
│── requirements.txt

## How to Run
Clone repository:
git clone https://github.com/SamritaNagarkar/Task_02_Descriptive_Stats.git
cd Task_02_Descriptive_Stats

Install dependencies:
pip install -r requirements.txt

Run scripts:
python scripts/pure_python_stats.py
python scripts/pandas_stats.py
python scripts/polars_stats.py

Outputs saved in:
results/

## Pure Python

The Pure Python implementation required the most manual development effort. Each step had to be explicitly programmed, including:

- CSV file loading  
- Missing value handling  
- Data type inference  
- Mean, median, and standard deviation calculations  
- Grouping rows using dictionaries  
- Frequency counting for categorical columns  

Although this approach required more time to develop, it provided the strongest understanding of the calculations and processes that analytical libraries automate. It also required careful handling of edge cases such as empty values, mixed data types, and grouped calculations.

---

## Pandas

Pandas significantly reduced development time.
Built-in functions such as:

- `describe()`
- `value_counts()`
- `groupby()`
- `isnull().sum()`

made common analysis tasks substantially faster and easier to implement.
Pandas was the most familiar and practical option for day-to-day analytics work. However, several defaults occur automatically, including:

- automatic type inference  
- standard deviation defaults  
- null handling during aggregation  

This convenience is valuable

---

## Polars

Polars introduced a more explicit and modern workflow.
Instead of relying heavily on chained DataFrame methods, Polars uses expressions such as:

- `pl.col("column").mean()`
- `group_by().agg()`

Polars appeared stricter than Pandas with respect to data types and transformations. it appears highly scalable and well suited for larger analytical workloads.

---

## Result Comparison

All three approaches produced matching core outputs:

- 246,745 rows  
- 41 columns  
- `bylines`: 1,009 missing values  
- 4,475 unique `page_id` groups  
- 246,745 unique `page_id + ad_id` groups  

Means, medians, counts, minimums, and maximums were nearly identical across all three implementations.

Minor differences were limited to:

- rounding format  
- output formatting  
- standard deviation defaults  

This confirmed that all three implementations were logically consistent.

---

## Key Findings

The dataset was relatively clean, with only minor missing values.

Unlike Task 1, the following fields were already stored as numeric values:

- `estimated_spend`
- `estimated_impressions`
- `estimated_audience_size`

This reduced preprocessing requirements significantly.

Many political topic and message columns were binary indicators (`0/1`), suggesting machine-generated classification labels.
Grouped analysis showed that advertising activity was distributed across thousands of organizations, while most rows represented unique ad-level records.

---

## Key Learnings

The most important takeaway from this project was that tools differ primarily in usability and workflow, rather than mathematics.

The core analytical logic remains the same:

- identify data types  
- handle missing values  
- aggregate correctly  
- validate outputs  

Pure Python develops foundational understanding.  
Pandas maximizes productivity.  
Polars emphasizes scalability and explicit design.




