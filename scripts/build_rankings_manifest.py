#!/usr/bin/env python3
"""Build a machine-readable manifest for Context7 ranking datasets."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_DOCS_JSON = "docs/data/context7_docs_popular_top50.json"
DEFAULT_DOCS_EXTENDED_JSON = "docs/data/context7_docs_extended_top1000.json"
DEFAULT_SKILLS_JSON = "docs/data/context7_skills_ranked_all.json"
DEFAULT_OUTPUT_JSON = "docs/data/context7_rankings_manifest.json"
DEFAULT_PUBLIC_BASE = "https://louislau-art.github.io/context7-skills-curated-pack"


def load_payload(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"Expected JSON object in {path}")
    items = payload.get("items")
    if not isinstance(items, list):
        raise RuntimeError(f"Expected list field 'items' in {path}")
    return payload


def to_pages_path(relative_path: str) -> str:
    path = relative_path.strip().lstrip("./")
    # GitHub Pages is configured to serve from the repo's /docs folder as site root.
    if path.startswith("docs/"):
        return path[len("docs/") :]
    return path


def public_url(base: str, relative_path: str) -> str:
    return f"{base.rstrip('/')}/{to_pages_path(relative_path)}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build machine-readable manifest for docs+skills ranking JSON files."
    )
    parser.add_argument("--docs-json", default=DEFAULT_DOCS_JSON)
    parser.add_argument("--docs-extended-json", default=DEFAULT_DOCS_EXTENDED_JSON)
    parser.add_argument("--skills-json", default=DEFAULT_SKILLS_JSON)
    parser.add_argument("--public-base", default=DEFAULT_PUBLIC_BASE)
    parser.add_argument("--output-json", default=DEFAULT_OUTPUT_JSON)
    args = parser.parse_args()

    docs_path = Path(args.docs_json)
    docs_extended_path = Path(args.docs_extended_json)
    skills_path = Path(args.skills_json)
    out_path = Path(args.output_json)

    docs = load_payload(docs_path)
    skills = load_payload(skills_path)

    docs_extended = load_payload(docs_extended_path) if docs_extended_path.exists() else None

    docs_rel = docs_path.as_posix()
    docs_ext_rel = docs_extended_path.as_posix()
    skills_rel = skills_path.as_posix()
    manifest_rel = out_path.as_posix()

    now = datetime.now(timezone.utc).isoformat()
    manifest: dict[str, Any] = {
        "generatedAtUtc": now,
        "project": "context7-skills-curated-pack",
        "siteUrl": args.public_base.rstrip("/"),
        "datasets": [
            {
                "id": "docs_popular_top50",
                "title": "Context7 Docs Popular Ranking (Top 50)",
                "relativePath": docs_rel,
                "publicUrl": public_url(args.public_base, docs_rel),
                "generatedAtUtc": docs.get("generatedAtUtc"),
                "rows": docs.get("rows"),
                "sourceEndpoint": docs.get("sourceEndpoint"),
                "notes": [
                    "Limited to top 50 rows from Context7 API snapshot.",
                    "Primary ranking metric is marketShare.",
                ],
                "keyFields": [
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
                    "libraryId",
                ],
            },
            {
                "id": "docs_extended_top1000",
                "title": "Context7 Docs Extended Ranking (Official Top 50 + Estimated)",
                "relativePath": docs_ext_rel,
                "publicUrl": public_url(args.public_base, docs_ext_rel),
                "generatedAtUtc": docs_extended.get("generatedAtUtc") if docs_extended else None,
                "rows": docs_extended.get("rows") if docs_extended else None,
                "officialRows": docs_extended.get("officialRows") if docs_extended else None,
                "estimatedRows": docs_extended.get("estimatedRows") if docs_extended else None,
                "notes": [
                    "Rows 1-50 are official from /api/rankings.",
                    "Rows >50 are estimated from /api/libraries/all and should be treated as directional.",
                ],
                "keyFields": [
                    "rank",
                    "rankType",
                    "officialRank",
                    "officialMarketShare",
                    "estimatedScore",
                    "title",
                    "source",
                    "popularityRank",
                    "snippets",
                    "tokens",
                    "updateAgo",
                    "trustScore",
                    "verified",
                ],
                "available": docs_extended is not None,
            },
            {
                "id": "skills_ranked_all",
                "title": "Context7 Skills Ranking (No installs threshold)",
                "relativePath": skills_rel,
                "publicUrl": public_url(args.public_base, skills_rel),
                "generatedAtUtc": skills.get("generatedAtUtc"),
                "rows": skills.get("rows"),
                "baseUrl": skills.get("baseUrl"),
                "minInstalls": skills.get("minInstalls"),
                "notes": [
                    "Rows are sorted by Context7 ranked endpoint order.",
                    "Current site build keeps minInstalls=0 (full ranked snapshot).",
                ],
                "keyFields": [
                    "rank",
                    "name",
                    "source",
                    "installCount",
                    "trustScore",
                    "verified",
                    "benchmarkScore",
                    "url",
                ],
            },
        ],
        "aiUsage": {
            "readOrder": [
                "Fetch this manifest first.",
                "Then fetch dataset publicUrl needed for your task.",
                "Use generatedAtUtc and rows for freshness checks.",
            ],
            "manifestPublicUrl": public_url(args.public_base, manifest_rel),
        },
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Done. wrote {out_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
