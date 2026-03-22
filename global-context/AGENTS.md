# 全局用户说明

## 核心偏好

1. 始终使用中文沟通。
2. Python 包与环境管理优先使用 `uv`，除非仓库已经明确固定其他工作流。
3. JavaScript 工具安装与运行优先使用 `bun`，除非仓库已经固定使用其他包管理器或锁文件。
4. 每个非平凡任务一开始都先用 `find-skills` 或 Context7 搜索。
   由于部分顶级技能只存在于 Context7 库中而不在 skills.sh 中，在寻找技能时不仅要查阅 `skills.sh` 的全网排行榜，也要用 Context7 进行检索。先检查是否存在匹配的已安装 skill 或可安装 skill；如果用户点名某个 skill，或者任务明显匹配某个已安装 skill，先打开对应的 `SKILL.md` 并按其流程执行。在去网络上下载或寻找新的 skill 之前，**必须先去 `~/.<agent>/skills_backup` 目录里看看是否已经被我们备份和隐藏过**，如果有，优先恢复或查阅它，不要盲目去外网重新下载。
5. 优先使用 MCP，而不是普通 web search。
   文档、框架、API、SDK、CLI 工具和配置说明优先用 Context7；GitHub 相关信息默认优先用 GitHub MCP 的只读搜索/发现能力；只有当 Context7、GitHub MCP、`gh` 和本地文档都不够时，才回退到 web search。
6. 如果用户直接给的是 GitHub 仓库 URL，优先用 `gh` 或 GitHub MCP 去看仓库信息、README、目录、issue、pull request、release，不要先用普通 web search。
7. 不要只在任务开始时用一次 skill。
   只要存在合适的 skill，就应在整个任务过程中持续优先采用 skill 驱动的工作流，而不是临时即兴探索。
8. 把 GitHub 当作优先知识与方案库。
   做任何事情之前，先思考 GitHub 上是否已经有人做过、并且已经开源；能复用现成方案、成熟实现、最佳实践或相近项目时，优先先查、先比对、先借鉴，而不是默认从零开始。

## Skills 使用规则

- 单个任务默认只用 `1-3` 个 skill；复杂任务通常 `2-3` 个最合适，避免一次铺到 `4+` 个。
- skill 组合优先 `1` 个通用 skill，加 `1-2` 个真正专用 skill；简单任务不要为了凑数硬上多个 skill。
- 优先 focused / compact skill，避免同时加载多个 comprehensive 或高度重叠的 skill。
- 出现命令失败、用户纠正、知识过期、外部工具异常，或者发现更好的重复性做法时，主动使用 `self-improving-agent`，并把稳定结论沉淀到 `AGENTS.md` 或 memories。

## 文档与沟通

- 用户经常兼任产品、售前和对甲方沟通角色；遇到文档、提案、汇报、FAQ、项目更新、PPT、Word、PDF、邮件这类任务时，主动考虑文档与沟通类 skills，而不是默认只从纯开发角度处理。

## 实验特性使用策略

- 已启用且值得主动利用的实验特性包括：`js_repl`、`multi_agent`、`memories`、`guardian approval`、`prevent_idle_sleep`。
- 对可拆分、可并行、互不阻塞的任务，主动考虑 `multi_agent`。
- 对网页调试、内联 JavaScript 验证、快速 Node 侧实验，主动考虑 `js_repl`。
- 对用户长期偏好、稳定 workflow、跨会话可复用经验，主动沉淀到 memories，而不是只留在临时对话里。
- 在需要审批的环境里，如果启用了 guardian approval，让系统先走自动安全审查；不要把它当成错误。
- `prevent_idle_sleep` 是自动保活能力，不需要额外手工触发。
- `Bubblewrap sandbox` 只有在启用了受限 sandbox 模式时才有明显价值；如果当前还是 `danger-full-access`，不要误判它已经在实际隔离文件系统和网络。

## 开发方式

- 采用胶水编程思路：优先复用成熟开源项目、SDK、示例和现成实现。
- 能不重写就不重写，能黑盒复用就尽量黑盒复用。
- 自定义代码尽量只承担组合、适配、封装和连接作用。

## 包管理与系统环境

- 当前机器是 Arch Linux。
- 包管理优先级：`pacman` > `paru` > `uv` > `pip`。
- `paru` 不要在 root 下运行；需要 AUR 时切到 `louis` 用户。
- 前端包管理优先用 `bun`。
- Python 依赖优先用 `uv`；只有在确实没法走 `uv` 时才考虑 `pip`。
- 如果必须使用 `npm` 或 `pip`，优先配置镜像。
- 如果 `pip` 被系统外部包限制拦住，再考虑 `--break-system-packages`。

## Skills 仓库维护约定

- 只有在维护当前公开 skills catalog 仓库或同步本机 skills 树时，才应用下面这些规则。
- 把当前公开 skills catalog 仓库视为 curated skills 的基线仓库。
- curated source of truth 是 `skills_selected.txt` 和 `skills_manifest.csv`。
- curated skills 去重或冲突裁剪时，优先官方来源和强维护者来源；`installs / trust / verified` 只做辅助判断。
- 用内置 `skill-installer` 新装的 skill 默认视为 overlay skill，可以装进 `~/.codex/skills`，但不默认并入 curated repo。
- 某个工作流族如果当前明确不用，优先整簇删除，不留零散残余。

## 本机目录与同步

- 当前 repo 中的 `global-context/AGENTS.md` 是三端共享上下文真源，目标包括 Codex、Claude Code、Gemini CLI。
- root 和 louis 是两套独立用户环境；当用户要求一致时，再做显式同步。
- 统计 curated skills 数量时，不要把 `.system` 算进去。

## 已知本地约定

- `session-handoff` 需要保留。
- 本机 `session-handoff` 有一个本地补丁：校验器已经改成接受 `###` 标题；如果从上游重装，补丁可能被覆盖。
