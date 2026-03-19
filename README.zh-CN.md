# Context7 Skills Curated Pack（中文说明）

[English](README.md) | [简体中文](README.zh-CN.md)

一个面向多 agent 软件工作流的公开 skills catalog 与 profile 安装仓库，同时附带多来源排行榜站点。

在线页面（GitHub Pages）：
https://louislau-art.github.io/context7-skills-curated-pack/

当前快照：**120 个公开可安装 skills**。默认公开安装档 `public-default` 当前会安装 **78 个 skills**；`all-public` 会安装完整的 120 个公开 catalog skills（另含内部 `.system`）。

## 这个仓库包含什么

- `skills_manifest.csv`：已选技能清单（含 source/installs/trust/score）
- `skills_selected.txt`：公开 catalog 的兼容导出列表
- `profiles/`：公开安装档，例如 `core-meta`、`development-core`、`writing-blog`
- `scripts/install_curated.py`：跨平台一键安装器
- `scripts/install_curated.sh`：对 Python 安装器的 Unix 薄封装
- `scripts/install_curated.ps1`：对 Python 安装器的 PowerShell 薄封装
- `scripts/validate_skills_frontmatter.py`：安装后校验/修复 `SKILL.md` frontmatter
- `scripts/fetch_skills_sh_rankings.py`：抓取 `skills.sh` 预渲染榜单并生成站点数据
- `scripts/fetch_context7_skill_rankings.py`：拉取 skills 动态排行榜
- `scripts/fetch_context7_library_rankings.py`：拉取 docs 库排行榜（popular/trending/latest）
- `scripts/fetch_context7_docs_popular.py`：拉取 docs popular 并生成站点数据
- `docs/index.html`：静态排行榜页面
- `docs/troubleshooting.md`：常见安装/认证/frontmatter 排障
- `global-context/`：同步到 GitHub 的全局 agent 上下文真源，供 Codex / Gemini / Claude 共用

不包含第三方技能原始 `SKILL.md` 文件；仓库只保留清单、安装器与同步逻辑。

## 为什么这么做

- 维护成本更低
- 可以稳定地从上游重新安装
- 避免在仓库里重复托管第三方 skill 文件
- 更容易把同一套精选 skills 同步到多个 agent 目录

## 快速开始

```bash
# 安装默认公开 profile 到 Claude 兼容基准目录
python scripts/install_curated.py claude --profiles public-default

# 安装完整公开 catalog
python scripts/install_curated.py claude --profiles all-public

# 一次安装，并同步到 Codex + Gemini + OpenCode + Amp + CodeBuddy
python scripts/install_curated.py all --profiles public-default

# 在默认 profile 基础上叠加写作/博客 profile
python scripts/install_curated.py claude --profiles public-default+writing-blog

# 求职/简历导向安装
python scripts/install_curated.py codex --profiles resume-job-search

# Unix 便捷包装
bash scripts/install_curated.sh all --profiles public-default

# Windows PowerShell 包装
powershell -ExecutionPolicy Bypass -File .\scripts\install_curated.ps1 all --profiles public-default

# 查看当前公开 profiles
python scripts/install_curated.py --list-profiles

# 先 dry-run
DRY_RUN=1 python scripts/install_curated.py claude+opencode+amp --profiles public-default+cloud-platform
```

PowerShell 的 dry-run 示例：

```powershell
$env:DRY_RUN = "1"
.\scripts\install_curated.ps1 qwen --profiles public-default
```

## 公开 Profiles

这个 repo 现在区分三层：

- **public catalog**：`skills_manifest.csv` 里的全部公开技能
- **public profiles**：`profiles/` 下的场景化安装档
- **private local overlay**：维护者本地私有扩展，不直接当作公开产品一部分

当前公开 profiles：

- `core-meta`：发现、验证、review、规划、会话衔接
- `development-core`：开发主流程 starter
- `writing-blog`：写作/博客 starter
- `resume-job-search`：简历/求职 starter
- `docs-office`：PDF / DOCX / PPTX / 办公文档处理
- `cloud-platform`：Vercel / Supabase / Hugging Face / 平台相关
- `design-ui`：设计与前端 UI
- `database-data`：数据库、RAG、数据工作流

安装器内置别名：

- `public-default = core-meta + development-core`
- `all-public = 所有公开 profiles 的并集`

支持目标：
- `claude`（默认）
- `codex`：通过 Claude 兼容目录安装，再同步到 `~/.codex/skills`
- `gemini`：同步到 `~/.gemini/skills`
- `qwen`：`gemini` 的别名，共用同一个 skills 目录
- `opencode`：Unix 类系统默认同步到 `~/.config/opencode/skills`；Windows 默认同步到 `%APPDATA%\\opencode\\skills`
- `amp` / `ampcode`：Unix 类系统默认同步到 `~/.config/agents/skills`；Windows 默认同步到 `%APPDATA%\\agents\\skills`
- `codebuddy`：同步到 `~/.codebuddy/skills`
- `all` / `claude+codex+gemini+opencode+amp+codebuddy`
- 自定义组合，例如 `claude+codex+opencode`、`claude+gemini+amp+codebuddy`、`claude+qwen`
- `universal`、`global`、`cursor`、`auto`（仅安装，不做后续同步）

