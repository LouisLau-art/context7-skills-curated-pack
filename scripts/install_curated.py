#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import os
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

BASE_TARGET_FLAGS = {
    "claude": "--claude",
    "universal": "--universal",
    "global": "--global",
    "cursor": "--cursor",
    "auto": None,
}
SYNC_TARGETS = ("codex", "gemini", "opencode", "amp", "codebuddy")
SYNC_ALIAS = {
    "ampcode": "amp",
    "qwen": "gemini",
}


@dataclass(frozen=True)
class SkillEntry:
    slug: str
    skill_name: str
    source: str


def env_truthy(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install the curated Context7 skills pack and sync it to compatible agent directories."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="claude",
        help=(
            "Install target. Examples: claude, codex, gemini, opencode, amp, codebuddy, qwen, all, "
            "claude+codex+gemini+opencode+amp+codebuddy+qwen, universal, global, cursor, auto"
        ),
    )
    parser.add_argument(
        "--manifest",
        default=str(Path(__file__).resolve().parent.parent / "skills_manifest.csv"),
        help="Path to skills_manifest.csv",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=env_truthy("DRY_RUN", False),
        help="Print install and sync commands without making changes",
    )
    return parser.parse_args()


def platform_skill_dirs() -> dict[str, Path]:
    home = Path.home()
    appdata = Path(os.getenv("APPDATA", str(home)))
    if os.name == "nt":
        opencode_default = appdata / "opencode" / "skills"
        amp_default = appdata / "agents" / "skills"
    else:
        opencode_default = home / ".config" / "opencode" / "skills"
        amp_default = home / ".config" / "agents" / "skills"
    return {
        "claude": Path(os.getenv("CLAUDE_SKILLS_DIR", str(home / ".claude" / "skills"))).expanduser(),
        "codex": Path(os.getenv("CODEX_SKILLS_DIR", str(home / ".codex" / "skills"))).expanduser(),
        "gemini": Path(os.getenv("GEMINI_SKILLS_DIR", str(home / ".gemini" / "skills"))).expanduser(),
        "opencode": Path(os.getenv("OPENCODE_SKILLS_DIR", str(opencode_default))).expanduser(),
        "amp": Path(os.getenv("AMP_SKILLS_DIR", str(amp_default))).expanduser(),
        "codebuddy": Path(os.getenv("CODEBUDDY_SKILLS_DIR", str(home / ".codebuddy" / "skills"))).expanduser(),
    }


def parse_target(raw_target: str) -> tuple[str, list[str]]:
    normalized = raw_target.replace(",", "+").strip()
    if not normalized:
        normalized = "claude"
    tokens = [SYNC_ALIAS.get(token.strip().lower(), token.strip().lower()) for token in normalized.split("+") if token.strip()]
    if not tokens:
        tokens = ["claude"]

    if tokens == ["all"]:
        return "claude", list(SYNC_TARGETS)

    base_target: str | None = None
    sync_targets: list[str] = []

    for token in tokens:
        if token in BASE_TARGET_FLAGS:
            if base_target and base_target != token:
                raise SystemExit(f"Conflicting base targets: {base_target} and {token}")
            base_target = token
            continue
        if token == "all":
            for sync_target in SYNC_TARGETS:
                if sync_target not in sync_targets:
                    sync_targets.append(sync_target)
            continue
        if token in SYNC_TARGETS:
            if token not in sync_targets:
                sync_targets.append(token)
            continue
        raise SystemExit(f"Unsupported target token: {token}")

    if base_target is None:
        base_target = "claude"

    if base_target != "claude" and sync_targets:
        raise SystemExit(
            "Sync targets require the Claude-compatible base install. "
            "Use 'claude+codex+gemini+opencode+amp+codebuddy' style targets for multi-agent sync."
        )

    return base_target, sync_targets


def load_manifest(manifest_path: Path) -> list[SkillEntry]:
    if not manifest_path.is_file():
        raise SystemExit(f"Manifest not found: {manifest_path}")

    entries: list[SkillEntry] = []
    seen_slugs: set[str] = set()
    with manifest_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"slug", "skill_name", "source"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise SystemExit(f"Manifest is missing required columns: {sorted(required)}")
        for row_num, row in enumerate(reader, start=2):
            slug = (row.get("slug") or "").strip()
            skill_name = (row.get("skill_name") or "").strip()
            source = (row.get("source") or "").strip()
            if not slug or not skill_name or not source:
                raise SystemExit(f"Malformed manifest row {row_num}: {row}")
            if slug in seen_slugs:
                raise SystemExit(f"Duplicate slug in manifest: {slug}")
            seen_slugs.add(slug)
            entries.append(SkillEntry(slug=slug, skill_name=skill_name, source=source))
    return entries


