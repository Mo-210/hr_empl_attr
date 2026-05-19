import pandas as pd


def attrition_rate(df: pd.DataFrame) -> float:
    """Fraction of rows where Attrition = Yes."""
    if len(df) == 0:
        return 0.0
    return float(df["Attrition Flag"].mean())


def summary_kpis(df: pd.DataFrame) -> dict[str, float | int]:
    """Top-line counts for the dashboard header."""
    left = int(df["Attrition Flag"].sum())
    return {
        "total_employees": len(df),
        "attrition_count": left,
        "attrition_rate_pct": round(attrition_rate(df) * 100, 1),
        "avg_age": float(round(df["Age"].mean(), 1)),
        "avg_years_at_company": float(round(df["Years At Company"].mean(), 1)),
        "avg_monthly_income": int(round(df["Monthly Income"].mean(), 0)),
    }


def attrition_by_column(
    df: pd.DataFrame, column: str, among_attrited_only: bool = False
) -> pd.DataFrame:
    """
    Count and share of attrition grouped by a categorical column.

    When among_attrited_only is True, percentages are share of all leavers
    (matching the exploratory notebook). Otherwise, attrition rate is computed
    within each group.
    """
    if among_attrited_only:
        subset = df[df["Attrition"] == "Yes"]
        counts = subset[column].value_counts()
        total = len(subset)
        result = pd.DataFrame(
            {
                "category": counts.index,
                "count": counts.values,
                "share_pct": (counts.values / total * 100).round(1),
            }
        )
        result["metric"] = "share_of_attrited"
        return result.sort_values("count", ascending=False).reset_index(drop=True)

    grouped = (
        df.groupby(column, observed=True)
        .agg(headcount=("Attrition Flag", "count"), attrition=("Attrition Flag", "sum"))
        .reset_index()
    )
    grouped.rename(columns={column: "category"}, inplace=True)
    grouped["attrition_rate_pct"] = (
        grouped["attrition"] / grouped["headcount"] * 100
    ).round(1)
    grouped["metric"] = "attrition_rate"
    return grouped.sort_values("attrition_rate_pct", ascending=False).reset_index(
        drop=True
    )


def filter_dataframe(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Sidebar multiselects — empty list means no filter."""
    filtered = df.copy()
    for column, values in filters.items():
        if values:
            filtered = filtered[filtered[column].isin(values)]
    return filtered
