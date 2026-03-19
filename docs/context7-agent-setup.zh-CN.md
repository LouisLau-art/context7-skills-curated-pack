# Codex、Gemini CLI、Claude Code 的 Context7 接法

这份文档说明这个工作区里最常用的三种 agent 应该如何接入 Context7：

- Codex
- Gemini CLI
- Claude Code

## 推荐结论

优先级建议如下：

1. **Context7 MCP + 薄的一层指令/skill**
2. **只有在 MCP 不方便时，才退回 skill-only**

原因很直接：

- MCP 负责统一的外部工具能力
- `AGENTS.md` / `GEMINI.md` / `CLAUDE.md` 负责稳定行为规则
- skill 适合做工作流包装，但不该被当成 MCP 的通用替代品

## 对应到本 repo

这个 repo 现在已经提供了一个可选公开 profile：

- `context7-integration`

当前包含：

- `context7-docs-lookup`
- `context7-mcp`
- `find-docs`

示例：

```bash
python scripts/install_curated.py codex --profiles context7-integration
python scripts/install_curated.py gemini --profiles context7-integration
python scripts/install_curated.py claude --profiles context7-integration
python scripts/install_curated.py all --profiles context7-integration
```

## Codex

### 全局规则

行为规则放在：

- `~/.codex/AGENTS.md`

示例：

```markdown
Always use Context7 MCP when I need library/API documentation, setup, configuration, or code examples.
```

### MCP 配置

MCP server 放在：

- `~/.codex/config.toml`

远端 server：

```toml
[mcp_servers.context7]
url = "https://mcp.context7.com/mcp"
http_headers = { "CONTEXT7_API_KEY" = "YOUR_API_KEY" }
```

本地 server：

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
startup_timeout_ms = 20_000
```

如果启动慢，可以把 `startup_timeout_ms` 提高到 `40_000`。

## Gemini CLI

### 全局规则

行为规则放在：

- `~/.gemini/GEMINI.md`

示例：

```markdown
Always use Context7 MCP when I need library/API documentation, setup, configuration, or code examples.
```

### MCP 配置

MCP server 放在：

- `~/.gemini/settings.json`

远端 server：

```json
{
  "mcpServers": {
    "context7": {
      "httpUrl": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "YOUR_API_KEY",
        "Accept": "application/json, text/event-stream"
      }
    }
  }
}
```

本地 server：

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

常用内建命令：

- `/mcp list`
- `/mcp refresh`
- `/memory show`
- `/memory refresh`
- `/memory add`

## Claude Code

### 全局规则

行为规则放在：

- `~/.claude/CLAUDE.md`

示例：

```markdown
Always use Context7 MCP when I need library/API documentation, setup, configuration, or code examples.
```

### MCP 配置

推荐用 user-scope 的远端接法：

```bash
claude mcp add --scope user --header "CONTEXT7_API_KEY: YOUR_API_KEY" --transport http context7 https://mcp.context7.com/mcp
```

本地 server：

```bash
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

校验：

```bash
claude mcp list
```

### Plugin 说明

对 Claude Code 来说，Context7 还可以走 plugin 方案。  
如果你不只是想要 MCP，而是还想要额外的 commands、agents、skills，那 plugin 路线更强。

## 什么时候可以接受 skill-only

只有这些情况我觉得可以直接用 skill-only：

- 只是想快速本地开箱
- 当前环境不方便接 MCP
- 只需要轻量级 docs 查询

但它不适合作为默认方案，尤其当你想要：

- 多 agent 一致
- 团队统一标准
- 可复用、可写进文档的配置方式

## 资料来源

- Codex docs: https://context7.com/openai/codex/llms.txt
- Gemini CLI docs: https://context7.com/google-gemini/gemini-cli/llms.txt
- Claude Code Context7 guide: https://context7.com/docs/clients/claude-code
- Context7 all-clients MCP configs: https://context7.com/docs/resources/all-clients
- Context7 best practices: https://context7.com/docs/tips
