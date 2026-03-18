#!/usr/bin/env python3
"""Fetch prerendered leaderboard data from skills.sh for static site usage."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "https://skills.sh"
DEFAULT_VIEW = "all-time"
DEFAULT_LIMIT = 600
DEFAULT_OUT_JSON = "docs/data/skills_sh_all_time_top600.json"
DEFAULT_OUT_CSV = "docs/data/skills_sh_all_time_top600.csv"

VIEW_PATHS = {
    "all-time": "/",
    "trending": "/trending",
    "hot": "/hot",
}


def fetch_html(url: str, timeout: int = 30) -> str:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=timeout) as resp:  # nosec B310 (trusted host input)
        return resp.read().decode("utf-8", "ignore")


def extract_initial_skills(html: str) -> tuple[list[dict], dict[str, int | str | None]]:
    needle = '\\"initialSkills\\":['
    meta_marker = '],\\"totalSkills\\":'
    start = html.find(needle)
    if start == -1:
        raise RuntimeError("skills.sh payload missing initialSkills marker")
    end = html.find(meta_marker, start)
    if end == -1:
        raise RuntimeError("skills.sh payload missing totalSkills marker")

    array_text = html[start + len(needle) - 1 : end + 1]
    try:
        items = json.loads(array_text.replace('\\"', '"'))
    except json.JSONDecodeError as exc:
        raise RuntimeError("failed to decode skills.sh initialSkills payload") from exc

    meta_start = end + 2
    meta_end = html.find("}]", meta_start)
    if meta_end == -1:
        raise RuntimeError("skills.sh payload missing metadata terminator")
    meta_text = "{" + html[meta_start:meta_end + 1].replace('\\"', '"')
    try:
        meta = json.loads(meta_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError("failed to decode skills.sh payload metadata") from exc

    return items, meta


def normalize_source(value: str) -> str:
    value = value.strip().strip("/")
    return f"/{value}" if value else ""


def build_view_url(base_url: str, view: str) -> str:
    path = VIEW_PATHS[view]
    return f"{base_url.rstrip('/')}{path}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch skills.sh leaderboard snapshot.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument(
        "--view",
        choices=sorted(VIEW_PATHS),
        default=DEFAULT_VIEW,
        help="Leaderboard view to fetch.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help="How many rows to keep from the prerendered payload.",
    )
    parser.add_argument("--output-json", default=DEFAULT_OUT_JSON)
    parser.add_argument("--output-csv", default=DEFAULT_OUT_CSV)
    args = parser.parse_args()

    source_url = build_view_url(args.base_url, args.view)
    html = fetch_html(source_url)
    raw_items, meta = extract_initial_skills(html)
    keep = max(1, int(args.limit))

    rows: list[dict[str, object]] = []
    for idx, item in enumerate(raw_items[:keep], start=1):
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or item.get("skillId") or "").strip()
        source = normalize_source(str(item.get("source") or ""))
        skill_id = str(item.get("skillId") or name).strip()
        detail_path = f"{source.lstrip('/')}/{skill_id}" if source and skill_id else ""
        rows.append(
            {
                "rank": idx,
                "name": name,
                "skillId": skill_id,
                "source": source,
                "installCount": item.get("installs"),
                "detailPath": detail_path,
                "detailUrl": f"{args.base_url.rstrip('/')}/{detail_path}" if detail_path else "",
            }
        )

    out_json = Path(args.output_json)
    out_csv = Path(args.output_csv)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    headers = ["rank", "name", "skillId", "source", "installCount", "detailPath", "detailUrl"]
    with out_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    payload = {
        "generatedAtUtc": datetime.now(timezone.utc).isoformat(),
        "baseUrl": args.base_url.rstrip("/"),
        "sourceUrl": source_url,
        "view": meta.get("view") or args.view,
        "rows": len(rows),
        "sourceRows": len(raw_items),
        "totalSkills": meta.get("totalSkills"),
        "allTimeTotal": meta.get("allTimeTotal"),
        "items": rows,
    }
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        "Done. "
        f"view={payload['view']} rows={payload['rows']} sourceRows={payload['sourceRows']} "
        f"totalSkills={payload['totalSkills']}"
    )
    print(f"JSON: {out_json}")
    print(f"CSV:  {out_csv}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, HTTPError, URLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
