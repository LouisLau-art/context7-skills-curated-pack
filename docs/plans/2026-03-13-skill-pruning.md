# Skill Pruning Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reduce the curated pack from 176 skills to 126 by removing the 50 approved slugs and updating the supporting documentation to match the new selection policy.

**Architecture:** Filter the two source-of-truth manifest files using the approved delete list, then regenerate derived counts and rewrite the pruning policy so the repo documents source-priority curation instead of the old installs-first heuristic.

**Tech Stack:** Markdown, CSV manifest data, Python helper scripts

---

### Task 1: Add the approved delete list to the repo workflow

**Files:**
- Create: `docs/plans/2026-03-13-skill-pruning.md`
- Modify: `skills_selected.txt`
- Modify: `skills_manifest.csv`
- Modify: `manifest_summary.json`

**Step 1: Define the approved delete list**

Use the 50 confirmed slugs from the review session as the canonical filter input.

**Step 2: Filter `skills_selected.txt`**

Remove every approved slug while preserving the original order of retained skills.

**Step 3: Filter `skills_manifest.csv`**

Remove the same slugs while preserving the original CSV column order and retained row order.

**Step 4: Update summary metadata**

Set `skills_count` to the retained count and refresh the generation timestamp in `manifest_summary.json`.

### Task 2: Update derived documentation

**Files:**
- Modify: `docs/dedup-policy.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `docs/skills-by-stack-zh.md`

**Step 1: Rewrite de-dup policy**

Document source priority, overlap caps, and manual content review rules.

**Step 2: Update README snapshot counts**

Replace `176/177` references with the new curated pack counts and adjust the curation label to reflect the new policy.

**Step 3: Regenerate stack grouping**

Run `scripts/rebuild_skills_by_stack_zh.py` after updating `skills_selected.txt`.

**Step 4: Refresh README distribution summary**

Update the English and Chinese summaries so their category counts match the regenerated grouping.

### Task 3: Verify the result

**Files:**
- Modify: `skills_selected.txt`
- Modify: `skills_manifest.csv`
- Modify: `manifest_summary.json`
- Modify: `docs/dedup-policy.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `docs/skills-by-stack-zh.md`

**Step 1: Count retained skills**

Verify both manifest sources report `126`.

**Step 2: Spot-check deleted slugs**

Confirm representative removed slugs no longer appear in the manifest files.

**Step 3: Spot-check retained slugs**

Confirm the explicitly retained borderline skills still exist in the manifest files.
