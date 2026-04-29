# UNT Digital Projects Lab — Data Preprocessing & Visualization Pipeline

## Overview
This project presents an end-to-end data preprocessing and visualization pipeline for the **UNT Digital Projects Lab** digitization tracking data. The raw data is exported from a Trello board that tracks digitization projects across various collections at the University of North Texas Libraries.

The goal is to clean, preprocess, and visualize the data to provide actionable insights into project progress, pipeline bottlenecks, partner activity, and collection timelines.

---

## Repository Structure

```
UNT-Digital-Projects/
│
├── step1_load.py                  # Load and inspect raw data
├── step2_drop_columns.py          # Drop irrelevant/empty columns
├── step3_missing_values.py        # Handle missing values
├── step4_dates.py                 # Parse and fix date columns
├── step5_clean_categories.py      # Clean categorical columns
├── step6_features.py              # Feature engineering
├── step7_export.py                # Final export to Excel
│
├── unt_cleaned.xlsx               # Cleaned dataset (output)
├── Digital projects Dashboard.pbix # Power BI dashboard
└── README.md
```

---

## Data Description

The raw dataset is a Trello board export from UNT Digital Projects Lab containing **100 rows × 33 columns** tracking active digitization projects.

Key columns include:
- **Card Name** — Project name
- **Labels** — Collection type (Nimitz, RTH25, Oral Histories, SPEC, etc.)
- **List Name** — Current pipeline stage
- **Start Date** — Project start date
- **Partner - Code** — External partner code
- **Final Items** — Actual digitized item count
- **Estimated Contents** — Estimated item count
- **Archived** — Whether project is archived

---

## Preprocessing Pipeline

The preprocessing is broken into 7 steps:

| Step | File | Description |
|------|------|-------------|
| 1 | `step1_load.py` | Load raw CSV and inspect shape and columns |
| 2 | `step2_drop_columns.py` | Drop 11 columns that are 90%+ empty or irrelevant |
| 3 | `step3_missing_values.py` | Fill nulls with appropriate defaults per column type |
| 4 | `step4_dates.py` | Parse 5 date columns to datetime format |
| 5 | `step5_clean_categories.py` | Clean Labels, standardize Pipeline Stage, add Has Partner flag |
| 6 | `step6_features.py` | Engineer 6 new features (Days in Pipeline, Completion Rate, etc.) |
| 7 | `step7_export.py` | Export final cleaned dataset to Excel |

### Engineered Features
- **Collection Type** — Cleaned version of Labels (color codes removed)
- **Pipeline Stage** — Standardized version of List Name
- **Has Partner** — Boolean flag for partner involvement
- **Days in Pipeline** — Days since project start date
- **Completion Rate %** — Final Items / Estimated Contents × 100
- **Checklist Completion %** — Completed checklist items / Total checklist items × 100
- **Start Month Year** — Month-year for time series analysis
- **Volume Bucket** — Item count categorized (Small, Medium, Large, XL)

---

## How to Run

1. Clone the repository
2. Place the raw CSV file in the same directory
3. Install dependencies:
```bash
pip install pandas numpy openpyxl
```
4. Run each step in order:
```bash
python step1_load.py
python step2_drop_columns.py
python step3_missing_values.py
python step4_dates.py
python step5_clean_categories.py
python step6_features.py
python step7_export.py
```
5. Open `unt_cleaned.xlsx` in Power BI Desktop

---

## Power BI Dashboard

The dashboard (`Digital projects Dashboard.pbix`) contains 5 pages:

| Page | Title | Key Visuals |
|------|-------|-------------|
| 1 | Portfolio Overview | KPI cards, Collection Type donut chart |
| 2 | Pipeline Stage Analysis | Projects by pipeline stage bar chart |
| 3 | Project Timelines | Top 10 longest projects, Avg days by collection |
| 4 | Partner & Collection Analysis | Projects by partner, Has Partner donut |
| 5 | Timeline Analysis | Projects by month/year, Active vs Archived |

### KPI Cards
- **Total Projects:** 100
- **Active Projects:** 85
- **Partner Projects:** 56
- **Avg Days in Pipeline:** 342.74 days

---

## Key Insights

- **Nimitz (21%)** and **RTH25 (19%)** are the largest collections
- **56%** of projects involve external partners
- Projects sit in the pipeline for an average of **342 days (~11 months)**
- Some projects have been in the pipeline for over **1,000 days**
- Most projects have **0% checklist completion**, indicating tracking gaps

---

## Tools Used
- **Python** (pandas, numpy, re, datetime)
- **Power BI Desktop**
- **Git / GitHub**

---

*Developed as part of the UNT Libraries Digital Projects Lab data workflow — April 2026*
