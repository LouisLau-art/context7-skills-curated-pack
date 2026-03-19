# Context7 Skills Curated Pack

[English](README.md) | [简体中文](README.zh-CN.md)

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Installable Skills](https://img.shields.io/badge/installable_skills-125-blue)
![Local Total](https://img.shields.io/badge/local_total_with__.system-121-6f42c1)
![Curation](https://img.shields.io/badge/curation-Source%2BOverlap%2BContent-orange)
![Rankings](https://img.shields.io/badge/rankings-skills.sh%20primary%20%7C%20Context7%20secondary-black)

A curated, deduplicated public skills catalog for multi-agent software workflows, plus profile-based installers and a public multi-source rankings dashboard.

Live site (GitHub Pages): https://louislau-art.github.io/context7-skills-curated-pack/

Current snapshot: **125 installable public skills** in the catalog. The default public install profile (`public-default`) currently resolves to **78 skills**. A full `all-public` install yields the complete 125-skill public catalog (plus internal `.system`).

This repository intentionally contains:
- `skills_manifest.csv` (selected skills with source/score)
- `skills_selected.txt` (plain list)
- `profiles/` (public install bundles such as `core-meta`, `development-core`, `writing-blog`)
- `scripts/install_curated.py` (cross-platform one-click installer)
- `scripts/install_curated.sh` (thin Unix wrapper around the Python installer)
- `scripts/install_curated.ps1` (thin PowerShell wrapper around the Python installer)
- `scripts/validate_skills_frontmatter.py` (post-install validator/sanitizer for `SKILL.md` frontmatter)
- `global-context/` (tracked global agent context shared by Codex / Gemini / Claude)
- docs for de-dup policy and stack classification

It intentionally does **not** contain third-party `SKILL.md` contents.

## Why this approach

- lighter and easier to maintain
- deterministic reinstall from source
- avoids re-hosting third-party skill files
- easier to sync the same curated pack across multiple agent directories

## Quick Start

```bash
# install the default public profile to the Claude-compatible base target
python scripts/install_curated.py claude --profiles public-default

# install the full public catalog
python scripts/install_curated.py claude --profiles all-public

# install once, then sync to Codex + Gemini + OpenCode + Amp + CodeBuddy
python scripts/install_curated.py all --profiles public-default

# add writing/blog support on top of the default profile
python scripts/install_curated.py claude --profiles public-default+writing-blog

# job-search/resume focused install
python scripts/install_curated.py codex --profiles resume-job-search

# Unix convenience wrapper
bash scripts/install_curated.sh all --profiles public-default

# Windows PowerShell wrapper
powershell -ExecutionPolicy Bypass -File .\scripts\install_curated.ps1 all --profiles public-default

# inspect available public profiles
python scripts/install_curated.py --list-profiles

# dry-run first
DRY_RUN=1 python scripts/install_curated.py claude+opencode+amp --profiles public-default+cloud-platform
```

PowerShell dry-run example:

```powershell
$env:DRY_RUN = "1"
.\scripts\install_curated.ps1 qwen --profiles public-default
```

## Public Profiles

This repo now distinguishes:

- **public catalog**: all rows in `skills_manifest.csv`
- **public profiles**: install bundles under `profiles/`
- **private local overlay**: local-only additions kept outside the public product surface

Current public profiles:

- `core-meta` — discovery, verification, review, planning, session continuity
- `development-core` — software development starter pack
- `context7-integration` — Context7 MCP plus reusable docs lookup workflow
- `writing-blog` — public writing/blogging starter
- `resume-job-search` — resume and job-search starter
- `docs-office` — PDF/DOCX/PPTX/office workflows
- `cloud-platform` — Vercel/Supabase/Hugging Face/platform workflows
- `design-ui` — design and frontend-heavy work
- `database-data` — database, RAG, and data workflows

Installer aliases:

- `public-default = core-meta + development-core`
- `all-public = union of all public profiles`

Context7 setup guide:

- `docs/context7-agent-setup.md`
- `docs/context7-agent-setup.zh-CN.md`

Supported targets:
- `claude` (default)
- `codex` (install via Claude-compatible target, then sync to `~/.codex/skills`)
- `gemini` (sync to `~/.gemini/skills`)
- `qwen` (alias of `gemini`; uses the same skills directory)
- `opencode` (sync to `~/.config/opencode/skills` on Unix-like systems, `%APPDATA%\\opencode\\skills` on Windows)
- `amp` / `ampcode` (sync to `~/.config/agents/skills` on Unix-like systems, `%APPDATA%\\agents\\skills` on Windows)
- `codebuddy` (sync to `~/.codebuddy/skills`)
- `all` / `claude+codex+gemini+opencode+amp+codebuddy`
- custom combos such as `claude+codex+opencode`, `claude+gemini+amp+codebuddy`, `claude+qwen`
- `universal`, `global`, `cursor`, `auto` (install-only targets; no post-install sync)

The installer reads `skills_manifest.csv` as the public catalog, resolves one or more profile files from `profiles/`, installs the matching upstream skills, validates/sanitizes known `SKILL.md` frontmatter issues in the Claude-compatible base install, then copies the resulting local skill tree into compatible agent directories. It does **not** vendor third-party `SKILL.md` files into this repo.

### Directory Overrides

If your local agent uses a non-default path, set an override before running the installer:

```bash
export CLAUDE_SKILLS_DIR=/custom/claude/skills
export CODEX_SKILLS_DIR=/custom/codex/skills
export GEMINI_SKILLS_DIR=/custom/gemini/skills
export OPENCODE_SKILLS_DIR=/custom/opencode/skills
export AMP_SKILLS_DIR=/custom/amp/skills
export CODEBUDDY_SKILLS_DIR=/custom/codebuddy/skills
```

`qwen` reuses `GEMINI_SKILLS_DIR`.

### Codex-First Sync

If you use `~/.codex/skills` as the primary user skills directory, sync other agents from Codex instead of treating `.claude/skills` as the source of truth:

```bash
# Preview what would change
python scripts/sync_from_codex.py --dry-run --prune

# Copy Codex user skills into Claude/Gemini/OpenCode/Amp/CodeBuddy
python scripts/sync_from_codex.py --prune

# Or mirror each skill directory as symlinks
python scripts/sync_from_codex.py --mode symlink --prune
```

This script syncs user skill directories only and leaves target-side `.system` folders untouched.

## Files

- `skills_manifest.csv`: `slug, skill_name, source, installs, trust, score`
- `skills_selected.txt`: compatibility export of the current public catalog
- `profiles/*.txt`: public install profiles
- `manifest_summary.json`: generation metadata
- `scripts/install_curated.py`: cross-platform installer and sync entry point
- `scripts/install_curated.sh`: Unix wrapper for the Python installer
- `scripts/install_curated.ps1`: PowerShell wrapper for the Python installer
- `scripts/validate_skills_frontmatter.py`: validate and sanitize known frontmatter issues in installed skills
- `scripts/fetch_skills_sh_rankings.py`: pull the prerendered `skills.sh` leaderboard for the static site
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

This repo now includes a static dashboard with four tabs:
- `Skills.sh All Time` (primary skills leaderboard, current top 2000 snapshot using the prerendered payload plus public pagination API)
- `Context7 Skills` (secondary skills leaderboard for Context7-specific comparison and long-tail lookup)
- `Docs Popular` (Context7 market-share list, currently top 50 from API)
- `Docs Extended` (rows 1-50 official, rows >50 estimated from full libraries catalog)

Files:
- `docs/index.html`
- `docs/data/skills_sh_all_time_top2000.json`
- `docs/data/context7_docs_popular_top50.json`
- `docs/data/context7_docs_extended_top1000.json`
- `docs/data/context7_skills_ranked_all.json`

The dataset is generated via:

```bash
python3 scripts/fetch_skills_sh_rankings.py \
  --view all-time \
  --limit 2000 \
  --output-json docs/data/skills_sh_all_time_top2000.json \
  --output-csv docs/data/skills_sh_all_time_top2000.csv

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

## 125 Skills Distribution (Current Pack)

High-level stack distribution for the current curated 125 skills:

| Category | Count | Share |
| --- | ---: | ---: |
| Frontend & Web UI | 34 | 28.3% |
| LLM / Agent / Prompting | 12 | 10.0% |
| Backend & Services | 12 | 10.0% |
| Engineering Workflow | 21 | 17.5% |
| Database & Data Engineering | 10 | 8.3% |
| Testing & QA | 8 | 6.7% |
| Docs & Office Automation | 9 | 7.5% |
| Python / AI / Data Science | 6 | 5.0% |
| Security & Architecture | 6 | 5.0% |
| Other / Uncategorized | 2 | 1.7% |

Detailed grouping: `docs/skills-by-stack-zh.md`

## Selection Rule

For high-overlap groups, use this order:

1. Prefer official or strong-maintainer sources
2. Keep only `1` general skill plus `1-2` specialized skills per topic cluster
3. Treat trigger conflicts and workflow overlap as stronger signals than naming collisions
4. Do a content review for close calls, favoring clearer triggers and better bundled material
5. Use installs/trust/verification as tie-breakers, not as the primary rule

Detailed policy: `docs/dedup-policy.md`

## SkillsBench-Informed Curation Notes

This pack uses the `skills.sh` leaderboard as a discovery surface, not as an auto-include list.
Popularity matters, but it does **not** override scope fit or content quality.

When deciding whether to keep or add a skill, prefer the following:

1. Human-authored procedural skills over generic prompts or self-generated skill content
2. Focused skills with a narrow workflow and `2-3` useful modules over broad "everything docs"
3. Skills that help the agent finish and verify work reliably, especially ones that reduce "quality below threshold" style failures
4. Official or strong-maintainer sources when two candidates cover the same job

In practice, this means:

- `skills.sh` install counts are a useful popularity signal, but not a sufficient reason to keep a skill
- broad cloud/mobile clusters can still be removed if they do not match the current workflow
- a lower-install but more focused resume/blog/review skill can beat a higher-install generic writing skill
- we avoid duplicate workflow coverage unless the extra skill is truly specialized
- same-name skills are not automatically duplicates, and different-name skills can still conflict if they trigger on the same work

## License

MIT for scripts/manifests in this repo.

Upstream skills remain under their original licenses and repositories.
