# Cloud Data Quality Pipeline Lab

Python and SQLite project for turning raw event data into validated, queryable, recruiter-readable pipeline outputs. This project supports data engineering, analytics engineering, backend data platform, and cloud pipeline roles that ask for ETL, SQL, data quality, reporting, and operational monitoring.

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

Outputs:

- `pipeline.db`
- `pipeline-summary.json`
- `pipeline-summary.md`

## Resume Angle

Built a Python/SQLite data-quality pipeline that validates raw event data, separates rejected records, computes funnel and daily activity metrics, and generates JSON/Markdown summaries for data engineering review.
