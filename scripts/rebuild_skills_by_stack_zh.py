#!/usr/bin/env python3
"""Rebuild docs/skills-by-stack-zh.md from current skills_selected.txt.

Uses existing category mapping in docs/skills-by-stack-zh.md as source of truth,
then keeps only currently selected skills.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "skills-by-stack-zh.md"
SELECTED_PATH = ROOT / "skills_selected.txt"


def parse_sections(markdown: str) -> list[tuple[str, str]]:
    parts = re.split(r"^##\s+", markdown, flags=re.M)
    sections: list[tuple[str, str]] = []
    for part in parts:
        if not part.strip():
            continue
        lines = part.splitlines()
        title = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        sections.append((title, body))
    return sections


def main() -> int:
    selected = [s.strip() for s in SELECTED_PATH.read_text(encoding="utf-8").splitlines() if s.strip()]
    selected_set = set(selected)

    original = DOC_PATH.read_text(encoding="utf-8")
    sections = parse_sections(original)

    category_order: list[str] = []
    category_desc: dict[str, str] = {}
    category_skills: dict[str, list[str]] = {}

    for title, body in sections:
        if title.startswith("分类总览") or title.startswith("系统内置"):
            continue
        base_title = title.split("（")[0]
        if base_title not in category_order:
            category_order.append(base_title)
        if base_title not in category_desc:
            desc = ""
            for line in body.splitlines():
                line = line.strip()
                if line.startswith("主要是"):
                    desc = line
                    break
            category_desc[base_title] = desc
        if base_title not in category_skills:
            category_skills[base_title] = re.findall(r"`([^`]+)`", body)

    grouped: dict[str, list[str]] = {k: [] for k in category_order}
    missing: list[str] = []

    # Preserve current selected order while grouping by existing category map.
    for skill in selected:
        assigned = False
        for category in category_order:
            if skill in category_skills.get(category, []):
                grouped[category].append(skill)
                assigned = True
                break
        if not assigned:
            missing.append(skill)

    if missing:
        extra = "其他/未分类"
        if extra not in grouped:
            grouped[extra] = []
            category_order.append(extra)
            category_desc[extra] = "无法从既有映射中归类的条目。"
        grouped[extra].extend(missing)

    total = len(selected)
    overview = [(cat, len(grouped.get(cat, []))) for cat in category_order if grouped.get(cat)]

    lines: list[str] = []
    lines.append("# 当前 Skills 按技术栈/语言分类")
    lines.append("")
    lines.append(f"- 总计目录数: {total}（仅当前已保留 skills）")
    lines.append("- 说明: 按“主要用途”进行单标签归类，便于快速筛选。")
    lines.append("- 数据源: `skills_selected.txt`")
    lines.append("")
    lines.append("## 分类总览")
    lines.append("")
    for cat, count in overview:
        lines.append(f"- {cat}: {count}")
    lines.append("")

    for cat, count in overview:
        lines.append(f"## {cat}（{count}）")
        lines.append("")
        desc = category_desc.get(cat, "")
        if desc:
            lines.append(desc)
            lines.append("")
        skills_line = ", ".join(f"`{s}`" for s in grouped[cat])
        lines.append(skills_line)
        lines.append("")

    DOC_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Rebuilt {DOC_PATH} with {total} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
