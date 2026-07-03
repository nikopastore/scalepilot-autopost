#!/usr/bin/env python3
"""Import reviewed Xquik/TweetClaw rows into content/trends.json."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


TEXT_FIELDS = (
    "text",
    "full_text",
    "tweetText",
    "tweet_text",
    "content",
    "body",
)
STATUS_FIELDS = ("status", "review_status", "approval_status")
APPROVED_STATUSES = {"approved", "published", "ready", "reviewed", "selected"}
BLOCKED_STATUSES = {
    "draft",
    "needs_review",
    "not_approved",
    "not_reviewed",
    "pending",
    "rejected",
    "unreviewed",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import reviewed Xquik/TweetClaw export rows as RSS content trends."
    )
    parser.add_argument("--input", required=True, help="CSV, JSON, or JSONL export path.")
    parser.add_argument("--output", default="content/trends.json", help="Trends JSON path.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum reviewed rows to import.")
    parser.add_argument(
        "--include-unreviewed",
        action="store_true",
        help="Include rows without an explicit approved/reviewed status.",
    )
    return parser.parse_args()


def normalize_status(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def row_is_reviewed(row: dict[str, Any], include_unreviewed: bool) -> bool:
    statuses = [normalize_status(row.get(field)) for field in STATUS_FIELDS]
    statuses = [status for status in statuses if status]
    if not statuses:
        return include_unreviewed
    return any(status in APPROVED_STATUSES for status in statuses) and not any(
        status in BLOCKED_STATUSES for status in statuses
    )


def first_text(row: dict[str, Any]) -> str:
    for field in TEXT_FIELDS:
        value = row.get(field)
        if isinstance(value, str) and value.strip():
            return " ".join(value.split())
    return ""


def flatten_items(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        for key in ("items", "tweets", "results", "data"):
            nested = value.get(key)
            if isinstance(nested, list):
                return [item for item in nested if isinstance(item, dict)]
        return [value]
    return []


def read_json(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonl":
        rows: list[dict[str, Any]] = []
        for line in text.splitlines():
            if line.strip():
                value = json.loads(line)
                if isinstance(value, dict):
                    rows.append(value)
        return rows
    return flatten_items(json.loads(text))


def read_rows(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() in {".json", ".jsonl"}:
        return read_json(path)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def load_trends(path: Path) -> dict[str, list[dict[str, str]]]:
    if not path.exists():
        return {"items": []}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("items"), list):
        raise ValueError(f"{path} must contain an object with an items list.")
    return value


def trend_title(text: str) -> str:
    title = text.strip()
    return title[:117].rstrip() + "..." if len(title) > 120 else title


def import_trends(input_path: Path, output_path: Path, limit: int, include_unreviewed: bool) -> int:
    rows = read_rows(input_path)
    trends = load_trends(output_path)
    existing = {str(item.get("title", "")).strip() for item in trends["items"]}
    imported = 0
    for row in rows:
        if imported >= limit:
            break
        if not row_is_reviewed(row, include_unreviewed):
            continue
        title = trend_title(first_text(row))
        if not title or title in existing:
            continue
        trends["items"].append({"title": title, "source": "xquik"})
        existing.add(title)
        imported += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(trends, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return imported


def main() -> None:
    args = parse_args()
    count = import_trends(Path(args.input), Path(args.output), args.limit, args.include_unreviewed)
    print(f"Imported {count} Xquik/TweetClaw trends into {args.output}")


if __name__ == "__main__":
    main()
