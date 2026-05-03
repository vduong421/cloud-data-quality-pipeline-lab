# Cloud Data Quality Pipeline Lab

Python and SQLite project for turning raw event data into validated, queryable, operations-ready pipeline outputs. This project supports data engineering, analytics engineering, backend data platform, and cloud pipeline workflows that require ETL, SQL, data quality, reporting, and operational monitoring.

## What It Does

- Loads sample application and system events from CSV
- Validates required fields, timestamp format, duplicate event IDs, and missing account IDs
- Writes clean events and rejected records into SQLite tables
- Produces daily event counts, account funnel counts, and data-quality metrics
- Writes JSON and Markdown summaries for pipeline review

## Run

```bash
python pipeline.py samples/events.csv
```

With local AI analyst enabled:

```bash
python pipeline.py samples/events.csv --use-ai
```

Outputs:

- `pipeline.db`
- `pipeline-summary.json`
- `pipeline-summary.md`
- `pipeline-ai-insights.json`
- `pipeline-ai-insights.md`

## Resume Angle

Built a Python/SQLite data-quality pipeline that validates raw event data, separates rejected records, computes funnel and daily activity metrics, and generates JSON/Markdown summaries for data engineering review.

## Project Workbench

Launch the production-style desktop workbench with:

```powershell
launch-workbench.bat
```

What it adds:

- Local-first AI copilot using `google/gemma-4-e4b` by default
- Operator-focused workbench for reviewing real project inputs and outputs
- System design, production-impact, and operational brief generation on demand
- Grounded responses based on this project's README, sample files, and deterministic outputs
