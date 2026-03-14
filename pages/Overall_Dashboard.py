"""pages/Overall_Dashboard.py — Corporate dark aesthetic dashboard."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import plotly.io as pio
from utils.data_loader import (
    load_bat_defect, load_prod_sev12, load_prod_sev3,
    load_invalid_defects, load_test_execution, load_schedule_slippage,
    load_kpi_e2e, load_kpi_sit, load_kpi_reg, get_unique,
)
from utils.charts import (
    bat_leakage_bar, bat_leakage_pct, sla_met_pie,
    prod_sev12_leakage, prod_sev12_defects,
    prod_sev3_leakage, prod_sev3_defects,
    invalid_defects_bar, invalid_defects_counts,
    test_execution_bar, test_execution_breakdown,
    schedule_variance_bar,
    automation_coverage_bar, automation_scenarios_bar, kpi_met_pie,
)

st.set_page_config(page_title="Overall Dashboard", page_icon="📊", layout="wide")

# ── Dark Plotly theme ────────────────────────────────────────────────────────
DARK_LAYOUT = dict(
    paper_bgcolor="#0a0e1a",
    plot_bgcolor="#0d1220",
    font=dict(family="DM Sans, sans-serif", color="#c8d4e8", size=12),
    title_font=dict(family="Space Mono, monospace", color="#7eb3ff", size=13),
    legend=dict(bgcolor="#0d1628", bordercolor="#1e3060", borderwidth=1,
                font=dict(color="#c8d4e8"), orientation="h",
                yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(gridcolor="#1a2a45", linecolor="#1e3060", tickfont=dict(color="#7a9cc8")),
    yaxis=dict(gridcolor="#1a2a45", linecolor="#1e3060", tickfont=dict(color="#7a9cc8")),
    margin=dict(l=40, r=20, t=55, b=40),
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp { background: #0a0e1a; }

section[data-testid="stSidebar"] {
    background: #0d1220 !important;
    border-right: 1px solid #1e2a45;
}
section[data-testid="stSidebar"] * { color: #c8d4e8 !important; }
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background: #1a2d4f !important; border: 1px solid #2e4a7a !important;
}

h1,h2,h3,h4,h5,h6,p,span,label,div { color: #e2e8f4 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1220 !important;
    border-bottom: 1px solid #1e3060 !important;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #5a7aaa !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.04em;
    border-radius: 6px 6px 0 0 !important;
    padding: 0.5rem 1.2rem !important;
    border: 1px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    background: #0f2a52 !important;
    color: #7eb3ff !important;
    border-color: #1e3060 #1e3060 #0a0e1a !important;
}
.stTabs [data-baseweb="tab-panel"] { background: #0a0e1a !important; padding-top: 1.2rem; }

/* Plotly charts */
.js-plotly-plot { border-radius: 10px; border: 1px solid #1e3060; background: #0d1220; }

/* Divider */
hr { border-color: #1a2a45 !important; }

/* Subheader */
.stSubheader { color: #7eb3ff !important; font-family: 'Space Mono',monospace !important; }

/* Expander */
details { background: #0d1628 !important; border: 1px solid #1e3060 !important; border-radius: 8px; }
details summary { color: #7eb3ff !important; }

/* Slider */
.stSlider [data-baseweb="slider"] { color: #3d7fd4 !important; }

/* Checkbox */
.stCheckbox label { color: #7a9cc8 !important; }

/* Info/Warning */
.stAlert { background: #0f1e38 !important; border-left-color: #2e5090 !important; }
.stAlert p { color: #7eb3ff !important; }

.page-title {
    font-family: 'Space Mono', monospace;
    font-size: 2rem; font-weight: 700;
    color: #e2e8f4 !important; letter-spacing: -0.02em;
}
.page-sub { color: #5a7aaa !important; font-size: 0.88rem; }
.tab-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.95rem; font-weight: 700;
    color: #7eb3ff !important; letter-spacing: 0.04em;
    margin-bottom: 1rem; padding: 0.5rem 0;
    border-bottom: 1px solid #1e3060;
}
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem; color: #5a7aaa !important;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">📊 Overall Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Interactive charts across all SLA and KPI sheets</div>', unsafe_allow_html=True)
st.divider()

# ── Load data ─────────────────────────────────────────────────────────────────
bat_df=load_bat_defect(); sev12_df=load_prod_sev12(); sev3_df=load_prod_sev3()
invalid_df=load_invalid_defects(); exec_df=load_test_execution(); slip_df=load_schedule_slippage()
kpi_e2e_df=load_kpi_e2e(); kpi_sit_df=load_kpi_sit(); kpi_reg_df=load_kpi_reg()

all_projects = sorted(set(
    bat_df["Project Name"].tolist()+sev12_df["Project Name"].tolist()+
    sev3_df["Project Name"].tolist()+invalid_df["Project Name"].tolist()+
    exec_df["Project Name"].tolist()+slip_df["Project Name"].tolist()+
    kpi_e2e_df["Project Name"].tolist()+kpi_sit_df["Project Name"].tolist()+
    kpi_reg_df["Project Name"].tolist()
))
all_streams=sorted(set(get_unique(bat_df,"Business Stream")+get_unique(sev12_df,"Business Stream")+
    get_unique(exec_df,"Business Stream")+get_unique(kpi_e2e_df,"Business Stream")))
all_phases=sorted(set(get_unique(bat_df,"Testing Phase")+get_unique(sev3_df,"Testing Phase")+
    get_unique(kpi_e2e_df,"Testing Phase")))

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Chart Settings")
    st.divider()
    sel_projects=st.multiselect("Projects",       all_projects, default=all_projects)
    sel_streams =st.multiselect("Business Stream",all_streams,  default=all_streams)
    sel_phases  =st.multiselect("Testing Phase",  all_phases,   default=all_phases)
    st.divider()
    chart_height=st.slider("Chart height (px)", 280, 600, 400, step=20)
    show_raw=st.checkbox("Show raw data under charts", value=False)

if not sel_projects:
    st.warning("⚠️ Select at least one project in the sidebar.")
    st.stop()

def _f(df):
    d=df.copy()
    if "Project Name"    in d.columns: d=d[d["Project Name"].isin(sel_projects)]
    if "Business Stream" in d.columns: d=d[d["Business Stream"].isin(sel_streams)]
    if "Testing Phase"   in d.columns: d=d[d["Testing Phase"].isin(sel_phases)]
    return d.reset_index(drop=True)

def _apply_dark(fig):
    fig.update_layout(**DARK_LAYOUT)
    fig.update_traces(marker_line_width=0)
    return fig

def _row(fl, fr, h, kl, kr):
    c1,c2=st.columns(2)
    with c1:
        fl=_apply_dark(fl); fl.update_layout(height=h)
        st.plotly_chart(fl, use_container_width=True, key=kl)
    with c2:
        fr=_apply_dark(fr); fr.update_layout(height=h)
        st.plotly_chart(fr, use_container_width=True, key=kr)

def _full(fig, h, key):
    fig=_apply_dark(fig); fig.update_layout(height=h)
    st.plotly_chart(fig, use_container_width=True, key=key)

def _no_data():
    st.info("No data matches the current filters — adjust the sidebar.")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_sla, tab_kpi = st.tabs(["  📋  SLA  ", "  📈  KPI  "])

with tab_sla:
    st.markdown('<div class="tab-header">SERVICE LEVEL AGREEMENTS</div>', unsafe_allow_html=True)
    s1,s2,s3,s4,s5 = st.tabs([
        "BAT Defect Leakage","Prod Sev1 & 2","Prod Sev3",
        "Invalid / Rejected Defects","Test Execution & Schedule"
    ])

    with s1:
        d=_f(bat_df)
        if d.empty: _no_data()
        else:
            _row(bat_leakage_bar(d), bat_leakage_pct(d), chart_height, "bat_bar","bat_pct")
            _full(sla_met_pie(d,"BAT – SLA Met Distribution"), chart_height-100,"bat_pie")
            if show_raw:
                with st.expander("Raw data"): st.dataframe(d,use_container_width=True)

    with s2:
        d=_f(sev12_df)
        if d.empty: _no_data()
        else:
            _row(prod_sev12_defects(d), prod_sev12_leakage(d), chart_height,"sev12_def","sev12_pct")
            _full(sla_met_pie(d,"Prod Sev1&2 – SLA Met"), chart_height-100,"sev12_pie")
            if show_raw:
                with st.expander("Raw data"): st.dataframe(d,use_container_width=True)

    with s3:
        d=_f(sev3_df)
        if d.empty: _no_data()
        else:
            _row(prod_sev3_defects(d), prod_sev3_leakage(d), chart_height,"sev3_def","sev3_pct")
            _full(sla_met_pie(d,"Prod Sev3 – SLA Met"), chart_height-100,"sev3_pie")
            if show_raw:
                with st.expander("Raw data"): st.dataframe(d,use_container_width=True)

    with s4:
        d=_f(invalid_df)
        if d.empty: _no_data()
        else:
            _row(invalid_defects_counts(d), invalid_defects_bar(d), chart_height,"inv_cnt","inv_pct")
            _full(sla_met_pie(d,"Invalid Defects – SLA Met"), chart_height-100,"inv_pie")
            if show_raw:
                with st.expander("Raw data"): st.dataframe(d,use_container_width=True)

    with s5:
        st.markdown('<div class="section-label">Test Execution Rate</div>', unsafe_allow_html=True)
        d=_f(exec_df)
        if d.empty: _no_data()
        else:
            _row(test_execution_breakdown(d), test_execution_bar(d), chart_height,"exec_bk","exec_bar")
            _full(sla_met_pie(d,"Test Execution – SLA Met"), chart_height-100,"exec_pie")
            if show_raw:
                with st.expander("Raw data"): st.dataframe(d,use_container_width=True)
        st.divider()
        st.markdown('<div class="section-label">Schedule Slippage</div>', unsafe_allow_html=True)
        d2=_f(slip_df)
        if d2.empty: _no_data()
        else:
            _full(schedule_variance_bar(d2), chart_height,"slip_bar")
            _full(sla_met_pie(d2,"Schedule Slippage – SLA Met"), chart_height-100,"slip_pie")
            if show_raw:
                with st.expander("Raw data"): st.dataframe(d2,use_container_width=True)

with tab_kpi:
    st.markdown('<div class="tab-header">KEY PERFORMANCE INDICATORS — AUTOMATION COVERAGE</div>', unsafe_allow_html=True)
    k1,k2,k3=st.tabs(["E2E Automation","SIT Automation","Regression Automation"])

    with k1:
        d=_f(kpi_e2e_df)
        if d.empty: _no_data()
        else:
            _row(automation_scenarios_bar(d,"Total E2E Scenarios","E2E – Automated vs Not Automated"),
                 automation_coverage_bar(d,"% E2E Scenarios Automated","E2E – % Automation Coverage"),
                 chart_height,"e2e_sc","e2e_pct")
            _full(kpi_met_pie(d,"E2E – KPI Met Distribution"), chart_height-100,"e2e_pie")
            if show_raw:
                with st.expander("Raw data"): st.dataframe(d,use_container_width=True)

    with k2:
        d=_f(kpi_sit_df)
        if d.empty: _no_data()
        else:
            _row(automation_scenarios_bar(d,"Total SIT Scenarios","SIT – Automated vs Not Automated"),
                 automation_coverage_bar(d,"% SIT Scenarios Automated","SIT – % Automation Coverage"),
                 chart_height,"sit_sc","sit_pct")
            _full(kpi_met_pie(d,"SIT – KPI Met Distribution"), chart_height-100,"sit_pie")
            if show_raw:
                with st.expander("Raw data"): st.dataframe(d,use_container_width=True)

    with k3:
        d=_f(kpi_reg_df)
        if d.empty: _no_data()
        else:
            _row(automation_scenarios_bar(d,"Total Reg Scenarios","Reg – Automated vs Not Automated"),
                 automation_coverage_bar(d,"% Reg Scenarios Automated","Reg – % Automation Coverage"),
                 chart_height,"reg_sc","reg_pct")
            _full(kpi_met_pie(d,"Reg – KPI Met Distribution"), chart_height-100,"reg_pie")
            if show_raw:
                with st.expander("Raw data"): st.dataframe(d,use_container_width=True)