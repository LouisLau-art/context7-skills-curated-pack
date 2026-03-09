# Context7 Skills Curated Pack

[English](README.md) | [简体中文](README.zh-CN.md)

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Installable Skills](https://img.shields.io/badge/installable_skills-173-blue)
![Local Total](https://img.shields.io/badge/local_total_with__.system-174-6f42c1)
![Curation](https://img.shields.io/badge/curation-Installs%2BTrust%2BVerified-orange)
![Context7](https://img.shields.io/badge/source-Context7-black)

A curated, deduplicated Context7 skills pack for software development workflows.

Live site (GitHub Pages): https://louislau-art.github.io/context7-skills-curated-pack/

Current snapshot: **173 installable skills** (plus internal `.system`, total local dirs = 174).

This repository intentionally contains:
- `skills_manifest.csv` (selected skills with source/score)
- `skills_selected.txt` (plain list)
- `scripts/install_curated.py` (cross-platform one-click installer)
- `scripts/install_curated.sh` (thin Unix wrapper around the Python installer)
- `scripts/install_curated.ps1` (thin PowerShell wrapper around the Python installer)
- `scripts/validate_skills_frontmatter.py` (post-install validator/sanitizer for `SKILL.md` frontmatter)
- docs for de-dup policy and stack classification

It intentionally does **not** contain third-party `SKILL.md` contents.

## Why this approach

- lighter and easier to maintain
- deterministic reinstall from source
- avoids re-hosting third-party skill files
- easier to sync the same curated pack across multiple agent directories

## Quick Start

```bash
# cross-platform install to the Claude-compatible base target
python scripts/install_curated.py claude

# install once, then sync to Codex + Gemini + OpenCode + Amp
python scripts/install_curated.py all

# Qwen-compatible flow (shares Gemini skills directory)
python scripts/install_curated.py qwen

# Unix convenience wrapper
bash scripts/install_curated.sh all

# Windows PowerShell wrapper
powershell -ExecutionPolicy Bypass -File .\scripts\install_curated.ps1 all

# dry-run first
DRY_RUN=1 python scripts/install_curated.py claude+opencode+amp
```

PowerShell dry-run example:

```powershell
$env:DRY_RUN = "1"
.\scripts\install_curated.ps1 qwen
```

Supported targets:
- `claude` (default)
- `codex` (install via Claude-compatible target, then sync to `~/.codex/skills`)
- `gemini` (sync to `~/.gemini/skills`)
- `qwen` (alias of `gemini`; uses the same skills directory)
- `opencode` (sync to `~/.config/opencode/skills` on Unix-like systems, `%APPDATA%\\opencode\\skills` on Windows)
- `amp` / `ampcode` (sync to `~/.config/agents/skills` on Unix-like systems, `%APPDATA%\\agents\\skills` on Windows)
- `all` / `claude+codex+gemini+opencode+amp`
- custom combos such as `claude+codex+opencode`, `claude+gemini+amp`, `claude+qwen`
- `universal`, `global`, `cursor`, `auto` (install-only targets; no post-install sync)

The installer reads `skills_manifest.csv` directly, installs from upstream Context7 sources, validates/sanitizes known `SKILL.md` frontmatter issues in the Claude-compatible base install, then copies the resulting local skill tree into compatible agent directories. It does **not** vendor third-party `SKILL.md` files into this repo.

### Directory Overrides

If your local agent uses a non-default path, set an override before running the installer:

```bash
export CLAUDE_SKILLS_DIR=/custom/claude/skills
export CODEX_SKILLS_DIR=/custom/codex/skills
export GEMINI_SKILLS_DIR=/custom/gemini/skills
export OPENCODE_SKILLS_DIR=/custom/opencode/skills
export AMP_SKILLS_DIR=/custom/amp/skills
```

`qwen` reuses `GEMINI_SKILLS_DIR`.

## Files

- `skills_manifest.csv`: `slug, skill_name, source, installs, trust, score`
- `skills_selected.txt`: current selected slugs
- `manifest_summary.json`: generation metadata
- `scripts/install_curated.py`: cross-platform installer and sync entry point
- `scripts/install_curated.sh`: Unix wrapper for the Python installer
- `scripts/install_curated.ps1`: PowerShell wrapper for the Python installer
- `scripts/validate_skills_frontmatter.py`: validate and sanitize known frontmatter issues in installed skills
- `scripts/fetch_context7_skill_rankings.py`: pull live ranked skills from Context7 API
- `scripts/fetch_context7_library_rankings.py`: pull live docs library rankings (popular/trending/latest)
- `scripts/rebuild_skills_by_stack_zh.py`: regenerate Chinese category doc from current `skills_selected.txt`
- `docs/dedup-policy.md`: de-dup rule
- `docs/skills-by-stack-zh.md`: Chinese stack/language categorization
- `docs/troubleshooting.md`: common install/auth/frontmatter troubleshooting

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

### Context7 API Key (Recommended)

For higher rate limits, set a key before running fetch scripts:

```bash
export CONTEXT7_API_KEY='your_ctx7_key'
```

Portable alternatives:
- `CONTEXT7_API_KEY_FILE=/path/to/key.txt` (first line is token)
- `CONTEXT7_ALLOW_CODEX_MCP_FALLBACK=1` to explicitly allow reading Codex MCP config (`~/.codex/config.toml`)

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

This repo now includes a static dashboard with three tabs:
- `Docs Popular` (Context7 market-share list, currently top 50 from API)
- `Docs Extended` (rows 1-50 official, rows >50 estimated from full libraries catalog)
- `Skills Ranking` (current ranked list without installs threshold, currently thousands of rows)

Files:
- `docs/index.html`
- `docs/data/context7_docs_popular_top50.json`
- `docs/data/context7_docs_extended_top1000.json`
- `docs/data/context7_skills_ranked_all.json`

The dataset is generated via:

```bash
python3 scripts/fetch_context7_docs_popular.py \
  --limit 50 \
  --output-json docs/data/context7_docs_popular_top50.json \
  --output-csv docs/data/context7_docs_popular_top50.csv

python3 scripts/fetch_context7_docs_extended.py \
  --top-k 20000 \
  --max-workers 12 \
  --output-json docs/data/context7_docs_extended_top1000.json \
  --output-csv docs/data/context7_docs_extended_top1000.csv

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

## For Other AI Models

If another model/agent needs these rankings, start here:

- Guide: `AI_RANKINGS_GUIDE.md`
- Machine-readable manifest: `docs/data/context7_rankings_manifest.json`
- Public manifest URL:
  `https://louislau-art.github.io/context7-skills-curated-pack/data/context7_rankings_manifest.json`
- Raw GitHub fallback:
  `https://raw.githubusercontent.com/LouisLau-art/context7-skills-curated-pack/main/docs/data/context7_rankings_manifest.json`

## 173 Skills Distribution (Current Pack)

High-level stack distribution for the current curated 173 skills:

| Category | Count | Share |
| --- | ---: | ---: |
| Frontend & Web UI | 46 | 26.6% |
| LLM / Agent / Prompting | 28 | 16.2% |
| Mobile (RN / Expo / Flutter) | 18 | 10.4% |
| Backend & Services | 16 | 9.2% |
| Testing & QA | 11 | 6.4% |
| Engineering Workflow | 11 | 6.4% |
| Database & Data Engineering | 9 | 5.2% |
| Docs & Office Automation | 8 | 4.6% |
| Cloud & DevOps | 7 | 4.0% |
| Other / Uncategorized | 7 | 4.0% |
| Python / AI / Data Science | 6 | 3.5% |
| Security & Architecture | 6 | 3.5% |

Detailed grouping: `docs/skills-by-stack-zh.md`

## Selection Rule

For high-overlap groups, use:

`0.60*Installs(log-normalized) + 0.25*Trust + 0.15*Verified`

Then do a content review when scores are close (`gap < 0.12` or installs ratio `< 1.8x`).
Used for high-overlap groups only, not blanket deletion.

## License

MIT for scripts/manifests in this repo.

Upstream skills remain under their original licenses and repositories.