安装器会把 `skills_manifest.csv` 当作公开 catalog，再从 `profiles/` 解析一个或多个安装档，只安装匹配到的 skills；随后在 Claude 兼容基准目录里校验并修复已知 `SKILL.md` frontmatter 问题，再把本地生成的 skills 目录同步到兼容 agent 的目录中；并不会把第三方 `SKILL.md` vendoring 到本仓库。

### 目录覆盖

如果你的本地目录不是默认路径，可以先设置环境变量：

```bash
export CLAUDE_SKILLS_DIR=/custom/claude/skills
export CODEX_SKILLS_DIR=/custom/codex/skills
export GEMINI_SKILLS_DIR=/custom/gemini/skills
export OPENCODE_SKILLS_DIR=/custom/opencode/skills
export AMP_SKILLS_DIR=/custom/amp/skills
export CODEBUDDY_SKILLS_DIR=/custom/codebuddy/skills
```

`qwen` 复用 `GEMINI_SKILLS_DIR`。

### 以 Codex 为主目录同步

如果你希望把 `~/.codex/skills` 当作主用户技能目录，建议从 Codex 向其他 agent 做单向同步，而不是继续把 `.claude/skills` 当 source of truth：

```bash
# 先预览会改哪些目录
python scripts/sync_from_codex.py --dry-run --prune

# 把 Codex 用户 skills 复制到 Claude/Gemini/OpenCode/Amp/CodeBuddy
python scripts/sync_from_codex.py --prune

# 或者把每个 skill 目录做成软链接
python scripts/sync_from_codex.py --mode symlink --prune
```

这个脚本只同步用户 skill 目录，不会碰目标目录里的 `.system`。

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

页面已支持四榜单：
- `Skills.sh All Time`（主技能榜，当前以预渲染 payload 为起点，再补拉公开分页 API，保留前 2000 条）
- `Context7 Skills`（次技能榜，用于 Context7 专属字段和长尾补充）
- `Docs Popular`（Context7 API 当前提供前 50 的市场份额榜）
- `Docs Extended`（1-50 为官方榜，50 以后为基于全量库的估算扩展榜）

页面与数据文件：
- `docs/index.html`
- `docs/data/skills_sh_all_time_top2000.json`
- `docs/data/context7_docs_popular_top50.json`
- `docs/data/context7_docs_extended_top1000.json`
- `docs/data/context7_skills_ranked_all.json`

数据生成命令：

```bash
python3 scripts/fetch_skills_sh_rankings.py \
  --view all-time \
  --limit 2000 \
  --output-json docs/data/skills_sh_all_time_top2000.json \
  --output-csv docs/data/skills_sh_all_time_top2000.csv

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

## 当前 120 技能分布（摘要）

- 前端与 Web UI: 34
- LLM / Agent / Prompting: 13
- 后端与服务端: 12
- 测试与质量保障: 8
- 工程流程与协作: 21
- 数据库与数据工程: 10
- 文档与办公自动化: 9
- 其他 / 未分类: 2
- Python / AI / 数据科学: 6
- 安全与架构: 6

详细分类见：`docs/skills-by-stack-zh.md`

## 当前裁剪规则

对高重叠主题，按下面顺序裁剪：

1. 优先官方来源和知名强仓库
2. 每个主题只保留 `1` 个通用 skill，加 `1-2` 个真正专用 skill
3. 优先处理触发条件冲突和工作流重叠，名字是否相同只是弱信号
4. 接近的候选再做内容复核，优先触发描述更清晰、附带脚本/参考资料更多的项
5. `installs/trust/verified` 只做辅助 tie-break，不再作为主规则

详细规则见：`docs/dedup-policy.md`

## SkillsBench 启发的补充规则

本仓库会把 `skills.sh` 榜单当作发现入口，而不是“高下载量就自动入选”的白名单。
下载量重要，但不能压过范围匹配和内容质量。

选型时额外遵循下面几条：

1. 优先人工编写、强调操作流程的 procedural skill，而不是泛提示词或模型临时自生成的 skill 内容
2. 优先范围收敛、模块数少但有效的 focused skill，而不是“大而全”的泛文档型 skill
3. 优先能帮助 agent 更稳定完成并校验任务的 skill，尤其是能减少 `quality below threshold` 这类失败的 skill
4. 两个候选覆盖同一工作时，仍优先官方源或强维护者来源

落地时意味着：

- `skills.sh` 的安装量只作为热度信号，不能单独决定去留
- 不符合当前工作流的云端、移动端技能，即使热门也可以移除
- 下载量较低但更聚焦的简历、博客、代码审查类 skill，可以优先于高下载量的泛写作类 skill
- 除非真有明确专长差异，否则不保留同工作流重复 skill
- 同名 skill 不会自动判重；不同名字的 skill 只要会抢同一类触发词，也算冲突候选

## 许可

- 本仓库脚本与清单：MIT
- 上游 skills 版权与许可：归各自原仓库所有
