# Role Packs Design

**Context**

The site currently exposes raw rankings only. That works for power users, but it does not help visitors quickly answer two practical questions:

1. Which skills should I care about for my role?
2. Which skills are good additions for diagrams, project updates, and boss-facing communication?

This repo also keeps a curated local install set, so additions should follow the existing de-dup policy rather than blindly mirroring rankings.

## Goals

- Add a role-based recommendation layer to the homepage.
- Add a goal-based recommendation layer for common use cases.
- Install a small number of high-value missing skills from the top 500 that expand the pack without obvious duplication.
- Keep recommendations limited to skills already present in the curated pack.

## Non-Goals

- Full marketplace taxonomy.
- Auto-generated recommendation clustering from embeddings or LLM tags.
- Per-role install commands on the site.

## Candidate Selection Approach

### Option A: Rank-only additions

Take the highest-ranked missing candidates from the top 500.

Pros:
- Simple.
- Easy to justify numerically.

Cons:
- Pulls in duplicates.
- Misses role fit.
- Favors broad but redundant skills.

### Option B: Manual role packs only, no new installs

Keep the existing pack unchanged and only curate homepage recommendation cards.

Pros:
- No repo churn.
- Lowest maintenance.

Cons:
- Leaves obvious gaps for PM/leadership workflows.
- Role packs would look thin for non-developers.

### Option C: Recommended

Use a hybrid approach:
- Add only missing top-500 skills that clearly expand role coverage.
- Reject lower-ranked or narrower candidates when an existing skill already covers the same job.
- Build homepage packs manually from the curated installed set.

Pros:
- Good signal-to-noise ratio.
- Maintains curated quality.
- Produces a homepage that is useful for both technical and non-technical visitors.

Cons:
- Requires judgment and a maintained allowlist.

## Candidate Decisions

Install:
- `product-manager-toolkit` — fills PM/PRD/prioritization gap.
- `ceo-advisor` — adds executive/board/investor communication perspective.
- `cto-advisor` — adds engineering leadership, tech debt, and metrics framing.

Keep already-added:
- `mermaid-diagrams` — dedicated Mermaid coverage.

Reject:
- `agile-product-owner` — overlaps with `product-manager-toolkit`, lower ranked.
- `product-strategist` — overlaps with `product-manager-toolkit` and `ceo-advisor`, lower ranked.
- `document-writer` — overlaps with `doc-coauthoring` and `internal-comms`, lower ranked.
- `docs-write` — Metabase-specific writing style; too narrow.
- `update-project` — overlaps with `update-docs` and existing docs workflow.
- `pr-status-triage` — too repo-specific to Next.js internals.

## Homepage Information Architecture

Add a new section near the top of `docs/index.html`:

1. `Recommended Packs`
- short intro explaining that these are curated starting points, not exhaustive sets

2. `By Role`
- Developer Core
- Technical Lead / Architect
- PM / Product
- Founder / CEO / Boss Updates
- Design / Research

3. `By Goal`
- Diagram & Architecture
- Weekly Status & Exec Updates
- PRD & Planning
- Deliverables (docx / ppt / pdf)

Each card should:
- show a title
- show a one-line rationale
- list installed skills as clickable chips linking to Context7 pages

## Data Model

Keep it static in the page for now:
- a small JS object with role and goal packs
- render based on the already-loaded skills dataset for links and validation

This keeps the change simple and avoids adding another data file.
