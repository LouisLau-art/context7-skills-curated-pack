#!/usr/bin/env python3
"""Fetch Context7 docs popular rankings and export enriched CSV/JSON.

Data source:
- GET /api/rankings (top libraries by market share)
- GET /api/libraries/{libraryId} (details per library)
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen

from context7_auth import build_context7_request


DEFAULT_BASE_URL = "https://context7.com"
DEFAULT_LIMIT = 50
DEFAULT_OUTPUT_JSON = "docs/data/context7_docs_popular_top50.json"
DEFAULT_OUTPUT_CSV = "docs/data/context7_docs_popular_top50.csv"
DEFAULT_RETRIES = 6
MAX_RETRY_AFTER_SECONDS = 120.0


def build_request(url: str):
    return build_context7_request(url)


def fetch_json(url: str, timeout: int = 30, retries: int = DEFAULT_RETRIES) -> Any:
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = build_request(url)
            with urlopen(req, timeout=timeout) as resp:  # nosec B310 (trusted host input)
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as exc:
            last_err = exc
            if attempt < retries:
                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                if retry_after and retry_after.strip().isdigit():
                    retry_after_s = float(retry_after.strip())
                    # Fail fast on long cooldown windows so refresh jobs don't appear hung.
                    if retry_after_s > MAX_RETRY_AFTER_SECONDS:
                        raise RuntimeError(
                            f"HTTP {exc.code} for {url}: Retry-After={int(retry_after_s)}s "
                            f"exceeds cap {int(MAX_RETRY_AFTER_SECONDS)}s"
                        ) from exc
                    sleep_s = retry_after_s
                elif exc.code == 429:
                    sleep_s = min(60.0, 1.5 * (2 ** (attempt - 1)))
                else:
                    sleep_s = 0.4 * attempt
                sleep_s += random.uniform(0.0, 0.25)
                time.sleep(sleep_s)
            continue
        except (URLError, json.JSONDecodeError) as exc:
            last_err = exc
            if attempt < retries:
                time.sleep(0.4 * attempt)
            continue

    if isinstance(last_err, HTTPError):
        raise RuntimeError(f"HTTP {last_err.code} for {url}") from last_err
    if isinstance(last_err, URLError):
        raise RuntimeError(f"Network error for {url}: {last_err}") from last_err
    if isinstance(last_err, json.JSONDecodeError):
        raise RuntimeError(f"Invalid JSON from {url}") from last_err
    raise RuntimeError(f"Failed to fetch {url}")


def parse_dt(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        try:
            dt = datetime.fromisoformat(raw + "T00:00:00+00:00")
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
        return f"{max(1, sec // 60)}m"
    if sec < 86400:
        return f"{sec // 3600}h"
    if sec < 86400 * 30:
        return f"{sec // 86400}d"
    if sec < 86400 * 365:
        return f"{sec // (86400 * 30)}mo"
    return f"{sec // (86400 * 365)}y"


def library_detail_url(base_url: str, library_id: str) -> str:
    encoded = quote(library_id, safe="")
    return f"{base_url.rstrip('/')}/api/libraries/{encoded}"


def flatten_item(
    rank_item: dict[str, Any], detail: dict[str, Any] | None, now: datetime
) -> dict[str, Any]:
    library_id = rank_item.get("libraryId", "")
    market_share = rank_item.get("marketShare")

    settings = (detail or {}).get("settings", {})
    version = (detail or {}).get("version", {})
    if not isinstance(settings, dict):
        settings = {}
    if not isinstance(version, dict):
        version = {}

    title = settings.get("title") or library_id
    source = settings.get("project") or library_id

    last_update_raw = (
        version.get("lastUpdateDate")
        or version.get("lastRunDate")
        or version.get("parseDate")
        or version.get("lastUpdate")
    )
    dt = parse_dt(last_update_raw)

    return {
        "rank": rank_item.get("rank"),
        "title": title,
        "source": source,
        "marketShare": market_share,
        "tokens": version.get("totalTokens"),
        "snippets": version.get("totalSnippets"),
        "updateUtc": dt.isoformat().replace("+00:00", "Z") if dt else "",
        "updateAgo": human_age(dt, now),
        "trustScore": settings.get("trustScore"),
        "verified": settings.get("verified"),
        "benchmarkScore": version.get("benchmarkScore"),
        "type": settings.get("type"),
        "popularityRank": settings.get("popularityRank"),
        "docsRepoUrl": settings.get("docsRepoUrl", ""),
        "docsSiteUrl": settings.get("docsSiteUrl", ""),
        "libraryId": library_id,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch Context7 docs popular rankings and export enriched table."
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--output-json", default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-csv", default=DEFAULT_OUTPUT_CSV)
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    limit = max(1, min(int(args.limit), 200))
    now = datetime.now(timezone.utc)

    rankings_url = f"{base_url}/api/rankings"
    payload = fetch_json(rankings_url)
    libraries = payload.get("data", {}).get("libraries", [])
    if not isinstance(libraries, list):
        raise RuntimeError("Unexpected /api/rankings shape: data.libraries should be a list")
    libraries = libraries[:limit]

    api_calls = 1
    items: list[dict[str, Any]] = []
    errors: list[str] = []

    for item in libraries:
        if not isinstance(item, dict):
            continue
        library_id = item.get("libraryId")
        detail = None
        if isinstance(library_id, str) and library_id:
            try:
                detail = fetch_json(library_detail_url(base_url, library_id))
            except Exception as exc:  # keep row even if detail fails
                errors.append(f"{library_id}: {exc}")
            finally:
                api_calls += 1
        row = flatten_item(item, detail, now)
        items.append(row)

    out_json = Path(args.output_json)
    out_csv = Path(args.output_csv)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    headers = [
        "rank",
        "title",
        "source",
        "marketShare",
        "tokens",
        "snippets",
        "updateUtc",
        "updateAgo",
        "trustScore",
        "verified",
        "benchmarkScore",
        "type",
        "popularityRank",
        "docsRepoUrl",
        "docsSiteUrl",
        "libraryId",
    ]
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(items)

    output = {
        "generatedAtUtc": now.isoformat(),
        "baseUrl": base_url,
        "limit": limit,
        "rows": len(items),
        "apiCalls": api_calls,
        "sourceEndpoint": rankings_url,
        "items": items,
        "errors": errors,
    }
    out_json.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Done. rows={len(items)} api_calls={api_calls}")
    print(f"JSON: {out_json}")
    print(f"CSV:  {out_csv}")
    if errors:
        print(f"Warnings: {len(errors)} detail fetch errors", file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
