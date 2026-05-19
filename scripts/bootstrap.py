"""Install dependencies and launch the Streamlit dashboard."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIREMENTS = ROOT / "requirements.txt"
DASHBOARD = ROOT / "streamlit_app.py"


def install_requirements() -> None:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS)],
    )


def run_dashboard() -> None:
    subprocess.check_call(
        [sys.executable, "-m", "streamlit", "run", str(DASHBOARD)],
        cwd=str(ROOT),
    )


def main() -> None:
    print("Installing dependencies from requirements.txt ...")
    install_requirements()
    print("Starting dashboard ...")
    run_dashboard()


if __name__ == "__main__":
    main()
