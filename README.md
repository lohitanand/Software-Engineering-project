# QA Dashboard — Streamlit App

A multi-page Streamlit dashboard that reads SLA and KPI data from an Excel
file and presents it as interactive tables and Plotly charts.

---

## Project Structure

```
qa_dashboard/
│
├── QA_Home.py                  ← Entry-point / Page 1
│
├── pages/
│   └── Overall_Dashboard.py   ← Page 2 (auto-discovered by Streamlit)
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py          ← Cached Excel reader
│   └── charts.py               ← Reusable Plotly chart builders
│
├── data/
│   └── metrics.xlsx            ← Source data (SLA + KPI sheets)
│
├── create_sample_data.py       ← One-off helper to regenerate sample data
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. (Optional) Regenerate the sample Excel file

```bash
python create_sample_data.py
```

### 3. Run the app

```bash
streamlit run QA_Home.py
```

Streamlit will open `http://localhost:8501` in your browser.
Navigate between pages using the **sidebar**.

---

## Excel File Format

### Sheet: `SLA`

| Column | Type | Description |
|---|---|---|
| Project | str | Project name |
| Month | str | Month label (Jan, Feb …) |
| SLA_Target_% | float | Target SLA percentage |
| SLA_Achieved_% | float | Actual SLA achieved |
| Total_Tickets | int | Total tickets in period |
| Resolved_OnTime | int | Tickets resolved within SLA |
| Breached | int | Tickets that breached SLA |
| Status | str | "Met" or "Breached" |

### Sheet: `KPI`

| Column | Type | Description |
|---|---|---|
| Project | str | Project name |
| Month | str | Month label |
| Defect_Density | float | Defects per KLOC or function point |
| Test_Coverage_% | float | Code / requirement coverage % |
| Test_Pass_Rate_% | float | % of tests passing |
| Automation_Rate_% | float | % of tests automated |
| Avg_Resolution_Days | float | Avg days to resolve a defect |
| Critical_Bugs_Open | int | Open critical bugs at month-end |
| Customer_Satisfaction | float | Score 0–5 |

---

## Pages

### 🏠 QA Home
- Sidebar filters by Project and Month
- Summary metric cards (4 KPIs)
- Colour-coded `st.dataframe()` for SLA (green = Met, red = Breached)
- Gradient-highlighted `st.dataframe()` for KPI quality metrics
- CSV download buttons

### 📊 Overall Dashboard
- Two tabs: **SLA** and **KPI**
- For every project:
  - **SLA tab**: grouped bar (target vs achieved), stacked bar (ticket
    breakdown), pie chart (status distribution)
  - **KPI tab**: multi-line quality chart, customer satisfaction gauge,
    defect density dual-axis bar, resolution days line chart
- Sidebar controls: project multi-select, chart height slider, raw-data toggle
