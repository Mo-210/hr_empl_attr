from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "hr_employee_attrition.xlsx"

LIVE_APP_URL = "https://hremplattr-irq6o2otusuc9f79adb7sc.streamlit.app/"
GITHUB_REPO_URL = "https://github.com/Mo-210/hr_empl_attr"

EXPERIENCE_BINS = [0, 2, 5, 10, 15, 20, 30, 40]
EXPERIENCE_LABELS = ["0-2", "3-5", "6-10", "11-15", "16-20", "21-30", "30+"]

AGE_BINS = [18, 25, 30, 35, 45, 55, 100]
AGE_LABELS = ["18-25", "26-30", "31-35", "36-45", "46-55", "56+"]

SATISFACTION_MAP = {1: "Very Low", 2: "Low", 3: "Neutral", 4: "High"}

CHART_COLORS = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B", "#95C623"]
PLOTLY_TEMPLATE = "plotly_white"
