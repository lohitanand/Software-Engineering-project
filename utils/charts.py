"""utils/charts.py — Plotly chart builders with dark-theme colors."""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

BLUE   = "#3d7fd4"
GREEN  = "#2da870"
RED    = "#e05c5c"
ORANGE = "#e8944a"
PURPLE = "#9b72d4"
TEAL   = "#36b8c8"

# Base layout WITHOUT xaxis/yaxis — those are added per-chart
_BASE = dict(
    paper_bgcolor="#0a0e1a",
    plot_bgcolor="#0d1220",
    font=dict(family="DM Sans, sans-serif", color="#c8d4e8", size=12),
    title_font=dict(family="Space Mono, monospace", color="#7eb3ff", size=13),
    legend=dict(bgcolor="#0d1628", bordercolor="#1e3060", borderwidth=1,
                font=dict(color="#c8d4e8"), orientation="h",
                yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=40, r=20, t=55, b=80),
)

_XAXIS = dict(gridcolor="#1a2a45", linecolor="#1e3060",
              tickfont=dict(color="#7a9cc8"), title_font=dict(color="#7a9cc8"))
_YAXIS = dict(gridcolor="#1a2a45", linecolor="#1e3060",
              tickfont=dict(color="#7a9cc8"), title_font=dict(color="#7a9cc8"))

def _layout(title, x_title="Project", y_title="", barmode=None, y_range=None):
    """Build a full layout dict without duplicate keys."""
    l = dict(**_BASE,
             title=title,
             xaxis=dict(**_XAXIS, title=x_title, tickangle=-35),
             yaxis=dict(**_YAXIS, title=y_title))
    if barmode:   l["barmode"] = barmode
    if y_range:   l["yaxis"]["range"] = y_range
    return l

def _met_colors(series):
    return [GREEN if v == "Yes" else RED for v in series]

# ── SLA: BAT ──────────────────────────────────────────────────────────────────
def bat_leakage_bar(df):
    fig = go.Figure()
    fig.add_bar(x=df["Project Name"], y=df["BAT Sev1+2 Defects"],
                name="Total BAT", marker_color=BLUE, opacity=0.85)
    fig.add_bar(x=df["Project Name"], y=df["BAT Sev1+2 Defects (Leaked)"],
                name="Leaked", marker_color=RED, opacity=0.9)
    fig.update_layout(**_layout("BAT Defects – Total vs Leaked", y_title="Count", barmode="group"))
    return fig

def bat_leakage_pct(df):
    fig = go.Figure(go.Bar(
        x=df["Project Name"], y=df["Prod Sev1+2 Leakage %"],
        marker_color=_met_colors(df["SLA Met"]),
        text=df["SLA Met"], textposition="outside",
        textfont=dict(color="#c8d4e8", size=10),
    ))
    fig.update_layout(**_layout("Prod Sev1+2 Leakage % (🟢 Met / 🔴 Not Met)", y_title="Leakage %"))
    return fig

def sla_met_pie(df, title="SLA Met"):
    cnt = df["SLA Met"].value_counts().reset_index()
    cnt.columns = ["SLA Met", "Count"]
    fig = px.pie(cnt, values="Count", names="SLA Met", color="SLA Met",
                 color_discrete_map={"Yes": GREEN, "No": RED}, title=title, hole=0.45)
    fig.update_traces(textposition="inside", textinfo="percent+label",
                      textfont=dict(color="white", size=12),
                      marker=dict(line=dict(color="#0a0e1a", width=2)))
    fig.update_layout(**_BASE, title=title)
    return fig

# ── SLA: Prod Sev12 ───────────────────────────────────────────────────────────
def prod_sev12_leakage(df):
    fig = go.Figure(go.Bar(
        x=df["Project Name"], y=df["Prod Sev1+2 Leakage %"],
        marker_color=_met_colors(df["SLA Met"]),
        text=df["SLA Met"], textposition="outside",
        textfont=dict(color="#c8d4e8", size=10),
    ))
    fig.update_layout(**_layout("Prod Sev1&2 Leakage %", y_title="Leakage %"))
    return fig

def prod_sev12_defects(df):
    fig = go.Figure()
    fig.add_bar(x=df["Project Name"], y=df["BAT Sev1+2 Defects"],
                name="BAT Defects", marker_color=BLUE, opacity=0.85)
    fig.add_bar(x=df["Project Name"], y=df["Prod Sev1+2 Defects (Leaked)"],
                name="Prod Leaked", marker_color=RED, opacity=0.9)
    fig.update_layout(**_layout("Prod Sev1&2 – BAT vs Leaked", y_title="Count", barmode="group"))
    return fig

# ── SLA: Prod Sev3 ────────────────────────────────────────────────────────────
def prod_sev3_leakage(df):
    fig = go.Figure(go.Bar(
        x=df["Project Name"], y=df["Prod Sev3 Leakage %"],
        marker_color=_met_colors(df["SLA Met"]),
        text=df["SLA Met"], textposition="outside",
        textfont=dict(color="#c8d4e8", size=10),
    ))
    fig.update_layout(**_layout("Prod Sev3 Leakage %", y_title="Leakage %"))
    return fig

