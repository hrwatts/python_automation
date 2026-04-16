import re

from scripts.maintenance import collect_stats, format_entry, run, write_report


# ---------------------------------------------------------------------------
# collect_stats
# ---------------------------------------------------------------------------


def test_collect_stats_has_required_keys():
    stats = collect_stats()
    for key in ("python_version", "python_files", "total_files", "timestamp"):
        assert key in stats


def test_collect_stats_types():
    stats = collect_stats()
    assert isinstance(stats["python_files"], int)
    assert isinstance(stats["total_files"], int)
    assert isinstance(stats["python_version"], str)
    assert isinstance(stats["timestamp"], str)


def test_collect_stats_excludes_skip_dirs(tmp_path):
    # A .venv py file should be ignored
    venv_py = tmp_path / ".venv" / "lib" / "site.py"
    venv_py.parent.mkdir(parents=True)
    venv_py.write_text("# venv internal\n")
    # A real source py file should be counted
    real_py = tmp_path / "src" / "app.py"
    real_py.parent.mkdir()
    real_py.write_text("pass\n")

    stats = collect_stats(tmp_path)
    assert stats["python_files"] == 1


# ---------------------------------------------------------------------------
# format_entry
# ---------------------------------------------------------------------------


def test_format_entry_contains_supplied_timestamp():
    stats = {
        "timestamp": "2025-01-01T00:00:00Z",
        "python_version": "3.11.0",
        "python_files": 3,
        "total_files": 10,
    }
    entry = format_entry(stats)
    assert "2025-01-01T00:00:00Z" in entry
    assert "python=3.11.0" in entry
    assert "py_files=3" in entry
    assert "total_files=10" in entry
    assert "status=ok" in entry
    assert entry.endswith("\n")


def test_format_entry_does_not_inject_env_vars():
    """format_entry must not embed GIT_AUTHOR_DATE or GIT_COMMITTER_DATE."""
    stats = {
        "timestamp": "2030-06-15T12:00:00Z",
        "python_version": "3.12.0",
        "python_files": 1,
        "total_files": 5,
    }
    entry = format_entry(stats)
    assert "GIT_AUTHOR_DATE" not in entry
    assert "GIT_COMMITTER_DATE" not in entry
    assert "2030-06-15T12:00:00Z" in entry


def test_format_entry_matches_log_pattern():
    stats = {
        "timestamp": "2025-07-04T08:30:00Z",
        "python_version": "3.11.9",
        "python_files": 5,
        "total_files": 20,
    }
    entry = format_entry(stats)
    pattern = (
        r"\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\] "
        r"python=\S+ py_files=\d+ total_files=\d+ status=ok"
    )
    assert re.search(pattern, entry)


# ---------------------------------------------------------------------------
# write_report
# ---------------------------------------------------------------------------


def test_write_report_creates_file_and_parent_dirs(tmp_path):
    log = tmp_path / "nested" / "dir" / "run_log.txt"
    write_report("first entry\n", log)
    assert log.exists()
    assert log.read_text(encoding="utf-8") == "first entry\n"


def test_write_report_appends(tmp_path):
    log = tmp_path / "run_log.txt"
    write_report("line1\n", log)
    write_report("line2\n", log)
    content = log.read_text(encoding="utf-8")
    assert "line1" in content
    assert "line2" in content
    assert content.count("\n") == 2


# ---------------------------------------------------------------------------
# run (integration)
# ---------------------------------------------------------------------------


def test_run_writes_entry_to_log(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    (root / "module.py").write_text("pass\n")
    log = tmp_path / "run_log.txt"

    entry = run(root=root, log_path=log)

    assert log.exists()
    written = log.read_text(encoding="utf-8")
    assert written == entry


def test_run_output_matches_log_format(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    log = tmp_path / "run_log.txt"

    entry = run(root=root, log_path=log)
    pattern = (
        r"\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\] "
        r"python=\S+ py_files=\d+ total_files=\d+ status=ok"
    )
    assert re.search(pattern, entry), f"Unexpected format: {entry!r}"


def test_run_appends_on_repeated_calls(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    log = tmp_path / "run_log.txt"

    run(root=root, log_path=log)
    run(root=root, log_path=log)

    lines = [ln for ln in log.read_text(encoding="utf-8").splitlines() if ln]
    assert len(lines) == 2


def test_run_counts_py_files_accurately(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    (root / "a.py").write_text("pass\n")
    (root / "b.py").write_text("pass\n")
    (root / "c.txt").write_text("text\n")
    log = tmp_path / "run_log.txt"

    entry = run(root=root, log_path=log)
    assert "py_files=2" in entry
    assert "total_files=3" in entry
