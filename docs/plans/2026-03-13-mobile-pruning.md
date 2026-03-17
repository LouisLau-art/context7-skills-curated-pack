# Mobile Skill Pruning Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Remove the remaining mobile and Expo-focused skills from the curated pack because there is no active mobile development need.

**Architecture:** Drop the 12 mobile slugs from the manifest sources, refresh snapshot counts in repo docs, regenerate the stack breakdown, and prune the same directories from both local `~/.codex/skills` trees.

**Tech Stack:** Markdown, CSV manifest data, local filesystem sync

---

### Task 1: Remove mobile skills from the source manifests

**Files:**
- Create: `docs/plans/2026-03-13-mobile-pruning.md`
- Modify: `skills_selected.txt`
- Modify: `skills_manifest.csv`
- Modify: `manifest_summary.json`

**Step 1: Define the delete set**

Use the remaining mobile slugs as the canonical delete list:
`building-native-ui`, `expo-api-routes`, `expo-cicd-workflows`, `expo-deployment`, `expo-dev-client`, `expo-tailwind-setup`, `flutter`, `mobile-android-design`, `mobile-ios-design`, `native-data-fetching`, `upgrading-expo`, `use-dom`.

**Step 2: Filter the source files**

Remove those slugs from `skills_selected.txt` and `skills_manifest.csv` while preserving the order of retained entries.

**Step 3: Refresh summary metadata**

Update `manifest_summary.json` so the retained count becomes `114`.

### Task 2: Refresh derived docs

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `docs/skills-by-stack-zh.md`

**Step 1: Update snapshot counts**

Change the curated-pack snapshot from `126/127` to `114/115`.

**Step 2: Regenerate stack classification**

Run `scripts/rebuild_skills_by_stack_zh.py` so the mobile category is removed from the current pack summary.

**Step 3: Update README distribution summaries**

Replace the previous category counts so they match the regenerated doc.

### Task 3: Sync local installs

**Files:**
- Modify: `/root/.codex/skills/*`
- Modify: `/home/louis/.codex/skills/*`

**Step 1: Remove deleted local skill directories**

Delete the 12 matching directories from both local Codex skill roots, leaving `.system` untouched.

**Step 2: Verify the result**

Confirm both users now have `114` curated skills plus `.system`, for `115` total top-level directories.
