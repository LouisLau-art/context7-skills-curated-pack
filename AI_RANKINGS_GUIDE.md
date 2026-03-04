# AI Rankings Guide

This guide is for external AI models/agents that need to consume the two public ranking datasets in this repository.

## Canonical Public URLs

- Site: `https://louislau-art.github.io/context7-skills-curated-pack/`
- Manifest (read this first): `https://louislau-art.github.io/context7-skills-curated-pack/data/context7_rankings_manifest.json`
- Docs ranking JSON: `https://louislau-art.github.io/context7-skills-curated-pack/data/context7_docs_popular_top50.json`
- Docs extended JSON (full target): `https://louislau-art.github.io/context7-skills-curated-pack/data/context7_docs_extended_top1000.json`
- Docs extended runtime JSON (temporary 51+ source): `https://louislau-art.github.io/context7-skills-curated-pack/data/context7_docs_extended_top100.runtime.json`
- Skills ranking JSON: `https://louislau-art.github.io/context7-skills-curated-pack/data/context7_skills_ranked_all.json`

Raw GitHub fallback (if Pages cache/deploy lags):
- Manifest: `https://raw.githubusercontent.com/LouisLau-art/context7-skills-curated-pack/main/docs/data/context7_rankings_manifest.json`
- Docs ranking: `https://raw.githubusercontent.com/LouisLau-art/context7-skills-curated-pack/main/docs/data/context7_docs_popular_top50.json`
- Docs extended (full target): `https://raw.githubusercontent.com/LouisLau-art/context7-skills-curated-pack/main/docs/data/context7_docs_extended_top1000.json`
- Docs extended runtime (temporary 51+ source): `https://raw.githubusercontent.com/LouisLau-art/context7-skills-curated-pack/main/docs/data/context7_docs_extended_top100.runtime.json`
- Skills ranking: `https://raw.githubusercontent.com/LouisLau-art/context7-skills-curated-pack/main/docs/data/context7_skills_ranked_all.json`

## What Each Dataset Means

- `docs_popular_top50`:
  - Context7 docs popularity snapshot (currently top 50 rows).
  - Main metric: `marketShare`.
- `docs_extended_top1000`:
  - Rows 1-50 are official rankings from Context7.
  - Rows >50 are estimated and directional (not official market-share rows).
  - Check `estimatedRows` in payload/meta. If `estimatedRows = 0`, the file is a temporary official-only snapshot.
- `docs_extended_top100_runtime`:
  - Runtime snapshot currently used when `docs_extended_top1000` is official-only.
  - Includes 1-50 official + 51-100 estimated rows.
- `skills_ranked_all`:
  - Context7 skills ranked snapshot with `minInstalls=0`.
  - Main metric: `installCount` (rank order comes from Context7 ranked endpoint).

## Recommended Consumption Protocol

1. Fetch `context7_rankings_manifest.json`.
2. Read `datasets[*].publicUrl` and `generatedAtUtc`.
3. For docs 51+, if `docs_extended_top1000.estimatedRows = 0`, switch to `docs_extended_top100_runtime`.
4. Fetch only the dataset(s) you need.
5. In responses, mention snapshot timestamp and dataset scope (for example: docs top 50 only, or docs top 100 runtime).

## Minimal Field Notes

- Docs ranking key fields: `rank`, `title`, `source`, `marketShare`, `snippets`, `tokens`, `updateAgo`, `verified`.
- Skills ranking key fields: `rank`, `name`, `source`, `installCount`, `trustScore`, `verified`.

## 中文提示

如果你是中文模型，请先读取 manifest，再按需读取 docs/skills JSON，并在回答中注明数据时间戳（`generatedAtUtc`）。如果 `docs_extended_top1000` 的 `estimatedRows=0`，请改用 `docs_extended_top100.runtime.json` 获取 51+。
