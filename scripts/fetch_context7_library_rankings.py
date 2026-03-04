#!/usr/bin/env python3
"""Fetch Context7 library rankings (popular/trending/latest/all) and export CSV.

Useful for generating the "popular docs" table with fields like:
source, tokens, snippets, update.
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
DEFAULT_KIND = "popular"
DEFAULT_LIMIT = 20
DEFAULT_MAX_PAGES = 1000


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


def parse_dt(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    v = value.strip()
    # Examples seen:
    # - 2026-03-03T01:36:19.617Z
    # - 2025-04-23
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(v)
    except ValueError:
        # Date-only fallback.
        try:
            dt = datetime.fromisoformat(v + "T00:00:00+00:00")
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def human_age(dt: datetime | None, now: datetime) -> str:
    if dt is None:
        return ""
    sec = int((now - dt).total_seconds())
    if sec < 0:
        return "0m"
    if sec < 3600:
        m = max(1, sec // 60)
        return f"{m}m"
    if sec < 86400:
        h = sec // 3600
        return f"{h}h"
    if sec < 86400 * 30:
        d = sec // 86400
        return f"{d}d"
    if sec < 86400 * 365:
        mo = sec // (86400 * 30)
        return f"{mo}mo"
    y = sec // (86400 * 365)
    return f"{y}y"


def iter_all_pages(base_url: str, max_pages: int) -> tuple[list[dict[str, Any]], int, int | None]:
    rows: list[dict[str, Any]] = []
    page = 1
    calls = 0
    total_count: int | None = None

    for _ in range(max_pages):
        url = f"{base_url.rstrip('/')}/api/libraries/all?page={page}"
        payload = fetch_json(url)
        calls += 1
        libs = payload.get("libraries", []) if isinstance(payload, dict) else []
        if not isinstance(libs, list) or not libs:
            break
        rows.extend([lib for lib in libs if isinstance(lib, dict)])

        total_pages = payload.get("totalPages") if isinstance(payload, dict) else None
        total_count = payload.get("totalCount") if isinstance(payload, dict) else None
        if isinstance(total_pages, int) and page >= total_pages:
            break
        page += 1
    return rows, calls, total_count


def flatten_library(item: dict[str, Any], rank: int, now: datetime) -> dict[str, Any]:
    settings = item.get("settings") if isinstance(item.get("settings"), dict) else {}
    version = item.get("version") if isinstance(item.get("version"), dict) else {}

    source = settings.get("project") or ""
    title = settings.get("title") or source
    trust_score = settings.get("trustScore")
    verified = settings.get("verified")
    popularity_rank = settings.get("popularityRank")
    benchmark_score = version.get("benchmarkScore")

    total_tokens = version.get("totalTokens")
    total_snippets = version.get("totalSnippets")

    last_update_raw = (
        version.get("lastUpdateDate")
        or version.get("lastRunDate")
        or version.get("parseDate")
        or version.get("lastUpdate")
    )
    dt = parse_dt(last_update_raw)
    update_iso = dt.isoformat().replace("+00:00", "Z") if dt else ""

    return {
        "rank": rank,
        "title": title,
        "source": source,
        "type": settings.get("type") or "",
        "tokens": total_tokens,
        "snippets": total_snippets,
        "updateUtc": update_iso,
        "updateAgo": human_age(dt, now),
        "trustScore": trust_score,
        "verified": verified,
        "popularityRank": popularity_rank,
        "benchmarkScore": benchmark_score,
        "docsRepoUrl": settings.get("docsRepoUrl") or "",
        "docsSiteUrl": settings.get("docsSiteUrl") or settings.get("docsSiteInputUrl") or "",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch Context7 docs library rankings and export CSV/JSON metadata."
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Context7 base URL")
    parser.add_argument(
        "--kind",
        default=DEFAULT_KIND,
        choices=["popular", "trending", "latest", "all"],
        help="Ranking source kind (default: popular)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help="Only for kind=latest: limit row count (default: 20)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=DEFAULT_MAX_PAGES,
        help="Only for kind=all: max pages to fetch (default: 1000)",
    )
    parser.add_argument(
        "--output-csv",
        default="data/context7_popular_libraries.csv",
        help="Output CSV path",
    )
    parser.add_argument(
        "--output-json",
        default="data/context7_popular_libraries.meta.json",
        help="Output metadata JSON path",
    )
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    kind = args.kind
    now = datetime.now(timezone.utc)

    rows_raw: list[dict[str, Any]] = []
    api_calls = 0
    total_count: int | None = None

    if kind in {"popular", "trending"}:
        url = f"{base}/api/libraries/homepage?{urlencode({'type': kind})}"
        payload = fetch_json(url)
        api_calls = 1
        if not isinstance(payload, list):
            raise RuntimeError(f"Unexpected payload from {url}: expected list")
        rows_raw = [x for x in payload if isinstance(x, dict)]
    elif kind == "latest":
        limit = max(1, min(int(args.limit), 100))
        url = f"{base}/api/libraries/latest?{urlencode({'limit': limit})}"
        payload = fetch_json(url)
        api_calls = 1
        if not isinstance(payload, list):
            raise RuntimeError(f"Unexpected payload from {url}: expected list")
        rows_raw = [x for x in payload if isinstance(x, dict)]
    elif kind == "all":
        rows_raw, api_calls, total_count = iter_all_pages(base, max_pages=max(1, int(args.max_pages)))
    else:
        raise RuntimeError(f"Unsupported kind: {kind}")

    rows = [flatten_library(item, idx, now) for idx, item in enumerate(rows_raw, start=1)]

    out_csv = Path(args.output_csv)
    out_json = Path(args.output_json)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    headers = [
        "rank",
        "title",
        "source",
        "type",
        "tokens",
        "snippets",
        "updateUtc",
        "updateAgo",
        "trustScore",
        "verified",
        "popularityRank",
        "benchmarkScore",
        "docsRepoUrl",
        "docsSiteUrl",
    ]
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    count_url = f"{base}/api/libraries/count"
    count_payload = fetch_json(count_url)
    api_total_count = count_payload.get("count") if isinstance(count_payload, dict) else None

    meta = {
        "generatedAtUtc": now.isoformat(),
        "baseUrl": base,
        "kind": kind,
        "apiTotalLibraries": api_total_count,
        "allEndpointTotalCount": total_count,
        "apiCalls": api_calls + 1,  # include count endpoint call
        "rowsKept": len(rows),
        "outputCsv": str(out_csv),
    }
    out_json.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Done. kind={kind}, rows={len(rows)}, api_calls={meta['apiCalls']}")
    print(f"CSV:  {out_csv}")
    print(f"META: {out_json}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
