#!/usr/bin/env python3
"""Fetch prerendered leaderboard data from skills.sh for static site usage."""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "https://skills.sh"
DEFAULT_VIEW = "all-time"
DEFAULT_LIMIT = 2000
DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 4
DEFAULT_OUT_JSON = "docs/data/skills_sh_all_time_top2000.json"
DEFAULT_OUT_CSV = "docs/data/skills_sh_all_time_top2000.csv"
TRANSIENT_HTTP_STATUS = {408, 425, 429, 500, 502, 503, 504}

VIEW_PATHS = {
    "all-time": "/",
    "trending": "/trending",
    "hot": "/hot",
}


def fetch_bytes(url: str, timeout: int = DEFAULT_TIMEOUT, retries: int = DEFAULT_RETRIES) -> bytes:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with urlopen(req, timeout=timeout) as resp:  # nosec B310 (trusted host input)
                return resp.read()
        except HTTPError as exc:
            last_err = exc
            if exc.code not in TRANSIENT_HTTP_STATUS or attempt >= retries:
                break
        except (TimeoutError, URLError) as exc:
            last_err = exc
            if attempt >= retries:
                break

        sleep_s = min(8.0, 0.5 * (2 ** (attempt - 1))) + random.uniform(0.0, 0.25)
        time.sleep(sleep_s)

    if isinstance(last_err, HTTPError):
        raise RuntimeError(f"HTTP {last_err.code} for {url}") from last_err
    if isinstance(last_err, TimeoutError):
        raise RuntimeError(f"Timeout fetching {url}") from last_err
    if isinstance(last_err, URLError):
        raise RuntimeError(f"Network error for {url}: {last_err}") from last_err
    raise RuntimeError(f"Failed to fetch {url}")


def fetch_html(url: str, timeout: int = DEFAULT_TIMEOUT, retries: int = DEFAULT_RETRIES) -> str:
    return fetch_bytes(url, timeout=timeout, retries=retries).decode("utf-8", "ignore")


def fetch_api_page(
    base_url: str,
    view: str,
    page: int,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
) -> dict:
    url = f"{base_url.rstrip('/')}/api/skills/{view}/{page}"
    try:
        payload = json.loads(fetch_bytes(url, timeout=timeout, retries=retries).decode("utf-8", "ignore"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"skills.sh API page {page} returned invalid JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"skills.sh API page {page} returned unexpected payload")
    return payload


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


def unique_skill_key(item: dict) -> tuple[str, str]:
    source = normalize_source(str(item.get("source") or ""))
    skill_id = str(item.get("skillId") or item.get("name") or "").strip()
    return source, skill_id


def build_view_url(base_url: str, view: str) -> str:
    path = VIEW_PATHS[view]
    return f"{base_url.rstrip('/')}{path}"


def can_keep_stale_snapshot(out_json: Path, out_csv: Path) -> bool:
    return out_json.exists() and out_csv.exists()


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
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    parser.add_argument(
        "--keep-stale-on-error",
        action="store_true",
        help="Keep existing output files and exit successfully when refresh fails.",
    )
    args = parser.parse_args()

    out_json = Path(args.output_json)
    out_csv = Path(args.output_csv)

    try:
        source_url = build_view_url(args.base_url, args.view)
        html = fetch_html(source_url, timeout=args.timeout, retries=args.retries)
        raw_items, meta = extract_initial_skills(html)
        keep = max(1, int(args.limit))
        page_size = 200
        prerender_rows = len(raw_items)
        collected: list[dict] = []
        seen_keys: set[tuple[str, str]] = set()
        for item in raw_items:
            if not isinstance(item, dict):
                continue
            key = unique_skill_key(item)
            if not key[1] or key in seen_keys:
                continue
            seen_keys.add(key)
            collected.append(item)
            if len(collected) >= keep:
                break
        api_pages_fetched = 0
        has_more = prerender_rows < int(meta.get("totalSkills") or prerender_rows)
        next_page = (prerender_rows + page_size - 1) // page_size

        while len(collected) < keep and has_more:
            payload = fetch_api_page(
                args.base_url,
                args.view,
                next_page,
                timeout=args.timeout,
                retries=args.retries,
            )
            api_pages_fetched += 1
            page_items = payload.get("skills")
            if not isinstance(page_items, list) or not page_items:
                break
            for item in page_items:
                if not isinstance(item, dict):
                    continue
                key = unique_skill_key(item)
                if not key[1] or key in seen_keys:
                    continue
                seen_keys.add(key)
                collected.append(item)
                if len(collected) >= keep:
                    break
            has_more = bool(payload.get("hasMore"))
            next_page += 1

        rows: list[dict[str, object]] = []
        for idx, item in enumerate(collected[:keep], start=1):
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
            "sourceRows": len(collected[:keep]),
            "prerenderRows": prerender_rows,
            "apiPagesFetched": api_pages_fetched,
            "totalSkills": meta.get("totalSkills"),
            "allTimeTotal": meta.get("allTimeTotal"),
            "items": rows,
        }
        out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as exc:
        if args.keep_stale_on_error and can_keep_stale_snapshot(out_json, out_csv):
            print(
                f"WARN: {exc}. keeping existing snapshot at {out_json} and {out_csv}",
                file=sys.stderr,
            )
            return 0
        raise

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
