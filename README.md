# Cloud Data Quality Pipeline Lab

Cloud Data Quality Pipeline Lab is a local data-platform tool that validates incoming event records, separates clean and rejected rows, calculates pipeline quality metrics, and produces AI-assisted operational insight for data quality review.

The project models a production data pipeline pattern: deterministic validation remains the source of truth, while a local AI analyst explains data quality risks, likely root causes, and next actions for operators.

## What It Does

- Reads raw events from CSV.
- Validates required fields, duplicate IDs, event timestamps, and account lifecycle consistency.
- Splits records into accepted and rejected outputs.
- Computes funnel metrics and rejection categories.
- Writes JSON and Markdown summaries for review.
- Shows results in a small local web dashboard.

## AI Features

- Local AI analyst for data quality summaries.
- Converts validation metrics into operational recommendations.
- Highlights the most likely source of rejected records.
- Produces a concise explanation suitable for pipeline handoff or daily review.

The AI analysis is generated from deterministic metrics only, so the model explains evidence instead of inventing new numbers.

## Architecture

```text
samples/events.csv
        |
        v
Validation pipeline -> accepted/rejected records -> summary metrics
        |
        v
Local AI analyst -> root-cause summary + next actions
        |
        v
pipeline-summary.json / pipeline-ai-insights.json / browser dashboard
```

## Run

```powershell
run.bat
```

The script installs dependencies, runs the pipeline, and opens the local dashboard.

## Local AI Setup

- Default local endpoint: `http://127.0.0.1:1234/v1/chat/completions`
- Recommended local model: `google/gemma-4-e4b` or another small OpenAI-compatible model.

If the local AI server is unavailable, the pipeline still produces deterministic summary files.

## Main Files

- `pipeline.py` - validation rules, metrics, and AI insight generation.
- `samples/events.csv` - sample event stream.
- `web/app.py` - local dashboard server.
- `pipeline-summary.json` - deterministic quality metrics.
- `pipeline-ai-insights.json` - AI-generated explanation.

## Output

The project produces accepted/rejected record counts, rejection reasons, funnel metrics, AI insight, and Markdown summaries that can be reviewed or attached to a data quality report.