def ensure_command(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Required command not found in PATH: {name}")


def run_install(entry: SkillEntry, flag: str | None, dry_run: bool) -> None:
    cmd = ["npx", "ctx7", "skills", "install"]
    if flag:
        cmd.append(flag)
    cmd.extend([entry.source, entry.skill_name])

    if dry_run:
        print(f"DRY_RUN install: {shlex.join(cmd)}")
        return

    subprocess.run(cmd, check=True)


def sync_dir(src: Path, dst: Path, dry_run: bool) -> None:
    if src.resolve(strict=False) == dst.resolve(strict=False):
        print(f"Skip sync (same real directory): {src} -> {dst}")
        return
    if dry_run:
        print(f"DRY_RUN sync: {src} -> {dst}")
        return
    if not src.is_dir():
        print(f"WARN: source directory does not exist, skip sync: {src}")
        return
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst, dirs_exist_ok=True)
    print(f"Synced skills: {src} -> {dst}")


def verify_expected_dirs(base_dir: Path, entries: list[SkillEntry]) -> list[str]:
    missing = []
    for entry in entries:
        if not (base_dir / entry.slug).is_dir():
            missing.append(entry.slug)
    return missing


def run_post_install_validation(base_dir: Path, entries: list[SkillEntry], dry_run: bool) -> None:
    if dry_run:
        print(
            "DRY_RUN validate: "
            f"{base_dir} (slugs={len(entries)}) via scripts/validate_skills_frontmatter.py"
        )
        return

    from validate_skills_frontmatter import validate_skill_tree

    summary = validate_skill_tree(base_dir, slugs=[entry.slug for entry in entries], check_only=False)
    print(
        "Post-install frontmatter validation: "
        f"valid={summary.valid} fixed={summary.fixed} invalid={summary.invalid} missing={summary.missing}"
    )

    for result in summary.results:
        if result.status not in {"fixed", "invalid", "missing"}:
            continue
        details = result.status.upper()
        if result.repairs:
            details += f" repairs={','.join(result.repairs)}"
        if result.error:
            details += f" error={result.error}"
        print(f"  - {result.path}: {details}")


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest).resolve()
    base_target, sync_targets = parse_target(args.target)
    entries = load_manifest(manifest_path)
    paths = platform_skill_dirs()

    ensure_command("npx")

    print(
        f"Installing curated skills (target={args.target}, base={base_target}, count={len(entries)})..."
    )
    print(f"Manifest: {manifest_path}")

    install_flag = BASE_TARGET_FLAGS[base_target]
    for index, entry in enumerate(entries, start=1):
        print(f"[{index}/{len(entries)}] {entry.skill_name} <= {entry.source}")
        run_install(entry, install_flag, args.dry_run)

    if base_target == "claude":
        run_post_install_validation(paths["claude"], entries, args.dry_run)
    else:
        print(
            f"Skipping post-install frontmatter validation for base target '{base_target}' "
            "(installer does not manage a deterministic local skills path for this target)."
        )

    synced_paths: list[tuple[str, Path]] = []
    if sync_targets:
        source_dir = paths["claude"]
        for sync_target in sync_targets:
            destination = paths[sync_target]
            sync_dir(source_dir, destination, args.dry_run)
            synced_paths.append((sync_target, destination))

    print("Done.")
    print(f"Installed via base target: {base_target}")
    if base_target == "claude":
        print(f"Base skills directory: {paths['claude']}")
    if synced_paths:
        summary = ", ".join(f"{name}={path}" for name, path in synced_paths)
        print(f"Synced targets: {summary}")

    if not args.dry_run and base_target == "claude":
        missing = verify_expected_dirs(paths["claude"], entries)
        if missing:
            print(
                "WARN: some curated slugs were not found in the Claude skills directory after install: "
                + ", ".join(missing[:20])
                + (" ..." if len(missing) > 20 else "")
            )
        else:
            print(f"Verified {len(entries)} curated skill directories in {paths['claude']}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
