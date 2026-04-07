# 全局指令 (Shared AGENT Config)

## 🎯 核心原则
- **沟通**：始终使用中文。
- **环境 (混合模式)**：
  - **系统级**：Ubuntu 优先使用 `nala` (作为 `apt` 的现代替代品)，负责底层库、系统工具和桌面软件。
  - **开发级**：Python 强制使用 `uv`；JS/TS 优先用 `bun`；Node.js 环境管理使用 `nvm`。
  - **Strict Tool Persistence**：对于常用工具，严禁使用临时运行器（如 `uvx`, `npx`）。必须执行持久化安装（`uv tool install`, `npm install -g`），以确保环境稳定性、性能和离线可用性。
  - **最佳实践**：开发工具链优先使用对应的语言包管理器以获取最新版本，仅在涉及内核、驱动或系统服务时使用 `nala`。
- **工具**：优先使用 MCP（Context7, GitHub MCP）而非普通 Web Search。
- **GitHub**：如果用户发了 GitHub 网址，强制使用 `gh` CLI 或 GitHub MCP 工具查看。
- **技能**：任务开始及过程中优先调用已安装或 Context7 的 Skill。
- **自动化**：强制使用非交互式标志（-y, --yes），减少 Terminal 确认。

## 🛠️ 开发与工作流
- **胶水编程**：优先复用成熟方案/SDK，自定义代码仅做连接。
- **检索**：做事前先查 GitHub 已有开源方案或最佳实践。
- **文档**：处理报告/PPT/Word/PDF时，主动选用文档类技能。
- **优化**：遇到失败或发现更好做法时，用 `self-improving-agent` 沉淀结论。
- **算法刷题**：
  - 算法题刷题主要使用 Python，对 Java 语法不熟悉
  - 所有算法题解题优先使用 Python 实现

## ⚠️ 关键约定
- **Skills**：单次任务仅限 1-3 个 Skill，优先 focused/compact 类型。
- **同步**：本文件是三端（Codex, Claude, Gemini）唯一真源。
- **补丁**：`session-handoff` 必须保留，已应用 `###` 标题补丁。
- **特性**：主动利用 `js_repl`, `multi_agent`, `memories`, `guardian approval`, `prevent_idle_sleep`。

## 🤖 模型配置

### 智谱AI GLM（免费模型）
- **免费模型**：`glm-4.7-flash`、`glm-4.6v-flash`（视觉多模态）
- **API Base**：`https://open.bigmodel.cn/api/paas/v4/`
- **API Key**：`<填写你的智谱API Key>`
- **调用示例**：
  ```bash
  curl https://open.bigmodel.cn/api/paas/v4/chat/completions \
    -H "Authorization: Bearer <API_KEY>" \
    -H "Content-Type: application/json" \
    -d '{"model": "glm-4.7-flash", "messages": [{"role": "user", "content": "你好"}]}'
  ```
- **获取 Key**：https://bigmodel.cn/usercenter/proj-mgmt/apikeys
