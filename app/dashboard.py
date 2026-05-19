"""Interactive HR attrition dashboard."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import CHART_COLORS, GITHUB_REPO_URL, PLOTLY_TEMPLATE
from src.data_loader import load_hr_data
from src.metrics import attrition_by_column, filter_dataframe, summary_kpis

st.set_page_config(
    page_title="HR Employee Attrition",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLOR_SEQUENCE = CHART_COLORS


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    return load_hr_data()


def _bar_chart(
    frame: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    orientation: str = "v",
    text_col: str | None = None,
) -> go.Figure:
    fig = px.bar(
        frame,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=COLOR_SEQUENCE,
        template=PLOTLY_TEMPLATE,
        orientation=orientation,
        text=text_col,
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
    )
    if text_col:
        fig.update_traces(textposition="outside")
    return fig


def _donut_chart(frame: pd.DataFrame, names: str, values: str, title: str) -> go.Figure:
    fig = px.pie(
        frame,
        names=names,
        values=values,
        title=title,
        hole=0.45,
        color_discrete_sequence=COLOR_SEQUENCE,
        template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20), showlegend=False)
    return fig


def sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")
    filter_defs = [
        ("Department", "Department"),
        ("Job Role", "Job Role"),
        ("Gender", "Gender"),
        ("Marital Status", "Marital Status"),
        ("Type Of Salary", "Type Of Salary"),
        ("Business Travel", "Business Travel"),
    ]
    selections: dict[str, list] = {}
    for label, column in filter_defs:
        options = sorted(df[column].dropna().unique().tolist())
        picked = st.sidebar.multiselect(label, options, default=[], key=f"filter_{column}")
        selections[column] = picked

    st.sidebar.markdown("---")
    st.sidebar.caption(f"[GitHub]({GITHUB_REPO_URL})")
    return filter_dataframe(df, selections)


def render_kpis(df: pd.DataFrame) -> None:
    kpis = summary_kpis(df)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Employees", f"{kpis['total_employees']:,}")
    c2.metric("Left (count)", f"{kpis['attrition_count']:,}")
    c3.metric("Attrition rate", f"{kpis['attrition_rate_pct']}%")
    c4.metric("Avg age", kpis["avg_age"])
    c5.metric("Avg tenure (yrs)", kpis["avg_years_at_company"])
    c6.metric("Avg monthly income", f"${kpis['avg_monthly_income']:,.0f}")


def tab_overview(df: pd.DataFrame) -> None:
    st.subheader("Attrition overview")
    col1, col2 = st.columns(2)

    dept = attrition_by_column(df, "Department")
    dept_chart = _bar_chart(
        dept,
        x="category",
        y="attrition_rate_pct",
        title="Attrition rate by department",
        text_col="attrition_rate_pct",
    )
    dept_chart.update_traces(texttemplate="%{text}%", textposition="outside")
    col1.plotly_chart(dept_chart, use_container_width=True)

    overall = pd.DataFrame(
        {
            "status": ["Stayed", "Left"],
            "count": [
                len(df) - df["Attrition Flag"].sum(),
                int(df["Attrition Flag"].sum()),
            ],
        }
    )
    col2.plotly_chart(
        _donut_chart(overall, "status", "count", "Workforce attrition split"),
        use_container_width=True,
    )

    exp = attrition_by_column(df[df["Attrition"] == "Yes"], "Experience Group", True)
    exp = exp.rename(columns={"share_pct": "share_pct"})
    fig = _bar_chart(
        exp,
        x="category",
        y="count",
        title="Leavers by years of experience (grouped)",
        text_col="share_pct",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)


def tab_demographics(df: pd.DataFrame) -> None:
    st.subheader("Demographics")
    left = df[df["Attrition"] == "Yes"]
    c1, c2, c3 = st.columns(3)

    gender = attrition_by_column(left, "Gender", True)
    c1.plotly_chart(
        _donut_chart(gender, "category", "count", "Leavers by gender"),
        use_container_width=True,
    )

    marital = attrition_by_column(left, "Marital Status", True)
    c2.plotly_chart(
        _donut_chart(marital, "category", "count", "Leavers by marital status"),
        use_container_width=True,
    )

    salary_type = attrition_by_column(left, "Type Of Salary", True)
    c3.plotly_chart(
        _donut_chart(salary_type, "category", "count", "Leavers by salary tier"),
        use_container_width=True,
    )

    age_grp = attrition_by_column(left, "Age Group", True)
    age_fig = _bar_chart(
        age_grp,
        x="category",
        y="count",
        title="Leavers by age group",
        text_col="share_pct",
    )
    age_fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(age_fig, use_container_width=True)


def tab_roles(df: pd.DataFrame) -> None:
    st.subheader("Roles and departments")
    c1, c2 = st.columns(2)

    roles = attrition_by_column(df, "Job Role")
    role_fig = _bar_chart(
        roles,
        x="attrition_rate_pct",
        y="category",
        title="Attrition rate by job role",
        orientation="h",
        text_col="attrition_rate_pct",
    )
    role_fig.update_traces(texttemplate="%{text}%", textposition="outside")
    c1.plotly_chart(role_fig, use_container_width=True)

    roles_left = attrition_by_column(df[df["Attrition"] == "Yes"], "Job Role", True)
    role_count_fig = _bar_chart(
        roles_left,
        x="count",
        y="category",
        title="Leavers by job role (share of all leavers)",
        orientation="h",
        text_col="share_pct",
    )
    role_count_fig.update_traces(texttemplate="%{text}%", textposition="outside")
    c2.plotly_chart(role_count_fig, use_container_width=True)

    edu = attrition_by_column(df[df["Attrition"] == "Yes"], "Education Field", True)
    edu_fig = _bar_chart(
        edu,
        x="category",
        y="count",
        title="Leavers by education field",
        text_col="share_pct",
    )
    edu_fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(edu_fig, use_container_width=True)


def tab_engagement(df: pd.DataFrame) -> None:
    st.subheader("Satisfaction and compensation")
    left = df[df["Attrition"] == "Yes"].dropna(subset=["Satisfaction Label"])
    c1, c2 = st.columns(2)

    sat = attrition_by_column(left, "Satisfaction Label", True)
    sat_fig = _bar_chart(
        sat,
        x="category",
        y="count",
        title="Leavers by job satisfaction level",
        text_col="share_pct",
    )
    sat_fig.update_traces(texttemplate="%{text}%", textposition="outside")
    c1.plotly_chart(sat_fig, use_container_width=True)

    income = left.groupby("Type Of Salary", observed=True)["Monthly Income"].mean().reset_index()
    income_fig = px.bar(
        income,
        x="Type Of Salary",
        y="Monthly Income",
        title="Average monthly income among leavers",
        color_discrete_sequence=COLOR_SEQUENCE,
        template=PLOTLY_TEMPLATE,
        text="Monthly Income",
    )
    income_fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    income_fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=50, b=20))
    c2.plotly_chart(income_fig, use_container_width=True)

    balance = attrition_by_column(df, "Work Life Balance")
    balance.rename(
        columns={"category": "Work Life Balance", "attrition_rate_pct": "rate"},
        inplace=True,
    )
    balance_fig = px.bar(
        balance,
        x="Work Life Balance",
        y="rate",
        title="Attrition rate by work-life balance score",
        color_discrete_sequence=COLOR_SEQUENCE,
        template=PLOTLY_TEMPLATE,
        text="rate",
    )
    balance_fig.update_traces(texttemplate="%{text}%", textposition="outside")
    balance_fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(balance_fig, use_container_width=True)


def main() -> None:
    st.title("HR Employee Attrition Dashboard")
    st.caption("Use the sidebar filters — all charts update together.")

    df = load_data()
    filtered = sidebar_filters(df)

    if filtered.empty:
        st.warning("No rows match the current filters. Clear one or more filters to continue.")
        return

    render_kpis(filtered)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Overview", "Demographics", "Roles & departments", "Satisfaction & pay"]
    )
    with tab1:
        tab_overview(filtered)
    with tab2:
        tab_demographics(filtered)
    with tab3:
        tab_roles(filtered)
    with tab4:
        tab_engagement(filtered)
