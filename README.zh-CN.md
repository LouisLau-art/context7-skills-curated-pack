# Context7 Skills Curated Pack（中文说明）

[English](README.md) | [简体中文](README.zh-CN.md)

一个面向开发流程的 Context7 skills 精选与去重仓库。

在线页面（GitHub Pages）：
https://louislau-art.github.io/context7-skills-curated-pack/

当前快照：**163 个可安装 skills**（另含内部 `.system`，本地目录总数 164）。

## 这个仓库包含什么

- `skills_manifest.csv`：已选技能清单（含 source/installs/trust/score）
- `skills_selected.txt`：纯技能名列表
- `scripts/install_curated.sh`：一键安装脚本
- `scripts/fetch_context7_skill_rankings.py`：拉取 skills 动态排行榜
- `scripts/fetch_context7_library_rankings.py`：拉取 docs 库排行榜（popular/trending/latest）
- `scripts/fetch_context7_docs_popular.py`：拉取 docs popular 并生成站点数据
- `docs/index.html`：静态排行榜页面

不包含第三方技能原始 `SKILL.md` 文件（避免重复托管上游内容）。

## 快速开始

```bash
# 安装到 Claude 目标目录
bash scripts/install_curated.sh claude

# 先 dry-run
DRY_RUN=1 bash scripts/install_curated.sh claude
```

支持目标：`claude`、`universal`、`global`、`auto`

## 拉取动态榜单

### 1) Skills 排行（可按 installs 过滤）

```bash
python3 scripts/fetch_context7_skill_rankings.py \
  --min-installs 36 \
  --output-csv data/context7_ranked_skills_min36.csv \
  --output-json data/context7_ranked_skills_min36.meta.json
```

### 2) Docs 库排行（popular / trending / latest）

```bash
python3 scripts/fetch_context7_library_rankings.py --kind popular \
  --output-csv data/context7_popular_libraries.csv \
  --output-json data/context7_popular_libraries.meta.json
```

## 静态网站（GitHub Pages）

页面已支持双榜单：
- `Docs Popular`（Context7 API 当前提供前 50 的市场份额榜）
- `Skills Ranking`（`installs >= 36`，当前约 240 条）

页面与数据文件：
- `docs/index.html`
- `docs/data/context7_docs_popular_top50.json`
- `docs/data/context7_skills_ranked_min36.json`

数据生成命令：

```bash
python3 scripts/fetch_context7_docs_popular.py \
  --limit 50 \
  --output-json docs/data/context7_docs_popular_top50.json \
  --output-csv docs/data/context7_docs_popular_top50.csv

python3 scripts/fetch_context7_skills_for_site.py \
  --min-installs 36 \
  --output-json docs/data/context7_skills_ranked_min36.json \
  --output-csv docs/data/context7_skills_ranked_min36.csv
```

自动更新由 GitHub Actions 执行：
- `.github/workflows/update-docs-popular-site.yml`
- 触发方式：每日定时 + 手动触发

## 当前 163 技能分布（摘要）

- Frontend & Web UI: 46
- LLM / Agent / Prompting: 27
- Mobile: 18
- Backend & Services: 16
- Testing & QA: 11
- Engineering Workflow: 10
- Database & Data Engineering: 9
- Docs & Office Automation: 8
- Cloud & DevOps: 7
- Python / AI / Data Science: 6
- Security & Architecture: 5

详细分类见：`docs/skills-by-stack-zh.md`

## 许可

- 本仓库脚本与清单：MIT
- 上游 skills 版权与许可：归各自原仓库所有
