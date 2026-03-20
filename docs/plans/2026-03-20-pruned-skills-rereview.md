# 2026-03-20 Pruned Skills Re-Review

## Goal

Re-review the local pruning waves from wave 20 through wave 31 using a broader agent-capability lens.

This review does **not** assume that coding skills are inherently more valuable than non-coding skills. It distinguishes:

1. `keep-pruned`: stay out of the tiny local default set
2. `public-or-on-demand`: stay pruned locally, but remain useful in the public catalog or as a `find-skills` restore target
3. `candidate-restore-or-rewrite`: important agent capabilities that were likely undervalued, misclassified, or need environment migration rather than deletion

## Scope

- Source audit: [2026-03-19-local-skills-audit.md](./2026-03-19-local-skills-audit.md)
- Reviewed waves: 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, and the follow-up Context7 conflict cleanup
- Focus: deleted skills only

## Context

Two earlier corrections already showed that the pruning process should not be purely coding-first:

- office/document skills (`docx`, `pptx`, `xlsx`, `pdf`) were restored immediately in wave 20 because they are high-frequency agent workflows
- resume skills were explicitly retained after wave 25 because they form a real procedural pipeline rather than redundant writing wrappers

That same logic should be applied to other deleted skills that support business operations, content systems, research, design-to-code, or artifact delivery.

## Status Update

A first Round B subset has now been applied:

- `send-email` moved from `writing-blog` to `cloud-platform`
- `stripe-integration` moved from `development-core` to `cloud-platform`
- `figma` was promoted into the public catalog and added to `design-ui`

A follow-up content-workflow update has also now been applied:

- `technical-blog-writing` was promoted into the public catalog and added to `writing-blog`
- local `infsh` CLI installation has been verified, though real execution still requires an authenticated inference.sh account

A high-confidence Round C cleanup has also now been applied:

- `claude-automation-recommender` was removed from the public catalog and `core-meta`
- `claude-opus-4-5-migration` was removed from the public catalog and `development-core`

A follow-up Figma review also clarified one duplication boundary:

- `figma-implement-design` remains non-public for now because the public catalog already includes `implement-design` as the active Figma-to-code on-demand entrypoint

## Bucket A: Keep Pruned

These deletions still look sound even after broadening the lens. They are mostly true overlap, environment conflict, or overly narrow vendor/tool wrappers that do not deserve default residency.

| Skill | Wave | Current Public State | Recommended Action | Why |
|---|---:|---|---|---|
| `audit-website` | 22 | not public | keep pruned | Useful, but bound to `squirrelscan`; superseded by more standard browser/perf audit paths. |
| `claude-opus-4-5-migration` | 22 | not public | keep pruned | One-time migration utility, not durable daily capability. |
| `claude-automation-recommender` | 22 | not public | keep pruned | Claude-specific meta-setup advice; weak fit for a cross-agent curated layer. |
| `react-web` | 23 | not public | keep pruned | Broad React umbrella, largely superseded by `react-dev`. |
| `react-components` | 23 | not public | keep pruned | Bound to the proprietary Stitch workflow. |
| `better-auth-best-practices` | 24 | not public | keep pruned | Fragmentary sub-skill under the already-kept `better-auth`. |
| `create-auth-skill` | 24 | not public | keep pruned | Same Better Auth overlap problem; too partial. |
| `email-and-password-best-practices` | 24 | not public | keep pruned | Same Better Auth overlap problem; too partial. |
| `coding-standards` | 26 | not public | keep pruned | Pure umbrella guidance, low procedural value. |
| `backend-patterns` | 26 | not public | keep pruned | Broad overlap with `nodejs-backend-patterns` and `architecture-patterns`. |
| `frontend-patterns` | 26 | not public | keep pruned | Broad overlap with `react-dev`, Next.js, and frontend-design skills. |
| `frontend-testing` | 28 | not public | keep pruned | Explicitly Dify-specific. |
| `react-testing` | 28 | not public | keep pruned | Generic testing wrapper; weaker than `vitest` + `webapp-testing`. |
| `internal-comms` | 29 | not public | keep pruned | Communication matters, but this one is strongly company-internal and template-bound. |
| `authjs-skills` | 30 | not public | keep pruned | Direct auth-library overlap after choosing `better-auth` as the local canonical path. |
| `vani-async-client-only` | 31 | not public | keep pruned | Very narrow rendering model helper; not a broad agent capability. |

## Bucket B: Public Or On-Demand Only

These skills are valuable, but they do not need to live in the tiny default local set. The right home is usually the public catalog, a profile, or `find-skills`-based restoration.

