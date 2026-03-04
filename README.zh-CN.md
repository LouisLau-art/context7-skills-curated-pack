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

# 一次安装并同步到 Codex + Gemini
bash scripts/install_curated.sh all

# 先 dry-run
DRY_RUN=1 bash scripts/install_curated.sh claude
```

支持目标：
`claude`、`codex`、`gemini`、`all`（或 `claude+codex+gemini`）、
`claude+codex`、`claude+gemini`、`codex+gemini`、
`universal`、`global`、`cursor`、`auto`

## 拉取动态榜单

### 1) Skills 排行（可按 installs 过滤）

```bash
python3 scripts/fetch_context7_skill_rankings.py \
  --min-installs 0 \
  --output-csv data/context7_ranked_skills_all.csv \
  --output-json data/context7_ranked_skills_all.meta.json
```

### 2) Docs 库排行（popular / trending / latest）

```bash
python3 scripts/fetch_context7_library_rankings.py --kind popular \
  --output-csv data/context7_popular_libraries.csv \
  --output-json data/context7_popular_libraries.meta.json
```

## 静态网站（GitHub Pages）

页面已支持三榜单：
- `Docs Popular`（Context7 API 当前提供前 50 的市场份额榜）
- `Docs Extended`（1-50 为官方榜，50 以后为基于全量库的估算扩展榜）
- `Skills Ranking`（不设 installs 阈值的全量榜单，当前为数千条）

页面与数据文件：
- `docs/index.html`
- `docs/data/context7_docs_popular_top50.json`
- `docs/data/context7_docs_extended_top1000.json`
- `docs/data/context7_skills_ranked_all.json`

数据生成命令：

```bash
python3 scripts/fetch_context7_docs_popular.py \
  --limit 50 \
  --output-json docs/data/context7_docs_popular_top50.json \
  --output-csv docs/data/context7_docs_popular_top50.csv

python3 scripts/fetch_context7_docs_extended.py \
  --top-k 20000 \
  --max-workers 12 \
  --output-json docs/data/context7_docs_extended_top1000.json \
  --output-csv docs/data/context7_docs_extended_top1000.csv

python3 scripts/fetch_context7_skills_for_site.py \
  --min-installs 0 \
  --output-json docs/data/context7_skills_ranked_all.json \
  --output-csv docs/data/context7_skills_ranked_all.csv
```

自动更新由 GitHub Actions 执行：
- `.github/workflows/update-docs-popular-site.yml`
- 触发方式：每日定时 + 手动触发

## 给其他大模型的说明书

为其他模型/Agent 准备的入口：

- 说明文档：`AI_RANKINGS_GUIDE.md`
- 机器可读清单：`docs/data/context7_rankings_manifest.json`
- 公网 manifest 地址：
  `https://louislau-art.github.io/context7-skills-curated-pack/data/context7_rankings_manifest.json`
- Raw GitHub 兜底地址：
  `https://raw.githubusercontent.com/LouisLau-art/context7-skills-curated-pack/main/docs/data/context7_rankings_manifest.json`

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
