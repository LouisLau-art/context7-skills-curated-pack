# Context7 Skills Curated Pack

[English](README.md) | [简体中文](README.zh-CN.md)

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Installable Skills](https://img.shields.io/badge/installable_skills-163-blue)
![Local Total](https://img.shields.io/badge/local_total_with__.system-164-6f42c1)
![Curation](https://img.shields.io/badge/curation-Installs%2BTrust%2BVerified-orange)
![Context7](https://img.shields.io/badge/source-Context7-black)

A curated, deduplicated Context7 skills pack for software development workflows.

Live site (GitHub Pages): https://louislau-art.github.io/context7-skills-curated-pack/

Current snapshot: **163 installable skills** (plus internal `.system`, total local dirs = 164).

This repository intentionally contains:
- `skills_manifest.csv` (selected skills with source/score)
- `skills_selected.txt` (plain list)
- `scripts/install_curated.sh` (one-click installer)
- docs for de-dup policy and stack classification

It intentionally does **not** contain third-party `SKILL.md` contents.

## Why this approach

- lighter and easier to maintain
- deterministic reinstall from source
- avoids re-hosting third-party skill files

## Quick Start

```bash
# install to Claude target
bash scripts/install_curated.sh claude

# dry-run first
DRY_RUN=1 bash scripts/install_curated.sh claude
```

Supported targets:
- `claude` (default)
- `universal`
- `global`
- `auto`

## Files

- `skills_manifest.csv`: `slug, skill_name, source, installs, trust, score`
- `skills_selected.txt`: current selected slugs
- `manifest_summary.json`: generation metadata
- `scripts/fetch_context7_skill_rankings.py`: pull live ranked skills from Context7 API
- `scripts/fetch_context7_library_rankings.py`: pull live docs library rankings (popular/trending/latest)
- `scripts/rebuild_skills_by_stack_zh.py`: regenerate Chinese category doc from current `skills_selected.txt`
- `docs/dedup-policy.md`: de-dup rule
- `docs/skills-by-stack-zh.md`: Chinese stack/language categorization

## Live Ranking Pull (Context7)

You can pull the **dynamic** Context7 ranked skills list directly from Context7:

```bash
python3 scripts/fetch_context7_skill_rankings.py \
  --min-installs 0 \
  --output-csv data/context7_ranked_skills_all.csv \
  --output-json data/context7_ranked_skills_all.meta.json
```

The script uses:
- `GET /api/skills/count`
- `GET /api/skills/ranked?limit=100&offset=...`

Note: this is a live leaderboard; counts change over time.

## Live Docs Popular Ranking

You can also pull Context7 docs library rankings (popular/trending/latest):

```bash
# Popular docs ranking (includes source/tokens/snippets/update fields)
python3 scripts/fetch_context7_library_rankings.py \
  --kind popular \
  --output-csv data/context7_popular_libraries.csv \
  --output-json data/context7_popular_libraries.meta.json

# Optional: trending/latest
python3 scripts/fetch_context7_library_rankings.py --kind trending \
  --output-csv data/context7_trending_libraries.csv \
  --output-json data/context7_trending_libraries.meta.json
python3 scripts/fetch_context7_library_rankings.py --kind latest \
  --output-csv data/context7_latest_libraries.csv \
  --output-json data/context7_latest_libraries.meta.json
```

Endpoints used:
- `GET /api/libraries/homepage?type=popular|trending`
- `GET /api/libraries/latest?limit=...`
- `GET /api/libraries/count`

## Static Ranking Site (GitHub Pages)

This repo now includes a static dashboard with two tabs:
- `Docs Popular` (Context7 market-share list, currently top 50 from API)
- `Skills Ranking` (current ranked list without installs threshold, currently thousands of rows)

Files:
- `docs/index.html`
- `docs/data/context7_docs_popular_top50.json`
- `docs/data/context7_skills_ranked_all.json`

The dataset is generated via:

```bash
python3 scripts/fetch_context7_docs_popular.py \
  --limit 50 \
  --output-json docs/data/context7_docs_popular_top50.json \
  --output-csv docs/data/context7_docs_popular_top50.csv

python3 scripts/fetch_context7_skills_for_site.py \
  --min-installs 0 \
  --output-json docs/data/context7_skills_ranked_all.json \
  --output-csv docs/data/context7_skills_ranked_all.csv
```

Automatic updates are handled by:
- `.github/workflows/update-docs-popular-site.yml`
- triggers: daily schedule + manual `workflow_dispatch`

### Enable GitHub Pages

1. Open repository `Settings` -> `Pages`.
2. Under `Build and deployment`, choose:
   - `Source`: `Deploy from a branch`
   - `Branch`: `main`
   - `Folder`: `/docs`
3. Save, then open the published URL.

After that, the ranking site updates automatically as the workflow refreshes data.

## 163 Skills Distribution (Current Pack)

High-level stack distribution for the current curated 163 skills:

| Category | Count | Share |
| --- | ---: | ---: |
| Frontend & Web UI | 46 | 28.2% |
| LLM / Agent / Prompting | 27 | 16.6% |
| Mobile (RN / Expo / Flutter) | 18 | 11.0% |
| Backend & Services | 16 | 9.8% |
| Testing & QA | 11 | 6.7% |
| Engineering Workflow | 10 | 6.1% |
| Database & Data Engineering | 9 | 5.5% |
| Docs & Office Automation | 8 | 4.9% |
| Cloud & DevOps | 7 | 4.3% |
| Python / AI / Data Science | 6 | 3.7% |
| Security & Architecture | 5 | 3.1% |

## Selection Rule

`0.50*Installs(log-normalized) + 0.30*Trust + 0.10*OfficialSource + 0.10*(Trust>=9)`

Used for high-overlap groups only, not blanket deletion.

## License

MIT for scripts/manifests in this repo.

Upstream skills remain under their original licenses and repositories.
