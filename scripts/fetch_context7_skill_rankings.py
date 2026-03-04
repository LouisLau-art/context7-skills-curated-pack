#!/usr/bin/env python3
"""Fetch Context7 ranked skills and export a filtered snapshot.

By default this pulls the live ranked skills list from:
  - /api/skills/count
  - /api/skills/ranked?limit=<N>&offset=<N>

Then keeps rows where installCount >= --min-installs (default: 36).
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


DEFAULT_BASE_URL = "https://context7.com"
DEFAULT_LIMIT = 100  # API currently caps at 100
DEFAULT_MIN_INSTALLS = 36
DEFAULT_MAX_PAGES = 500


def fetch_json(url: str, timeout: int = 30) -> Any:
    try:
        with urlopen(url, timeout=timeout) as resp:  # nosec B310 (trusted host input)
            payload = resp.read().decode("utf-8")
            return json.loads(payload)
    except HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} for {url}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error for {url}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON from {url}") from exc


def to_number(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def build_ranked_url(base_url: str, limit: int, offset: int) -> str:
    query = urlencode({"limit": limit, "offset": offset})
    return f"{base_url.rstrip('/')}/api/skills/ranked?{query}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch Context7 ranked skills and export installs-filtered snapshot."
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Context7 base URL")
    parser.add_argument(
        "--min-installs",
        type=int,
        default=DEFAULT_MIN_INSTALLS,
        help=f"Keep skills with installCount >= this value (default: {DEFAULT_MIN_INSTALLS})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Page size for /api/skills/ranked (default: {DEFAULT_LIMIT})",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=DEFAULT_MAX_PAGES,
        help=f"Safety cap for number of paginated calls (default: {DEFAULT_MAX_PAGES})",
    )
    parser.add_argument(
        "--output-csv",
        default="data/context7_ranked_skills_min36.csv",
        help="Output CSV path",
    )
    parser.add_argument(
        "--output-json",
        default="data/context7_ranked_skills_min36.meta.json",
        help="Output metadata JSON path",
    )
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    limit = max(1, min(int(args.limit), 100))  # API cap observed at 100
    min_installs = int(args.min_installs)
    max_pages = max(1, int(args.max_pages))

    count_url = f"{base_url}/api/skills/count"
    count_payload = fetch_json(count_url)
    total_count = count_payload.get("count") if isinstance(count_payload, dict) else None

    all_rows: list[dict[str, Any]] = []
    calls = 0
    offset = 0

    for _ in range(max_pages):
        ranked_url = build_ranked_url(base_url, limit, offset)
        page = fetch_json(ranked_url)
        calls += 1

        if not isinstance(page, list):
            raise RuntimeError(f"Unexpected payload from {ranked_url}: expected list")
        if not page:
            break

        # Keep all rows for this page so we can build a deterministic filtered snapshot.
        for idx, item in enumerate(page, start=1):
            if not isinstance(item, dict):
                continue
            row = {
                "rank": offset + idx,
                "name": item.get("name", ""),
                "source": item.get("project", ""),
                "installCount": item.get("installCount"),
                "trustScore": item.get("trustScore"),
                "verified": item.get("verified"),
                "benchmarkScore": item.get("benchmarkScore"),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
            }
            all_rows.append(row)

        installs = [to_number(item.get("installCount")) for item in page if isinstance(item, dict)]
        installs = [x for x in installs if x is not None]
        if installs and max(installs) < float(min_installs):
            break

        offset += limit

    filtered = [
        row
        for row in all_rows
        if (to_number(row.get("installCount")) is not None)
        and (to_number(row.get("installCount")) >= float(min_installs))
    ]

    # Stable order by rank from API (already ordered).
    filtered.sort(key=lambda x: int(x["rank"]))

    out_csv = Path(args.output_csv)
    out_json = Path(args.output_json)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    headers = [
        "rank",
        "name",
        "source",
        "installCount",
        "trustScore",
        "verified",
        "benchmarkScore",
        "url",
        "description",
    ]
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(filtered)

    meta = {
        "generatedAtUtc": datetime.now(timezone.utc).isoformat(),
        "baseUrl": base_url,
        "countEndpoint": f"{base_url}/api/skills/count",
        "rankedEndpoint": f"{base_url}/api/skills/ranked",
        "apiTotalCount": total_count,
        "apiCalls": calls,
        "pageLimit": limit,
        "minInstalls": min_installs,
        "rowsFetched": len(all_rows),
        "rowsKept": len(filtered),
        "outputCsv": str(out_csv),
    }
    out_json.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        f"Done. kept={len(filtered)} (min_installs>={min_installs}), "
        f"fetched={len(all_rows)}, api_calls={calls}"
    )
    print(f"CSV:  {out_csv}")
    print(f"META: {out_json}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
