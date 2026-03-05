#!/usr/bin/env python3
"""Fetch Context7 skills ranked list for static site usage."""

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
from urllib.parse import urlencode
from urllib.request import urlopen

from context7_auth import build_context7_request


DEFAULT_BASE_URL = "https://context7.com"
DEFAULT_LIMIT = 100
DEFAULT_MIN_INSTALLS = 0
DEFAULT_MAX_PAGES = 500
DEFAULT_OUT_JSON = "docs/data/context7_skills_ranked_all.json"
DEFAULT_OUT_CSV = "docs/data/context7_skills_ranked_all.csv"
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


def to_num(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def build_ranked_url(base: str, limit: int, offset: int) -> str:
    return f"{base.rstrip('/')}/api/skills/ranked?{urlencode({'limit': limit, 'offset': offset})}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch Context7 ranked skills for site JSON/CSV.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--min-installs", type=int, default=DEFAULT_MIN_INSTALLS)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    parser.add_argument("--output-json", default=DEFAULT_OUT_JSON)
    parser.add_argument("--output-csv", default=DEFAULT_OUT_CSV)
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    min_installs = int(args.min_installs)
    limit = max(1, min(int(args.limit), 100))
    max_pages = max(1, int(args.max_pages))
    now = datetime.now(timezone.utc)

    rows: list[dict[str, Any]] = []
    offset = 0
    api_calls = 0

    for _ in range(max_pages):
        url = build_ranked_url(base, limit, offset)
        page = fetch_json(url)
        api_calls += 1
        if not isinstance(page, list) or not page:
            break

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
            }
            rows.append(row)

        installs = [to_num(x.get("installCount")) for x in page if isinstance(x, dict)]
        installs = [v for v in installs if v is not None]
        if installs and max(installs) < float(min_installs):
            break

        offset += limit

    filtered = [
        r
        for r in rows
        if to_num(r.get("installCount")) is not None and to_num(r.get("installCount")) >= min_installs
    ]
    filtered.sort(key=lambda x: int(x["rank"]))

    out_json = Path(args.output_json)
    out_csv = Path(args.output_csv)
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
        "url",
    ]
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(filtered)

    payload = {
        "generatedAtUtc": now.isoformat(),
        "baseUrl": base,
        "minInstalls": min_installs,
        "rows": len(filtered),
        "apiCalls": api_calls,
        "items": filtered,
    }
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Done. rows={len(filtered)} api_calls={api_calls} min_installs>={min_installs}")
    print(f"JSON: {out_json}")
    print(f"CSV:  {out_csv}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
