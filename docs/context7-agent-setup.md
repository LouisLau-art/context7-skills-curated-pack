# Context7 Setup for Codex, Gemini CLI, and Claude Code

This document explains the recommended Context7 setup for the three agent environments used in this workspace:

- Codex
- Gemini CLI
- Claude Code

## Recommendation

Use this order of preference:

1. **Context7 MCP + thin instruction/skill layer** for the default setup
2. **Skill-only fallback** only when MCP is unavailable or inconvenient

Rationale:

- MCP gives a consistent external tool surface
- instruction files (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`) keep the workflow stable
- skills remain useful as reusable workflow wrappers, but should not be treated as a universal replacement for MCP

## Public Repo Mapping

This repository exposes an optional public profile for this setup:

- `context7-integration`

It currently includes:

- `context7-docs-lookup`
- `context7-mcp`
- `find-docs`

Example:

```bash
python scripts/install_curated.py codex --profiles context7-integration
python scripts/install_curated.py gemini --profiles context7-integration
python scripts/install_curated.py claude --profiles context7-integration
python scripts/install_curated.py all --profiles context7-integration
```

## Codex

### Global instructions

Put the behavior rule in:

- `~/.codex/AGENTS.md`

Example:

```markdown
Always use Context7 MCP when I need library/API documentation, setup, configuration, or code examples.
```

### MCP configuration

Put the MCP server in:

- `~/.codex/config.toml`

Remote server:

```toml
[mcp_servers.context7]
url = "https://mcp.context7.com/mcp"
http_headers = { "CONTEXT7_API_KEY" = "YOUR_API_KEY" }
```

Local server:

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
startup_timeout_ms = 20_000
```

If startup is slow, increase `startup_timeout_ms` to `40_000`.

## Gemini CLI

### Global instructions

Put the behavior rule in:

- `~/.gemini/GEMINI.md`

Example:

```markdown
Always use Context7 MCP when I need library/API documentation, setup, configuration, or code examples.
```

### MCP configuration

Put the MCP server in:

- `~/.gemini/settings.json`

Remote server:

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

Local server:

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

Useful built-ins:

- `/mcp list`
- `/mcp refresh`
- `/memory show`
- `/memory refresh`
- `/memory add`

## Claude Code

### Global instructions

Put the behavior rule in:

- `~/.claude/CLAUDE.md`

Example:

```markdown
Always use Context7 MCP when I need library/API documentation, setup, configuration, or code examples.
```

### MCP configuration

Recommended user-scope remote setup:

```bash
claude mcp add --scope user --header "CONTEXT7_API_KEY: YOUR_API_KEY" --transport http context7 https://mcp.context7.com/mcp
```

Local server:

```bash
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

Verification:

```bash
claude mcp list
```

### Plugin note

For Claude Code specifically, Context7 can also be installed as a plugin-oriented integration. That path is stronger when you want more than raw MCP access, because it can also expose commands, agents, and skills.

## When Skill-Only Is Acceptable

Skill-only is acceptable when:

- you want the fastest personal setup
- MCP is blocked by environment restrictions
- you only need lightweight docs lookup

It is not the best default when you want:

- cross-agent consistency
- team-standardized behavior
- a shared documented setup

## Sources

- Codex docs: https://context7.com/openai/codex/llms.txt
- Gemini CLI docs: https://context7.com/google-gemini/gemini-cli/llms.txt
- Claude Code Context7 guide: https://context7.com/docs/clients/claude-code
- Context7 all-clients MCP configs: https://context7.com/docs/resources/all-clients
- Context7 best practices: https://context7.com/docs/tips
