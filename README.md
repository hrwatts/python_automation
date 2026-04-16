# Python Automation

![CI](https://github.com/hrwatts/python_automation/actions/workflows/ci.yml/badge.svg)

A tool for automatically managing pull requests on GitHub. The repo also includes a scheduled CI/maintenance pipeline that commits real, timestamped run reports on a daily schedule.

## Local Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
pytest -q
```

## Automated Maintenance

A GitHub Actions workflow (`scheduled-maintenance.yml`) runs daily at UTC midnight. It executes `scripts/maintenance.py`, which appends a timestamped entry to `reports/run_log.txt` containing Python version, file counts, and run status. If the file changed, the workflow commits and pushes with a real timestamp from the Actions runner — no dates are forged or overridden.

To opt out of scheduled runs, disable the workflow under **Actions → Scheduled Maintenance → ⋯ → Disable workflow** in the GitHub UI.

## Features

- Automatic pull-request analysis and merging
- Daily maintenance commits via GitHub Actions
- Full pytest suite with CI gate on push/PR
- `black` formatting and `flake8` linting enforced in CI

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines, the ethics policy, and the PR checklist.

## License

This project is licensed under consideration.