def prod_sev3_defects(df):
    fig = go.Figure()
    fig.add_bar(x=df["Project Name"], y=df["BAT Sev3 Defects"],
                name="BAT Sev3", marker_color=ORANGE, opacity=0.85)
    fig.add_bar(x=df["Project Name"], y=df["Prod Sev3 Defects (Leaked)"],
                name="Prod Leaked", marker_color=RED, opacity=0.9)
    fig.update_layout(**_layout("Prod Sev3 – BAT vs Leaked", y_title="Count", barmode="group"))
    return fig

# ── SLA: Invalid Defects ──────────────────────────────────────────────────────
def invalid_defects_bar(df):
    fig = go.Figure(go.Bar(
        x=df["Project Name"], y=df["Invalid Defects %"],
        marker_color=_met_colors(df["SLA Met"]),
        text=df["SLA Met"], textposition="outside",
        textfont=dict(color="#c8d4e8", size=10),
    ))
    fig.update_layout(**_layout("Invalid/Rejected Defects %", y_title="Invalid %"))
    return fig

def invalid_defects_counts(df):
    fig = go.Figure()
    fig.add_bar(x=df["Project Name"], y=df["Invalid SIT  Defects"],
                name="Invalid SIT", marker_color=ORANGE, opacity=0.85)
    fig.add_bar(x=df["Project Name"], y=df["Invalid Reg  Defects (Leaked)"],
                name="Invalid Reg", marker_color=PURPLE, opacity=0.85)
    fig.update_layout(**_layout("Invalid Defects – SIT vs Reg", y_title="Count", barmode="group"))
    return fig

# ── SLA: Test Execution ───────────────────────────────────────────────────────
def test_execution_bar(df):
    fig = go.Figure(go.Bar(
        x=df["Project Name"], y=df["On-time Execution %"],
        marker_color=_met_colors(df["SLA Met"]),
        text=df["SLA Met"], textposition="outside",
        textfont=dict(color="#c8d4e8", size=10),
    ))
    fig.add_hline(y=99, line_dash="dash", line_color=RED,
                  annotation_text="Min 99%", annotation_font_color=RED)
    fig.update_layout(**_layout("On-time Execution %", y_title="Execution %", y_range=[90, 102]))
    return fig

def test_execution_breakdown(df):
    fig = go.Figure()
    fig.add_bar(x=df["Project Name"], y=df["Executed On-time"],
                name="On-time", marker_color=GREEN, opacity=0.85)
    fig.add_bar(x=df["Project Name"], y=df["Executed Late"],
                name="Late", marker_color=RED, opacity=0.85)
    fig.update_layout(**_layout("Execution – On-time vs Late", y_title="Test Cases", barmode="stack"))
    return fig

# ── SLA: Schedule Slippage ────────────────────────────────────────────────────
def schedule_variance_bar(df):
    colors = [GREEN if v <= 0 else RED for v in df["Schedule Variance (days)"]]
    fig = go.Figure(go.Bar(
        x=df["Project Name"], y=df["Schedule Variance (days)"],
        marker_color=colors, text=df["SLA Met"], textposition="outside",
        textfont=dict(color="#c8d4e8", size=10),
    ))
    fig.add_hline(y=0, line_color="#5a7aaa", line_width=1)
    fig.update_layout(**_layout("Schedule Variance (days)", y_title="Days"))
    return fig

# ── KPI: Automation Coverage ──────────────────────────────────────────────────
def automation_coverage_bar(df, pct_col, title):
    fig = go.Figure(go.Bar(
        x=df["Project Name"], y=df[pct_col],
        marker_color=_met_colors(df["KPI Met"]),
        text=df["KPI Met"], textposition="outside",
        textfont=dict(color="#c8d4e8", size=10),
    ))
    fig.add_hline(y=99, line_dash="dash", line_color=RED,
                  annotation_text="Min 99%", annotation_font_color=RED)
    fig.update_layout(**_layout(title, y_title="Coverage %", y_range=[85, 106]))
    return fig

def automation_scenarios_bar(df, total_col, title):
    auto_col = "Automated Scenarios"
    manual = df[total_col] - df[auto_col]
    fig = go.Figure()
    fig.add_bar(x=df["Project Name"], y=df[auto_col],
                name="Automated", marker_color=GREEN, opacity=0.85)
    fig.add_bar(x=df["Project Name"], y=manual,
                name="Not Automated", marker_color=ORANGE, opacity=0.75)
    fig.update_layout(**_layout(title, y_title="Scenarios", barmode="stack"))
    return fig

def kpi_met_pie(df, title="KPI Met"):
    cnt = df["KPI Met"].value_counts().reset_index()
    cnt.columns = ["KPI Met", "Count"]
    fig = px.pie(cnt, values="Count", names="KPI Met", color="KPI Met",
                 color_discrete_map={"Yes": GREEN, "No": RED}, title=title, hole=0.45)
    fig.update_traces(textposition="inside", textinfo="percent+label",
                      textfont=dict(color="white", size=12),
                      marker=dict(line=dict(color="#0a0e1a", width=2)))
    fig.update_layout(**_BASE, title=title)
    return fig