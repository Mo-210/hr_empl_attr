"""One-command entry point: install deps and open the dashboard."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    bootstrap = ROOT / "scripts" / "bootstrap.py"
    subprocess.check_call([sys.executable, str(bootstrap)], cwd=str(ROOT))


if __name__ == "__main__":
    main()
