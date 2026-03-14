"""
utils/data_loader.py — loads all sheets from Dataset.xlsx
"""
import os
import pandas as pd
import streamlit as st

_BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_PATH = os.path.join(_BASE_DIR, "data", "Dataset.xlsx")

@st.cache_data(show_spinner="Loading data…")
def load_sla_definitions() -> pd.DataFrame:
    df = pd.read_excel(_DATA_PATH, sheet_name="SLAs & KPIs")
    kpi_idx = df.index[df['SLA Name'] == 'KPI Name'].tolist()
    if kpi_idx:
        return df.iloc[:kpi_idx[0]].dropna(how='all').copy().reset_index(drop=True)
    return df.dropna(how='all').reset_index(drop=True)

@st.cache_data(show_spinner="Loading data…")
def load_kpi_definitions() -> pd.DataFrame:
    df = pd.read_excel(_DATA_PATH, sheet_name="SLAs & KPIs")
    kpi_idx = df.index[df['SLA Name'] == 'KPI Name'].tolist()
    if kpi_idx:
        idx = kpi_idx[0]
        kpi_part = df.iloc[idx+1:].copy()
        kpi_part.columns = df.iloc[idx].tolist()
        return kpi_part.dropna(how='all').reset_index(drop=True)
    return pd.DataFrame()

@st.cache_data(show_spinner="Loading data…")
def load_bat_defect() -> pd.DataFrame:
    return pd.read_excel(_DATA_PATH, sheet_name="SLA-BAT Defect Leakage").dropna(subset=["Project Name"])

@st.cache_data(show_spinner="Loading data…")
def load_prod_sev12() -> pd.DataFrame:
    return pd.read_excel(_DATA_PATH, sheet_name="SLA-Prod defect leakage – Sev12").dropna(subset=["Project Name"])

@st.cache_data(show_spinner="Loading data…")
def load_prod_sev3() -> pd.DataFrame:
    return pd.read_excel(_DATA_PATH, sheet_name="SLA-Prod defect leakage – Sev3").dropna(subset=["Project Name"])

@st.cache_data(show_spinner="Loading data…")
def load_invalid_defects() -> pd.DataFrame:
    return pd.read_excel(_DATA_PATH, sheet_name="SLA-Invalid_Rejected_Defects").dropna(subset=["Project Name"])

@st.cache_data(show_spinner="Loading data…")
def load_test_execution() -> pd.DataFrame:
    return pd.read_excel(_DATA_PATH, sheet_name="SLA_Test_Execution_Rate").dropna(subset=["Project Name"])

@st.cache_data(show_spinner="Loading data…")
def load_schedule_slippage() -> pd.DataFrame:
    return pd.read_excel(_DATA_PATH, sheet_name="SLA- Schedule Slippage").dropna(subset=["Project Name"])

@st.cache_data(show_spinner="Loading data…")
def load_kpi_e2e() -> pd.DataFrame:
    return pd.read_excel(_DATA_PATH, sheet_name="KPI-%Automation Coverage - E2E").dropna(subset=["Project Name"])

@st.cache_data(show_spinner="Loading data…")
def load_kpi_sit() -> pd.DataFrame:
    return pd.read_excel(_DATA_PATH, sheet_name="KPI-%Automation Coverage -SIT").dropna(subset=["Project Name"])

@st.cache_data(show_spinner="Loading data…")
def load_kpi_reg() -> pd.DataFrame:
    return pd.read_excel(_DATA_PATH, sheet_name="KPI-%Automation Coverage -Reg").dropna(subset=["Project Name"])

def get_unique(df: pd.DataFrame, col: str) -> list:
    if col not in df.columns:
        return []
    return sorted(df[col].dropna().unique().tolist())