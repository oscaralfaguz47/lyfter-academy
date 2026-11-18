""" Run the test suite and save a short report. """
import subprocess
import sys
from pathlib import Path

REPORT = Path(__file__).resolve().parent.parent / "reports" / "test-report.txt"


def main() -> int:
    REPORT.parent.mkdir(exist_ok=True)
    result = subprocess.run([sys.executable, "-m", "pytest", "-rA"], capture_output=True, text=True)
    REPORT.write_text(result.stdout + result.stderr, encoding="utf-8")
    print(result.stdout)
    print(f"Report written to {REPORT}")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())