| Skill | Wave | Current Public State | Recommended Action | Why |
|---|---:|---|---|---|
| `find-docs` | 31b | public (`context7-integration`) | keep pruned locally, keep public | Valuable, but local user-level install conflicts with the Gemini Context7 extension copy. |
| `gsap` | 20 | public (`design-ui`) | public/on-demand | Important motion toolkit, but not default-resident. |
| `motion` | 20 | public (`design-ui`) | public/on-demand | Same as GSAP; useful when needed, noisy when always resident. |
| `convex-best-practices` | 21 | public (`development-core`) | public/on-demand | Real backend capability, just framework-specific. |
| `remotion-best-practices` | 21 | public (`design-ui`) | public/on-demand | Valuable for video generation workflows, but niche. |
| `redis-js` | 21 | public (`database-data`) | public/on-demand | Useful infrastructure capability, but provider-specific. |
| `polars` | 21 | public (`database-data`) | public/on-demand | Strong data-analysis capability, but specialized. |
| `react-modernization` | 23 | public (`development-core`) | public/on-demand | Real migration workflow, but not worth default activation. |
| `postgresql-table-design` | 27 | public (`database-data`) | public/on-demand | Good schema design skill; local dedupe against Supabase/Postgres is still defensible. |
| `sql-optimization-patterns` | 27 | public (`database-data`) | public/on-demand | Valuable generic DB skill, but local Postgres truth-source dedupe is defensible. |
| `e2e-testing-patterns` | 28 | public (`development-core`) | public/on-demand | Good conceptual testing guidance, but weaker than the local procedural toolkits kept. |
| `stripe-best-practices` | 21 | public (`development-core`) | public/on-demand | Important monetization knowledge, but best activated when payments are actually in scope. |

## Bucket C: Candidate Restore, Rewrite, Or Public Promotion

These are the deletions that most likely suffered from a coding-first or overly narrow default-set lens. Some should remain pruned locally, but they should be treated as important agent capabilities rather than noise.

| Skill | Wave | Current Public State | Recommended Action | Why |
|---|---:|---|---|---|
| `figma` | 22 | public (`design-ui`) | keep public/on-demand | Design-token extraction and design-to-code are real agent workflows, not fluff. |
| `figma-implement-design` | 22 | not public | keep non-public for now | Figma-to-code is a valid implementation surface, but the public catalog already exposes the overlapping `implement-design` skill with stronger current public signal. |
| `send-email` | 22 | public (`cloud-platform`) | keep public | Transactional email is core solo-founder/business capability, not a minor SaaS edge case. |
| `stripe-integration` | 21 | public (`cloud-platform`) | keep public | Payments are central business infrastructure, not just an occasional API wrapper. |
| `blog-post` | 29 | not public | rewrite before restore or public promotion | High-value long-form content pipeline, but written against unavailable `task` + `generate_cover` contracts. |
| `technical-blog-writing` | 29 | public (`writing-blog`) | keep public/on-demand, consider future rewrite | Valuable technical content workflow; `infsh` is now installable locally, but the workflow still depends on authenticated inference.sh access. |
| `ai-elements` | 31 | public (`design-ui`) | keep public, consider optional local restore for AI-product work | Strong AI-native UI surface, not mere cosmetic library noise. |
| `web-artifacts-builder` | 31 | public (`design-ui`) | keep public, consider optional local restore for artifact-heavy work | Artifact/demo delivery is a legitimate agent output surface, especially for prototypes and rich deliverables. |

## Most Important Re-Read

If only a small number of deleted skills are revisited, prioritize these seven:

1. `blog-post`
2. `technical-blog-writing`
3. `send-email`
4. `stripe-integration`
5. `ai-elements`
6. `web-artifacts-builder`
7. `figma`

## Implications

- The local default set can remain strict without collapsing the broader idea of what agents do.
- Public-catalog decisions should not inherit local-default pruning logic mechanically.
- Non-coding workflows should only be removed when they are truly low-fit, overlapping, or environment-broken, not just because they are not code-generation skills.

## Suggested Next Round

If a follow-up public-catalog pass happens, the best Round B candidates are:

1. Re-evaluate whether `blog-post` and `technical-blog-writing` deserve public inclusion after adapting them to the current environment.
2. Re-check profile placement for `send-email` and `stripe-integration`.
3. Revisit whether `figma-implement-design` offers enough differentiated value beyond the already-public `implement-design` skill.
4. If Figma on-demand coverage expands, decide whether `code-connect-components` or another Figma MCP specialist should be promoted instead of duplicating the existing implement-design slot.

## Draft Round B Actions

This is the most concrete next-pass proposal for the seven highest-priority skills:

| Skill | Draft Action | Target Profile | Notes |
|---|---|---|---|
| `blog-post` | rewrite before public | `writing-blog` | High-value long-form pipeline, but current `task researcher` + `generate_cover` contract must be rewritten first. |
| `technical-blog-writing` | keep public/on-demand, future rewrite optional | `writing-blog` | Better fit than `blog-post` for the repo's technical audience; public inclusion is now reasonable, but removing the hard `infsh` dependency would make it more portable. |
| `send-email` | keep public but move profile | `cloud-platform` | Business infrastructure skill; current placement under `writing-blog` is misleading. |
| `stripe-integration` | keep public but move profile | `cloud-platform` | Business infrastructure, not a default core-development skill. |
| `ai-elements` | keep public as-is | `design-ui` | Strong AI-native UI capability; current public placement is reasonable. |
| `web-artifacts-builder` | keep public as-is | `design-ui` | Legitimate artifact/prototype output surface; keep until/unless a dedicated artifact profile exists. |
| `figma` | promote to public | `design-ui` | Design-token extraction and design-to-code are real agent workflows; best Round B promotion candidate. |

If only one of the two blog skills gets adapted first, `blog-post` is now the clearer rewrite target because `technical-blog-writing` has already been promoted for on-demand public use.
