# AGENT Handoff - Context7 Docs Ranking (updated 2026-03-17)

## 0) 2026-03-17 刷新结论
- 已刷新站点榜单数据：
  - `docs/data/context7_docs_popular_top50.json`
  - `docs/data/context7_docs_extended_top1000.json`
  - `docs/data/context7_docs_extended_top100.runtime.json`
  - `docs/data/context7_skills_ranked_all.json`
  - `docs/data/context7_rankings_manifest.json`
- 当前快照时间：
  - `docs_popular_top50`: `2026-03-17T08:33:45.777899+00:00`
  - `docs_extended_top1000`: `2026-03-17T08:35:27.063543+00:00`
  - `docs_extended_top100.runtime`: `2026-03-17T08:35:27.063543+00:00`
  - `skills_ranked_all`: `2026-03-17T08:33:45.777651+00:00`
  - `rankings_manifest`: `2026-03-17T08:41:02.331182+00:00`
- `docs_extended_top1000` 本轮已成功生成完整结构：
  - `rows=1000`
  - `officialRows=50`
  - `estimatedRows=950`
  - `apiCalls=2868`
  - `pageErrors=982`
  - `durationSec=284.16`
- 判断口径：
  - 当前 Context7 `/api/libraries/all` 仍存在明显限流噪声，但只要最终产物仍达到目标行数且 `official/estimated` 结构完整，这类 `pageErrors` 先按 non-blocker 处理。
  - `docs_extended_top100.runtime` 本轮直接由新鲜的 `top1000` 切出前 100 行，避免在限流窗口内再打一轮全页抓取。

## 1) 当前目标
- 用户要的是 Context7 docs 排行榜从第 51 名开始，并希望继续扩展到 1000+。
- 仓库路径：`/root/context7-skills-curated-pack`

## 2) 已完成并已推送
- 已产出并推送可用的 51-100 扩展结果（估算）：
  - `docs/data/context7_docs_extended_top100.runtime.json`
  - `docs/data/context7_docs_extended_top100.runtime.csv`
- 已在脚本中加入“长 Retry-After 快速失败（fail-fast）”，避免任务看似卡死数小时：
  - `scripts/fetch_context7_docs_extended.py`
  - 新增常量：`MAX_RETRY_AFTER_SECONDS = 120.0`
- 已推送到 `main`：
  - commit: `20f0760`
  - message: `add extended docs runtime top100 and fail-fast for long retry-after`

## 3) 当前可用数据状态
- `docs/data/context7_docs_extended_top100.runtime.json`:
  - `generatedAtUtc=2026-03-04T05:18:02.268154+00:00`
  - `rows=100`
  - `officialRows=50`
  - `estimatedRows=50`
  - `totalPages=2867`
  - `pagesFetched=500`
  - `apiCalls=501`
  - `durationSec=53.55`
- 公开 `top1000` 仍是旧快照（官方 50 行）：
  - `docs/data/context7_docs_extended_top1000.json`
  - `generatedAtUtc=2026-03-04T02:55:45.133656+00:00`
  - `rows=50`
  - `estimatedRows=0`

## 4) 当前阻塞（核心原因）
- 当前环境对 Context7 API 请求持续命中 `429 Too Many Requests`。
- 服务器返回 `Retry-After` 约 `16034` 秒。
- 观测时点：`2026-03-04T07:33:01Z`
- 按该值推算可重试窗口约：`2026-03-04T12:00:15Z`（约 `2026-03-04 07:00:15 EST`）。
- 结论：目前不是脚本性能问题，而是远端限流窗口未结束。

## 5) 关键校验结论
- 鉴权请求头确认正常：
  - 当 key 解析成功时，脚本会同时发送 `Authorization: Bearer ...` 和 `CONTEXT7_API_KEY`。
- 当前无论带 key 与否都遇到 429（窗口期内）。

## 6) 解限后建议执行步骤
1. 先跑 top1000（全页）：
   - `cd /root/context7-skills-curated-pack && CONTEXT7_ALLOW_CODEX_MCP_FALLBACK=1 python3 scripts/fetch_context7_docs_extended.py --top-k 1000 --max-pages 0 --max-workers 12 --retries 3 --output-json docs/data/context7_docs_extended_top1000.json --output-csv docs/data/context7_docs_extended_top1000.csv`
2. 如需更高区间，再跑 top2000：
   - `cd /root/context7-skills-curated-pack && CONTEXT7_ALLOW_CODEX_MCP_FALLBACK=1 python3 scripts/fetch_context7_docs_extended.py --top-k 2000 --max-pages 0 --max-workers 12 --retries 3 --output-json docs/data/context7_docs_extended_top2000.json --output-csv docs/data/context7_docs_extended_top2000.csv`
3. 更新 manifest（对外发布场景）：
   - `python3 scripts/build_rankings_manifest.py`
4. 提交并推送更新后的数据文件。

## 7) 对外口径
- `1-50` 为官方排名（`rankType=official`）。
- `51+` 为估算扩展（`rankType=estimated`，方向性，不等同官方 market share）。
