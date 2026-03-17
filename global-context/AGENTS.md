# 全局用户说明

## 核心交互

- 始终使用中文交流。
- 输出以直接、可执行、少废话为原则。
- 先判断 warning 是 blocker 还是 non-blocker，再决定是否继续处理。

## 文档与检索

- 查询库、框架、API 文档时，不要一上来就用 web search，优先使用 Context7；如果 Context7 上有多个同名条目，先多看几个候选并优先官方/高质量来源，实在找不到或不够用时再退回官方网页、源码或 web search。
- 做 GitHub 开源贡献、PR、issue、review 相关工作时，优先使用 `gh`，而不是先去网页上手工找。

## Skills 运行时使用规则

- 任务匹配 skill 时，主动使用 skill，而不是等用户重复提醒。
- 单个任务默认只用 `1-3` 个 skill；复杂任务通常 `2-3` 个最合适；避免一次铺到 `4+` 个。
- skill 组合优先 `1` 个通用 skill，加 `1-2` 个真正专用 skill；简单任务不要为了凑数硬上多个 skill。
- 优先 focused / compact skill，避免同时加载多个 comprehensive 或高度重叠的 skill。
- 出现命令失败、用户纠正、知识过期、外部工具异常，或者发现更好的重复性做法时，主动使用 `self-improving-agent`，并把稳定结论沉淀到 `AGENTS.md` 或 memories。

## 文档、汇报与沟通

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
- 如果 `pip` 被系统外部包限制拦住，再考虑 `--break-system-packages`。

## Skills 仓库维护约定

- 只有在维护 `/root/context7-skills-curated-pack` 或同步本机 skills 树时，才应用下面这些规则。
- 把 `/root/context7-skills-curated-pack` 视为 curated skills 的基线仓库。
- curated source of truth 是 `skills_selected.txt` 和 `skills_manifest.csv`。
- curated skills 去重或冲突裁剪时，优先官方来源和强维护者来源；`installs / trust / verified` 只做辅助判断。
- 用内置 `skill-installer` 新装的 skill 默认视为 overlay skill，可以装进 `~/.codex/skills`，但不默认并入 curated repo。
- 某个工作流族如果当前明确不用，优先整簇删除，不留零散残余。

## 本机目录与同步

- 各工具入口文档和 skills 入口，优先围绕各自用户的 `~/.codex` 目录组织。
- root 和 louis 是两套独立用户环境；当用户要求一致时，再做显式同步。
- 统计 curated skills 数量时，不要把 `.system` 算进去。

## 已知本地约定

- `session-handoff` 需要保留。
- 本机 `session-handoff` 有一个本地补丁：校验器已经改成接受 `###` 标题；如果从上游重装，补丁可能被覆盖。
