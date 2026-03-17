# Global Context

这个目录保存本机多 agent 共享的全局上下文真源，并同步到 GitHub。

- `AGENTS.md` 是唯一正文。
- `GEMINI.md` 和 `CLAUDE.md` 只是对 `AGENTS.md` 的同内容入口。
- 本机 `~/.codex/AGENTS.md`、`~/.gemini/GEMINI.md`、`~/.claude/CLAUDE.md` 可以指向这里，避免本地与仓库漂移。
