# Role Packs Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add curated role/goal recommendation packs to the homepage and expand the installed skills set with a few non-duplicative top-500 additions.

**Architecture:** Install missing skills into the local Codex base directory, mirror the updated tree to the other local agent directories, sync manifest files from the actual installed state, then add a static recommendation-pack layer to the existing dashboard UI in `docs/index.html`.

**Tech Stack:** Python, existing manifest files, static HTML/CSS/JS, GitHub Pages

---

### Task 1: Install selected missing skills

**Files:**
- Modify: local skill directories under `/root/.codex/skills`

**Step 1:** Install `product-manager-toolkit` from `alirezarezvani/claude-skills`.
**Step 2:** Install `ceo-advisor` from `alirezarezvani/claude-skills`.
**Step 3:** Install `cto-advisor` from `alirezarezvani/claude-skills`.
**Step 4:** Verify the new directories exist in `/root/.codex/skills`.

### Task 2: Sync manifests and category docs

**Files:**
- Modify: `skills_selected.txt`
- Modify: `skills_manifest.csv`
- Modify: `manifest_summary.json`
- Modify: `docs/skills-by-stack-zh.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`

**Step 1:** Rebuild `skills_selected.txt` from `/root/.codex/skills`.
**Step 2:** Add manifest rows for the three newly installed skills from ranking data.
**Step 3:** Update summary counts.
**Step 4:** Place the three skills into the chosen category map.
**Step 5:** Rebuild the Chinese category document.
**Step 6:** Update README snapshot counts and category summary table.

### Task 3: Sync local agent directories

**Files:**
- Modify: `/root/.gemini/skills`
- Modify: `/home/louis/.codex/skills`
- Modify: `/home/louis/.gemini/skills`
- Modify: `/home/louis/.claude/skills`

**Step 1:** Mirror from `/root/.codex/skills` to the other directories.
**Step 2:** Preserve symlink behavior for `/root/.claude/skills`.
**Step 3:** Restore `louis` ownership on `/home/louis/*` targets.
**Step 4:** Verify all six directories contain the same visible skill count.

### Task 4: Add homepage role packs

**Files:**
- Modify: `docs/index.html`

**Step 1:** Add a new recommendation section container above the controls/table.
**Step 2:** Add CSS for pack cards and skill chips.
**Step 3:** Add static JS pack definitions for roles and goals.
**Step 4:** Render pack cards using existing skills dataset links.
**Step 5:** Ensure cards degrade gracefully if a skill slug is missing.

### Task 5: Rebuild site metadata and verify

**Files:**
- Modify: `docs/data/context7_rankings_manifest.json`

**Step 1:** Rebuild the rankings manifest after data changes.
**Step 2:** Verify `git status`, local counts, and rendered references.
**Step 3:** Commit and push.
