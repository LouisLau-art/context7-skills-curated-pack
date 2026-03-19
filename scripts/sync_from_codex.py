#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


SYNC_ALIAS = {
    "ampcode": "amp",
    "qwen": "gemini",
}


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync user skills from ~/.codex/skills to other agent directories."
    )
    parser.add_argument(
        "--targets",
        default="claude,gemini,opencode,amp,codebuddy",
        help="Comma-separated target dirs to sync from codex. Supported: claude, gemini, qwen(alias), opencode, amp, codebuddy.",
    )
    parser.add_argument(
        "--mode",
        choices=("copy", "symlink"),
        default="copy",
        help="How to mirror each skill into target dirs.",
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Remove target user skill dirs that are not present in ~/.codex/skills.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without changing files.",
    )
    return parser.parse_args()


def iter_user_skill_dirs(root: Path) -> dict[str, Path]:
    if not root.is_dir():
        return {}
    out: dict[str, Path] = {}
    for child in root.iterdir():
        if child.name == ".system":
            continue
        if child.is_dir() or child.is_symlink():
            out[child.name] = child
    return out


def remove_path(path: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"DRY_RUN remove: {path}")
        return
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
        return
    if path.is_dir():
        shutil.rmtree(path)


def sync_target(source_root: Path, target_root: Path, mode: str, prune: bool, dry_run: bool) -> None:
    source_skills = iter_user_skill_dirs(source_root)
    target_skills = iter_user_skill_dirs(target_root)

    if dry_run:
        print(f"DRY_RUN target: {target_root}")
    else:
        target_root.mkdir(parents=True, exist_ok=True)

    if prune:
        for stale in sorted(set(target_skills) - set(source_skills)):
            remove_path(target_root / stale, dry_run)

    for slug, src in sorted(source_skills.items()):
        dst = target_root / slug
        if mode == "symlink":
            desired = src.resolve(strict=False)
            if dst.is_symlink() and dst.resolve(strict=False) == desired:
                continue
            if dst.exists() or dst.is_symlink():
                remove_path(dst, dry_run)
            if dry_run:
                print(f"DRY_RUN symlink: {dst} -> {src}")
            else:
                dst.symlink_to(src)
            continue

        if dry_run:
            print(f"DRY_RUN copy: {src} -> {dst}")
            continue

        if dst.exists() or dst.is_symlink():
            remove_path(dst, dry_run=False)
        shutil.copytree(src, dst, symlinks=True)


def main() -> int:
    args = parse_args()
    paths = platform_skill_dirs()
    source_root = paths["codex"]
    if not source_root.is_dir():
        raise SystemExit(f"Codex skills directory not found: {source_root}")

    raw_targets = [t.strip().lower() for t in args.targets.split(",") if t.strip()]
    targets = [SYNC_ALIAS.get(t, t) for t in raw_targets]
    valid = {"claude", "gemini", "opencode", "amp", "codebuddy"}
    for target in targets:
        if target not in valid:
            raise SystemExit(f"Unsupported target: {target}")

    print(f"Source of truth: {source_root}")
    print(f"Targets: {', '.join(targets)}")
    print(f"Mode: {args.mode}")
    print(f"Prune: {args.prune}")

    for target in targets:
        sync_target(source_root, paths[target], args.mode, args.prune, args.dry_run)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
