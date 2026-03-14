"""QA_Home.py — Corporate dark aesthetic entry point."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
from utils.data_loader import (
    load_sla_definitions, load_kpi_definitions,
    load_bat_defect, load_prod_sev12, load_prod_sev3,
    load_invalid_defects, load_test_execution, load_schedule_slippage,
    load_kpi_e2e, load_kpi_sit, load_kpi_reg, get_unique,
)

st.set_page_config(page_title="QA Home", page_icon="🏠", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #0a0e1a;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0d1220 !important;
    border-right: 1px solid #1e2a45;
}
section[data-testid="stSidebar"] * { color: #c8d4e8 !important; }
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background: #1a2d4f !important;
    border: 1px solid #2e4a7a !important;
}

/* ── Main text ── */
h1, h2, h3, h4, h5, h6, p, span, label, div { color: #e2e8f4 !important; }

/* ── Dataframe ── */
.stDataFrame { border-radius: 10px; overflow: hidden; }
.stDataFrame thead tr th {
    background: #0f1e3a !important;
    color: #7eb3ff !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.06em;
    border-bottom: 1px solid #1e3060 !important;
}
.stDataFrame tbody tr:nth-child(even) td { background: #0d1628 !important; }
.stDataFrame tbody tr:nth-child(odd) td  { background: #0a1220 !important; }
.stDataFrame tbody tr:hover td { background: #13203a !important; }
.stDataFrame td { color: #c8d4e8 !important; border-color: #1a2a45 !important; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #0f1e38;
    border: 1px solid #1e3060;
    border-radius: 10px;
    padding: 1rem 1.2rem;
}
[data-testid="metric-container"] label { color: #7eb3ff !important; font-size: 0.78rem !important; letter-spacing:0.05em; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #e2e8f4 !important; font-family: 'Space Mono', monospace; font-size: 1.8rem !important; }

/* ── Divider ── */
hr { border-color: #1a2a45 !important; }

/* ── Expander ── */
details { background: #0d1628 !important; border: 1px solid #1e3060 !important; border-radius: 8px; }
details summary { color: #7eb3ff !important; }

/* ── Download button ── */
.stDownloadButton button {
    background: #0f2a52 !important;
    border: 1px solid #2e5090 !important;
    color: #7eb3ff !important;
    border-radius: 6px;
    font-family: 'DM Sans', sans-serif;
}
.stDownloadButton button:hover { background: #1a3a6a !important; }

/* ── Warning / info ── */
.stAlert { background: #0f1e38 !important; border-left-color: #2e5090 !important; }

/* ── Caption ── */
.stCaption { color: #5a7aaa !important; }

/* Custom section headers */
.sla-header {
    background: linear-gradient(135deg, #0f2a52 0%, #1a3d6e 100%);
    color: #7eb3ff !important;
    padding: 0.65rem 1.2rem;
    border-radius: 8px;
    margin-bottom: 0.75rem;
    border-left: 3px solid #3d7fd4;
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    letter-spacing: 0.04em;
}
.kpi-header {
    background: linear-gradient(135deg, #0a2e1e 0%, #113d28 100%);
    color: #5fcea0 !important;
    padding: 0.65rem 1.2rem;
    border-radius: 8px;
    margin-bottom: 0.75rem;
    border-left: 3px solid #2da870;
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    letter-spacing: 0.04em;
}
.page-title {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #e2e8f4 !important;
    letter-spacing: -0.02em;
    margin-bottom: 0;
}
.page-sub {
    color: #5a7aaa !important;
    font-size: 0.88rem;
    margin-top: 0.2rem;
}
.badge-sla {
    display:inline-block; background:#0f2a52; color:#7eb3ff !important;
    border:1px solid #2e5090; border-radius:4px;
    padding:2px 10px; font-size:0.72rem; font-family:'Space Mono',monospace;
    letter-spacing:0.05em; margin-bottom:0.5rem;
}
.badge-kpi {
    display:inline-block; background:#0a2e1e; color:#5fcea0 !important;
    border:1px solid #1e6644; border-radius:4px;
    padding:2px 10px; font-size:0.72rem; font-family:'Space Mono',monospace;
    letter-spacing:0.05em; margin-bottom:0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">🏠 QA Home</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">All SLA and KPI data pulled from <strong>Dataset.xlsx</strong></div>', unsafe_allow_html=True)
st.divider()

# ── Load data ────────────────────────────────────────────────────────────────
sla_def    = load_sla_definitions()
kpi_def    = load_kpi_definitions()
bat_df     = load_bat_defect()
sev12_df   = load_prod_sev12()
sev3_df    = load_prod_sev3()
invalid_df = load_invalid_defects()
exec_df    = load_test_execution()
slip_df    = load_schedule_slippage()
kpi_e2e_df = load_kpi_e2e()
kpi_sit_df = load_kpi_sit()
kpi_reg_df = load_kpi_reg()

all_projects = sorted(set(
    bat_df["Project Name"].tolist() + sev12_df["Project Name"].tolist() +
    sev3_df["Project Name"].tolist() + invalid_df["Project Name"].tolist() +
    exec_df["Project Name"].tolist() + slip_df["Project Name"].tolist() +
    kpi_e2e_df["Project Name"].tolist() + kpi_sit_df["Project Name"].tolist() +
    kpi_reg_df["Project Name"].tolist()
))
all_streams = sorted(set(
    get_unique(bat_df,"Business Stream") + get_unique(sev12_df,"Business Stream") +
    get_unique(exec_df,"Business Stream") + get_unique(kpi_e2e_df,"Business Stream")
))
all_phases = sorted(set(
    get_unique(bat_df,"Testing Phase") + get_unique(sev3_df,"Testing Phase") +
    get_unique(kpi_e2e_df,"Testing Phase")
))

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Filters")
    st.divider()
    sel_projects = st.multiselect("Project Name",    all_projects, default=all_projects)
    sel_streams  = st.multiselect("Business Stream", all_streams,  default=all_streams)
    sel_phases   = st.multiselect("Testing Phase",   all_phases,   default=all_phases)

def _f(df):
    d = df.copy()
    if "Project Name"    in d.columns: d = d[d["Project Name"].isin(sel_projects)]
    if "Business Stream" in d.columns: d = d[d["Business Stream"].isin(sel_streams)]
    if "Testing Phase"   in d.columns: d = d[d["Testing Phase"].isin(sel_phases)]
    return d.reset_index(drop=True)

bat_f=_f(bat_df); sev12_f=_f(sev12_df); sev3_f=_f(sev3_df)
invalid_f=_f(invalid_df); exec_f=_f(exec_df); slip_f=_f(slip_df)
e2e_f=_f(kpi_e2e_df); sit_f=_f(kpi_sit_df); reg_f=_f(kpi_reg_df)

def _style_met(df, met_col):
    def hl(val):
        if val=="Yes": return "background-color:#0d2e1a;color:#4ade80;"
        if val=="No":  return "background-color:#2e0d0d;color:#f87171;"
        return ""
    if met_col in df.columns and not df.empty:
        return df.style.applymap(hl, subset=[met_col])
    return df.style

def _summary(df, met_col, is_sla=True):
    total = len(df)
    met   = int((df[met_col]=="Yes").sum()) if met_col in df.columns and not df.empty else 0
    pct   = f"{(met/total*100):.0f}%" if total else "—"
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Records", total)
    c2.metric("✅ Met", met)
    c3.metric("❌ Not Met", total-met)
    c4.metric("Compliance", pct)

def _section(label, badge, df, met_col, csv_name, is_sla=True):
    css = "sla-header" if is_sla else "kpi-header"
    bcss = "badge-sla" if is_sla else "badge-kpi"
    st.markdown(f'<span class="{bcss}">{"SLA" if is_sla else "KPI"}</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="{css}">{label}</div>', unsafe_allow_html=True)
    _summary(df, met_col, is_sla)
    if df.empty:
        st.warning("No records match the current filters.")
    else:
        st.dataframe(_style_met(df, met_col), use_container_width=True, height=280)
    with st.expander("📥 Download CSV"):
        st.download_button("Download", df.to_csv(index=False).encode(), csv_name, "text/csv")
    st.divider()

# ── Section 0a: SLA Definitions ──────────────────────────────────────────────
st.markdown('<span class="badge-sla">REFERENCE</span>', unsafe_allow_html=True)
st.markdown('<div class="sla-header">📋 Section 0a — SLA Definitions</div>', unsafe_allow_html=True)
st.caption("Service Level Agreement reference thresholds and descriptions.")
if not sla_def.empty:
    st.dataframe(sla_def, use_container_width=True, height=200)
else:
    st.info("SLA definitions not found.")
st.divider()

# ── Section 0b: KPI Definitions ──────────────────────────────────────────────
st.markdown('<span class="badge-kpi">REFERENCE</span>', unsafe_allow_html=True)
st.markdown('<div class="kpi-header">📊 Section 0b — KPI Definitions</div>', unsafe_allow_html=True)
st.caption("Key Performance Indicator reference thresholds and descriptions.")
if not kpi_def.empty:
    st.dataframe(kpi_def, use_container_width=True, height=200)
else:
    st.info("KPI definitions not found.")
st.divider()

# ── SLA Sections ─────────────────────────────────────────────────────────────
_section("📋 Section 1 — BAT Defect Leakage",             "SLA", bat_f,     "SLA Met","bat_defect.csv")
_section("📋 Section 2 — Prod Defect Leakage – Sev1 & 2", "SLA", sev12_f,   "SLA Met","prod_sev12.csv")
_section("📋 Section 3 — Prod Defect Leakage – Sev3",     "SLA", sev3_f,    "SLA Met","prod_sev3.csv")
_section("📋 Section 4 — Invalid / Rejected Defects",     "SLA", invalid_f, "SLA Met","invalid_defects.csv")
_section("📋 Section 5 — Test Execution Rate",            "SLA", exec_f,    "SLA Met","test_execution.csv")
_section("📋 Section 6 — Schedule Slippage",              "SLA", slip_f,    "SLA Met","schedule_slippage.csv")

# ── KPI Sections ─────────────────────────────────────────────────────────────
_section("📊 Section 7 — % Automation Coverage – E2E", "KPI", e2e_f, "KPI Met","kpi_e2e.csv", is_sla=False)
_section("📊 Section 8 — % Automation Coverage – SIT", "KPI", sit_f, "KPI Met","kpi_sit.csv", is_sla=False)
_section("📊 Section 9 — % Automation Coverage – Reg", "KPI", reg_f, "KPI Met","kpi_reg.csv", is_sla=False)

st.caption("💡 Switch to Overall Dashboard in the sidebar for interactive charts.")