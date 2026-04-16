import datetime
import platform
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
REPORTS_DIR = REPO_ROOT / "reports"
LOG_FILE = REPORTS_DIR / "run_log.txt"


_SKIP_DIRS = {".git", ".venv", "venv", "env", "__pycache__", "build", "dist"}


def collect_stats(root: Path = REPO_ROOT) -> dict:
    """Return basic repo statistics as a dict."""
    py_files = [f for f in root.rglob("*.py") if not _SKIP_DIRS.intersection(f.parts)]
    all_files = [
        f
        for f in root.rglob("*")
        if f.is_file() and not _SKIP_DIRS.intersection(f.parts)
    ]
    return {
        "python_version": platform.python_version(),
        "python_files": len(py_files),
        "total_files": len(all_files),
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def format_entry(stats: dict) -> str:
    """Format stats dict into a single, grep-friendly log line."""
    return (
        f"[{stats['timestamp']}] "
        f"python={stats['python_version']} "
        f"py_files={stats['python_files']} "
        f"total_files={stats['total_files']} "
        f"status=ok\n"
    )


def write_report(entry: str, log_path: Path = LOG_FILE) -> None:
    """Append entry to the log file, creating parent directories as needed."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as fh:
        fh.write(entry)


def run(root: Path = REPO_ROOT, log_path: Path = LOG_FILE) -> str:
    """Collect stats, write to log, and return the formatted entry."""
    stats = collect_stats(root)
    entry = format_entry(stats)
    write_report(entry, log_path)
    return entry


if __name__ == "__main__":
    result = run()
    sys.stdout.write(result)
