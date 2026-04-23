#!/usr/bin/env python3
import csv
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


REQUIRED_FIELDS = ["event_id", "account_id", "event_type", "event_time"]


def valid_timestamp(value):
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate(row, seen_event_ids):
    errors = []
    for field in REQUIRED_FIELDS:
        if not row.get(field):
            errors.append(f"missing_{field}")
    if row.get("event_id") in seen_event_ids:
        errors.append("duplicate_event_id")
    if row.get("event_time") and not valid_timestamp(row["event_time"]):
        errors.append("invalid_event_time")
    return errors


def load_rows(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def reset_db(conn):
    conn.executescript(
        """
        DROP TABLE IF EXISTS clean_events;
        DROP TABLE IF EXISTS rejected_events;

        CREATE TABLE clean_events (
            event_id TEXT PRIMARY KEY,
            account_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            event_time TEXT NOT NULL,
            source TEXT
        );

        CREATE TABLE rejected_events (
            event_id TEXT,
            account_id TEXT,
            event_type TEXT,
            event_time TEXT,
            source TEXT,
            errors TEXT NOT NULL
        );
        """
    )


def write_db(conn, clean_rows, rejected_rows):
    conn.executemany(
        "INSERT INTO clean_events VALUES (:event_id, :account_id, :event_type, :event_time, :source)",
        clean_rows,
    )
    conn.executemany(
        "INSERT INTO rejected_events VALUES (:event_id, :account_id, :event_type, :event_time, :source, :errors)",
        rejected_rows,
    )
    conn.commit()


def summarize(clean_rows, rejected_rows):
    by_type = Counter(row["event_type"] for row in clean_rows)
    by_day = Counter(row["event_time"][:10] for row in clean_rows)
    account_funnel = defaultdict(set)
    for row in clean_rows:
        account_funnel[row["account_id"]].add(row["event_type"])

    return {
        "total_rows": len(clean_rows) + len(rejected_rows),
        "clean_rows": len(clean_rows),
        "rejected_rows": len(rejected_rows),
        "quality_rate": round(len(clean_rows) / (len(clean_rows) + len(rejected_rows)), 3) if clean_rows or rejected_rows else 0,
        "events_by_type": dict(by_type.most_common()),
        "events_by_day": dict(sorted(by_day.items())),
        "accounts_with_signup": sum(1 for events in account_funnel.values() if "signup" in events),
        "accounts_with_activation": sum(1 for events in account_funnel.values() if "activation" in events),
        "accounts_with_purchase": sum(1 for events in account_funnel.values() if "purchase" in events),
        "top_rejection_reasons": dict(Counter(row["errors"] for row in rejected_rows).most_common()),
    }


def write_markdown(summary):
    lines = [
        "# Pipeline Summary",
        "",
        f"- Total rows: {summary['total_rows']}",
        f"- Clean rows: {summary['clean_rows']}",
        f"- Rejected rows: {summary['rejected_rows']}",
        f"- Data quality rate: {summary['quality_rate']:.1%}",
        "",
        "## Events By Type",
    ]
    for key, value in summary["events_by_type"].items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Funnel Counts")
    lines.append(f"- Signup accounts: {summary['accounts_with_signup']}")
    lines.append(f"- Activated accounts: {summary['accounts_with_activation']}")
    lines.append(f"- Purchase accounts: {summary['accounts_with_purchase']}")
    lines.append("")
    lines.append("## Top Rejection Reasons")
    for key, value in summary["top_rejection_reasons"].items():
        lines.append(f"- {key}: {value}")
    Path("pipeline-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    input_path = Path(sys.argv[1] if len(sys.argv) > 1 else "samples/events.csv")
    rows = load_rows(input_path)
    seen = set()
    clean_rows = []
    rejected_rows = []

    for row in rows:
        errors = validate(row, seen)
        if row.get("event_id"):
            seen.add(row["event_id"])
        record = {key: row.get(key, "") for key in ["event_id", "account_id", "event_type", "event_time", "source"]}
        if errors:
            record["errors"] = ",".join(errors)
            rejected_rows.append(record)
        else:
            clean_rows.append(record)

    conn = sqlite3.connect("pipeline.db")
    reset_db(conn)
    write_db(conn, clean_rows, rejected_rows)
    conn.close()

    summary = summarize(clean_rows, rejected_rows)
    Path("pipeline-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_markdown(summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
