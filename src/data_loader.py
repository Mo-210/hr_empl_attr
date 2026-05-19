from pathlib import Path

import pandas as pd

from src.config import (
    AGE_BINS,
    AGE_LABELS,
    DATA_PATH,
    EXPERIENCE_BINS,
    EXPERIENCE_LABELS,
    SATISFACTION_MAP,
)


def load_hr_data(path: Path | str | None = None) -> pd.DataFrame:
    """Load the HR dataset and add derived columns used across analysis."""
    file_path = Path(path) if path else DATA_PATH
    df = pd.read_excel(file_path)

    df["Attrition Flag"] = (df["Attrition"] == "Yes").astype(int)
    df["Age Group"] = pd.cut(
        df["Age"], bins=AGE_BINS, labels=AGE_LABELS, right=True
    )
    df["Experience Group"] = pd.cut(
        df["Total Working Years"],
        bins=EXPERIENCE_BINS,
        labels=EXPERIENCE_LABELS,
        right=False,
    )
    df["Satisfaction Label"] = df["Job Satisfaction"].map(SATISFACTION_MAP)

    return df
