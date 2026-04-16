# Contributing

Thank you for your interest in contributing! Please read this document before opening a PR.

## Ethics Policy — History Integrity

> **Do not modify commit dates or rewrite history prior to 2025.**

Specifically:
- Do **not** set `GIT_AUTHOR_DATE` or `GIT_COMMITTER_DATE` in any workflow, script, or manual command.
- Do **not** use `git commit --amend` to alter timestamps of existing commits.
- Do **not** use `git push --force` or `git rebase` to rewrite published history.
- Automated commits (via GitHub Actions) must use the real wall-clock time of the runner. No timestamp overrides of any kind.
- No fake author identities. Automated commits must use `github-actions[bot]`.

Violations of this policy will result in PRs being closed without merge.

## Pull Request Guidelines

1. **One concern per PR** — keep diffs small and focused.
2. **Branch naming** — `feat/<short-description>`, `fix/<short-description>`, or `chore/<short-description>`.
3. **Commit messages** — use [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat(scope): description`
   - `fix(scope): description`
   - `chore(scope): description`
4. **Tests required** — every change to `scripts/` must have corresponding tests in `tests/`.
5. **CI must pass** — all of `black --check`, `flake8`, and `pytest -q` must be green before merge.

## Local Development

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt

# Format check
black --check .

# Lint
flake8 scripts/ tests/

# Tests
pytest -q
```

## Scheduled Maintenance Workflow

The `scheduled-maintenance.yml` workflow runs daily and commits `reports/run_log.txt` updates with real timestamps. To disable it locally for testing, you can comment out the `schedule:` trigger in a feature branch. Do not merge that change to `main`.
