# Context7 Skills Curated Pack（中文说明）

[English](README.md) | [简体中文](README.zh-CN.md)

一个面向开发流程的 Context7 skills 精选与去重仓库。

在线页面（GitHub Pages）：
https://louislau-art.github.io/context7-skills-curated-pack/

当前快照：**170 个可安装 skills**（另含内部 `.system`，本地目录总数 171）。

## 这个仓库包含什么

- `skills_manifest.csv`：已选技能清单（含 source/installs/trust/score）
- `skills_selected.txt`：纯技能名列表
- `scripts/install_curated.py`：跨平台一键安装器
- `scripts/install_curated.sh`：对 Python 安装器的 Unix 薄封装
- `scripts/install_curated.ps1`：对 Python 安装器的 PowerShell 薄封装
- `scripts/fetch_context7_skill_rankings.py`：拉取 skills 动态排行榜
- `scripts/fetch_context7_library_rankings.py`：拉取 docs 库排行榜（popular/trending/latest）
- `scripts/fetch_context7_docs_popular.py`：拉取 docs popular 并生成站点数据
- `docs/index.html`：静态排行榜页面

不包含第三方技能原始 `SKILL.md` 文件；仓库只保留清单、安装器与同步逻辑。

## 为什么这么做

- 维护成本更低
- 可以稳定地从上游重新安装
- 避免在仓库里重复托管第三方 skill 文件
- 更容易把同一套精选 skills 同步到多个 agent 目录

## 快速开始

```bash
# 跨平台：安装到 Claude 兼容基准目录
python scripts/install_curated.py claude

# 一次安装，并同步到 Codex + Gemini + OpenCode + Amp
python scripts/install_curated.py all

# Qwen 兼容用法（复用 Gemini skills 目录）
python scripts/install_curated.py qwen

# Unix 便捷包装
bash scripts/install_curated.sh all

# Windows PowerShell 包装
powershell -ExecutionPolicy Bypass -File .\scripts\install_curated.ps1 all

# 先 dry-run
DRY_RUN=1 python scripts/install_curated.py claude+opencode+amp
```

PowerShell 的 dry-run 示例：

```powershell
$env:DRY_RUN = "1"
.\scripts\install_curated.ps1 qwen
```

支持目标：
- `claude`（默认）
- `codex`：通过 Claude 兼容目录安装，再同步到 `~/.codex/skills`
- `gemini`：同步到 `~/.gemini/skills`
- `qwen`：`gemini` 的别名，共用同一个 skills 目录
- `opencode`：Unix 类系统默认同步到 `~/.config/opencode/skills`；Windows 默认同步到 `%APPDATA%\\opencode\\skills`
- `amp` / `ampcode`：Unix 类系统默认同步到 `~/.config/agents/skills`；Windows 默认同步到 `%APPDATA%\\agents\\skills`
- `all` / `claude+codex+gemini+opencode+amp`
- 自定义组合，例如 `claude+codex+opencode`、`claude+gemini+amp`、`claude+qwen`
- `universal`、`global`、`cursor`、`auto`（仅安装，不做后续同步）

安装器会直接读取 `skills_manifest.csv`，从上游 Context7 来源安装，再把本地生成的 skills 目录同步到兼容 agent 的目录中；并不会把第三方 `SKILL.md` vendoring 到本仓库。

### 目录覆盖

如果你的本地目录不是默认路径，可以先设置环境变量：

```bash
export CLAUDE_SKILLS_DIR=/custom/claude/skills
export CODEX_SKILLS_DIR=/custom/codex/skills
export GEMINI_SKILLS_DIR=/custom/gemini/skills
export OPENCODE_SKILLS_DIR=/custom/opencode/skills
export AMP_SKILLS_DIR=/custom/amp/skills
```

`qwen` 复用 `GEMINI_SKILLS_DIR`。

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

### Context7 API Key（建议）

为了提升限额，运行抓取脚本前建议设置：

```bash
export CONTEXT7_API_KEY='your_ctx7_key'
```

可移植替代方案：
- `CONTEXT7_API_KEY_FILE=/path/to/key.txt`（读取首行 token）
- `CONTEXT7_ALLOW_CODEX_MCP_FALLBACK=1`：显式允许从 Codex MCP 配置（`~/.codex/config.toml`）读取

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

## 当前 170 技能分布（摘要）

- 前端与 Web UI: 46
- LLM / Agent / Prompting: 27
- 移动端: 18
- 后端与服务端: 16
- 测试与质量保障: 11
- 工程流程与协作: 10
- 数据库与数据工程: 9
- 文档与办公自动化: 8
- 云与 DevOps / 基础设施: 7
- 其他 / 未分类: 7
- Python / AI / 数据科学: 6
- 安全与架构: 5

详细分类见：`docs/skills-by-stack-zh.md`

## 许可

- 本仓库脚本与清单：MIT
- 上游 skills 版权与许可：归各自原仓库所有
