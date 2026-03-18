# Skill Curation Cleanup Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Remove cloud/mobile local skills that no longer fit the user's workflow and document SkillsBench-inspired curation rules in the repo.

**Architecture:** Treat the local Codex skill directory and the repo docs as separate sources of truth. First remove local-only skills that violate the approved scope, then update repo-facing documentation so future curation decisions explicitly follow the same paper-backed rules.

**Tech Stack:** Markdown, local filesystem operations, Python one-liners, repo documentation

---

### Task 1: Remove disallowed local skills

**Files:**
- Modify: `/home/louis/.codex/skills/`

**Step 1: Confirm delete candidates**

Run:

```bash
python - <<'PY'
from pathlib import Path
skills_dir = Path('/home/louis/.codex/skills')
cloud = ['aws-solution-architect','github-actions-templates','senior-devops','terraform-module-library','vercel-deploy','wrangler']
mobile = ['building-native-ui','expo-api-routes','expo-cicd-workflows','expo-deployment','expo-dev-client','expo-tailwind-setup','flutter','mobile-android-design','mobile-ios-design','native-data-fetching','react-native-architecture','react-native-best-practices','react-native-components','react-native-design','upgrading-expo','use-dom','vercel-react-native-skills']
for slug in cloud + mobile:
    print(slug, (skills_dir / slug).exists())
PY
```

Expected: only existing local directories are listed for removal.

**Step 2: Remove local cloud/mobile skills**

Run:

```bash
python - <<'PY'
from pathlib import Path
import shutil
skills_dir = Path('/home/louis/.codex/skills')
targets = ['aws-solution-architect','github-actions-templates','senior-devops','terraform-module-library','vercel-deploy','wrangler','building-native-ui','expo-api-routes','expo-cicd-workflows','expo-deployment','expo-dev-client','expo-tailwind-setup','flutter','mobile-android-design','mobile-ios-design','native-data-fetching','react-native-architecture','react-native-best-practices','react-native-components','react-native-design','upgrading-expo','use-dom','vercel-react-native-skills']
for slug in targets:
    path = skills_dir / slug
    if path.exists():
        shutil.rmtree(path)
        print(f"deleted {slug}")
PY
```

**Step 3: Verify removal**

Run:

```bash
python - <<'PY'
from pathlib import Path
skills_dir = Path('/home/louis/.codex/skills')
targets = ['aws-solution-architect','github-actions-templates','senior-devops','terraform-module-library','vercel-deploy','wrangler','building-native-ui','expo-api-routes','expo-cicd-workflows','expo-deployment','expo-dev-client','expo-tailwind-setup','flutter','mobile-android-design','mobile-ios-design','native-data-fetching','react-native-architecture','react-native-best-practices','react-native-components','react-native-design','upgrading-expo','use-dom','vercel-react-native-skills']
print([slug for slug in targets if (skills_dir / slug).exists()])
PY
```

Expected: `[]`

### Task 2: Document SkillsBench-backed curation rules

**Files:**
- Modify: `/home/louis/context7-skills-curated-pack/README.md`
- Modify: `/home/louis/context7-skills-curated-pack/README.zh-CN.md`
- Modify: `/home/louis/context7-skills-curated-pack/AGENT.md`

**Step 1: Add explicit curation principles to README**

Document:
- do not choose by installs alone
- prefer focused 2-3 module skills over broad documentation
- curated human-authored procedural skills beat self-generated skill content
- prioritize skills that reduce verification failures and complete workflows

**Step 2: Mirror the same guidance in Chinese README**

Keep the same policy but adapted to the repo's Chinese terminology.

**Step 3: Add a short agent-facing curation note to AGENT.md**

Make it clear that future ranking refreshes and skill additions should follow the paper-backed rules.

### Task 3: Validate final state

**Files:**
- Modify: `/home/louis/context7-skills-curated-pack/README.md`
- Modify: `/home/louis/context7-skills-curated-pack/README.zh-CN.md`
- Modify: `/home/louis/context7-skills-curated-pack/AGENT.md`

**Step 1: Count remaining local skills**

Run:

```bash
python - <<'PY'
from pathlib import Path
skills = [p.name for p in Path('/home/louis/.codex/skills').iterdir() if p.is_dir() and p.name != '.system']
print(len(skills))
PY
```

**Step 2: Spot-check doc wording**

Run:

```bash
rg -n "SkillsBench|focused|self-generated|verification failures|下载量|skills.sh" README.md README.zh-CN.md AGENT.md
```

**Step 3: Review repo status**

Run:

```bash
git status --short
```
