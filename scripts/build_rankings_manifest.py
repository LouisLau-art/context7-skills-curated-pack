#!/usr/bin/env python3
"""Build a machine-readable manifest for the public ranking datasets."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_DOCS_JSON = "docs/data/context7_docs_popular_top50.json"
DEFAULT_DOCS_EXTENDED_JSON = "docs/data/context7_docs_extended_top1000.json"
DEFAULT_DOCS_EXTENDED_RUNTIME_JSON = "docs/data/context7_docs_extended_top100.runtime.json"
DEFAULT_SKILLS_SH_JSON = "docs/data/skills_sh_all_time_top600.json"
DEFAULT_CONTEXT7_SKILLS_JSON = "docs/data/context7_skills_ranked_all.json"
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
        description="Build machine-readable manifest for docs + skills ranking JSON files."
    )
    parser.add_argument("--docs-json", default=DEFAULT_DOCS_JSON)
    parser.add_argument("--docs-extended-json", default=DEFAULT_DOCS_EXTENDED_JSON)
    parser.add_argument("--docs-extended-runtime-json", default=DEFAULT_DOCS_EXTENDED_RUNTIME_JSON)
    parser.add_argument("--skills-sh-json", default=DEFAULT_SKILLS_SH_JSON)
    parser.add_argument("--context7-skills-json", default=DEFAULT_CONTEXT7_SKILLS_JSON)
    parser.add_argument("--public-base", default=DEFAULT_PUBLIC_BASE)
    parser.add_argument("--output-json", default=DEFAULT_OUTPUT_JSON)
    args = parser.parse_args()

    docs_path = Path(args.docs_json)
    docs_extended_path = Path(args.docs_extended_json)
    docs_extended_runtime_path = Path(args.docs_extended_runtime_json)
    skills_sh_path = Path(args.skills_sh_json)
    context7_skills_path = Path(args.context7_skills_json)
    out_path = Path(args.output_json)

    docs = load_payload(docs_path)
    skills_sh = load_payload(skills_sh_path)
    context7_skills = load_payload(context7_skills_path)

    docs_extended = load_payload(docs_extended_path) if docs_extended_path.exists() else None
    docs_extended_runtime = (
        load_payload(docs_extended_runtime_path) if docs_extended_runtime_path.exists() else None
    )

    docs_rel = docs_path.as_posix()
    docs_ext_rel = docs_extended_path.as_posix()
    docs_ext_runtime_rel = docs_extended_runtime_path.as_posix()
    skills_sh_rel = skills_sh_path.as_posix()
    context7_skills_rel = context7_skills_path.as_posix()
    manifest_rel = out_path.as_posix()

    now = datetime.now(timezone.utc).isoformat()
    docs_extended_estimated_rows = (
        docs_extended.get("estimatedRows")
        if isinstance(docs_extended, dict)
        else None
    )
    docs_runtime_estimated_rows = (
        docs_extended_runtime.get("estimatedRows")
        if isinstance(docs_extended_runtime, dict)
        else None
    )

    preferred_docs_extended_dataset_id = "docs_extended_top1000"
    if isinstance(docs_extended_estimated_rows, int) and docs_extended_estimated_rows > 0:
        preferred_docs_extended_dataset_id = "docs_extended_top1000"
    elif isinstance(docs_runtime_estimated_rows, int) and docs_runtime_estimated_rows > 0:
        preferred_docs_extended_dataset_id = "docs_extended_top100_runtime"

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
                "id": "docs_extended_top100_runtime",
                "title": "Context7 Docs Extended Runtime Snapshot (Top 100)",
                "relativePath": docs_ext_runtime_rel,
                "publicUrl": public_url(args.public_base, docs_ext_runtime_rel),
                "generatedAtUtc": docs_extended_runtime.get("generatedAtUtc") if docs_extended_runtime else None,
                "rows": docs_extended_runtime.get("rows") if docs_extended_runtime else None,
                "officialRows": docs_extended_runtime.get("officialRows") if docs_extended_runtime else None,
                "estimatedRows": docs_extended_runtime.get("estimatedRows") if docs_extended_runtime else None,
                "notes": [
                    "Temporary runtime snapshot generated from /api/rankings + /api/libraries/all.",
                    "Use this when docs_extended_top1000 is official-only (estimatedRows=0).",
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
                "available": docs_extended_runtime is not None,
            },
            {
                "id": "skills_sh_all_time_top600",
                "title": "Skills.sh All-Time Ranking Snapshot (Top 600)",
                "relativePath": skills_sh_rel,
                "publicUrl": public_url(args.public_base, skills_sh_rel),
                "generatedAtUtc": skills_sh.get("generatedAtUtc"),
                "rows": skills_sh.get("rows"),
                "sourceRows": skills_sh.get("sourceRows"),
                "sourceUrl": skills_sh.get("sourceUrl"),
                "totalSkills": skills_sh.get("totalSkills"),
                "allTimeTotal": skills_sh.get("allTimeTotal"),
                "notes": [
                    "Primary skills dataset for the site.",
                    "Derived from the prerendered skills.sh all-time leaderboard payload.",
                    "Current snapshot keeps the first 600 rows exposed in the site payload.",
                ],
                "keyFields": [
                    "rank",
                    "name",
                    "skillId",
                    "source",
                    "installCount",
                    "detailUrl",
                ],
            },
            {
                "id": "skills_ranked_all",
                "title": "Context7 Skills Ranking (Secondary, No installs threshold)",
                "relativePath": context7_skills_rel,
                "publicUrl": public_url(args.public_base, context7_skills_rel),
                "generatedAtUtc": context7_skills.get("generatedAtUtc"),
                "rows": context7_skills.get("rows"),
                "baseUrl": context7_skills.get("baseUrl"),
                "minInstalls": context7_skills.get("minInstalls"),
                "notes": [
                    "Secondary skills dataset for long-tail lookup and Context7-specific comparison.",
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
                "For skills, prefer skills_sh_all_time_top600 first, then fall back to skills_ranked_all for Context7-specific or long-tail lookups.",
                "For docs 51+, if docs_extended_top1000.estimatedRows=0, use docs_extended_top100_runtime.",
            ],
            "preferredSkillsDatasetId": "skills_sh_all_time_top600",
            "preferredDocsExtendedDatasetId": preferred_docs_extended_dataset_id,
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
