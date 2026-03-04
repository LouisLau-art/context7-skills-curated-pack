#!/usr/bin/env python3
"""Build a Figma-related skills watchlist from ranked-all dataset."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_INPUT_JSON = "docs/data/context7_skills_ranked_all.json"
DEFAULT_SELECTED = "skills_selected.txt"
DEFAULT_PATTERN = "figma"
DEFAULT_OUTPUT_JSON = "docs/data/context7_figma_watchlist.json"
DEFAULT_OUTPUT_CSV = "docs/data/context7_figma_watchlist.csv"


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"Expected JSON object in {path}")
    items = payload.get("items")
    if not isinstance(items, list):
        raise RuntimeError(f"Missing list field 'items' in {path}")
    return payload


def load_selected(path: Path) -> set[str]:
    slugs: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        item = line.strip()
        if item and not item.startswith("#"):
            slugs.add(item)
    return slugs


def as_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a Figma-related watchlist from ranked Context7 skills data."
    )
    parser.add_argument("--input-json", default=DEFAULT_INPUT_JSON)
    parser.add_argument("--selected-list", default=DEFAULT_SELECTED)
    parser.add_argument("--pattern", default=DEFAULT_PATTERN, help="Regex keyword pattern")
    parser.add_argument("--max-rows", type=int, default=0, help="0 means no limit")
    parser.add_argument("--output-json", default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-csv", default=DEFAULT_OUTPUT_CSV)
    args = parser.parse_args()

    input_json = Path(args.input_json)
    selected_list = Path(args.selected_list)
    out_json = Path(args.output_json)
    out_csv = Path(args.output_csv)

    payload = load_json(input_json)
    selected = load_selected(selected_list)
    pattern = re.compile(args.pattern, re.IGNORECASE)

    rows: list[dict[str, Any]] = []
    for item in payload["items"]:
        if not isinstance(item, dict):
            continue
        text = " ".join(
            [
                str(item.get("name", "")),
                str(item.get("source", "")),
                str(item.get("url", "")),
            ]
        )
        if not pattern.search(text):
            continue

        name = str(item.get("name", ""))
        row = {
            "rank": item.get("rank"),
            "name": name,
            "source": item.get("source", ""),
            "installCount": item.get("installCount"),
            "trustScore": item.get("trustScore"),
            "verified": item.get("verified"),
            "benchmarkScore": item.get("benchmarkScore"),
            "url": item.get("url", ""),
            "inCurated": name in selected,
        }
        rows.append(row)

    rows.sort(key=lambda r: as_int(r.get("rank")) if as_int(r.get("rank")) is not None else 10**12)
    if args.max_rows and args.max_rows > 0:
        rows = rows[: args.max_rows]

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    headers = [
        "rank",
        "name",
        "source",
        "installCount",
        "trustScore",
        "verified",
        "benchmarkScore",
        "inCurated",
        "url",
    ]
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    meta = {
        "generatedAtUtc": datetime.now(timezone.utc).isoformat(),
        "sourceDataset": str(input_json),
        "selectedList": str(selected_list),
        "pattern": args.pattern,
        "rows": len(rows),
        "inCuratedCount": sum(1 for r in rows if r.get("inCurated")),
        "items": rows,
    }
    out_json.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        f"Done. rows={len(rows)} in_curated={meta['inCuratedCount']} pattern={args.pattern!r}"
    )
    print(f"JSON: {out_json}")
    print(f"CSV:  {out_csv}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
