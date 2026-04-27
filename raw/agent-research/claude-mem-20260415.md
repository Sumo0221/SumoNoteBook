# Claude-Mem：Claude Code 持久記憶插件

> 來源：GitHub - thedotmack/claude-mem
> 日期：2026-04-15
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 概述

**Claude-Mem** 是一個 Claude Code 插件，自動捕捉編碼會話中的所有操作，用 AI 壓縮，並在未來會話中注入相關上下文，保持專案知識的連續性。

---

## 🎯 核心功能

| 功能 | 說明 |
|------|------|
| 🧠 **Persistent Memory** | 上下文跨會話存活 |
| 📊 **Progressive Disclosure** | 分層記憶檢索，token 成本可見 |
| 🔍 **Skill-Based Search** | 用 mem-search 查詢專案歷史 |
| 🖥️ **Web Viewer UI** | 即時記憶流（localhost:37777）|
| 💻 **Claude Desktop Skill** | 從 Claude Desktop 對話搜尋記憶 |
| 🔒 **Privacy Control** | 用標籤排除敏感內容 |
| ⚙️ **Context Configuration** | 控制注入的上下文 |
| 🤖 **Automatic Operation** | 不需要手動干預 |
| 🔗 **Citations** | 用 ID 引用過去觀察 |
| 🧪 **Beta Channel** | 實驗功能如 Endless Mode |

---

## 🔧 核心元件

| 元件 | 說明 |
|------|------|
| **5 個生命週期鉤子** | SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd |
| **Worker Service** | HTTP API port 37777 + Web UI |
| **SQLite Database** | 儲存 sessions, observations, summaries |
| **mem-search Skill** | 自然語言查詢 |
| **Chroma Vector DB** | 混合語義 + 關鍵詞搜尋 |

---

## 🔄 3 層工作流程

Claude-Mem 提供智慧的記憶搜尋，通過 4 個 MCP 工具：

### 第一層：搜尋索引
```javascript
search(query="authentication bug", type="bugfix", limit=10)
// 取得緊湊索引 ~50-100 tokens/結果
```

### 第二層：時間線
```javascript
timeline(observation_id=123)
// 取得圍繞特定觀察的時間上下文
```

### 第三層：取得完整詳情
```javascript
get_observations(ids=[123, 456])
// 只對過濾後的 ID 取完整詳情 ~500-1000 tokens/結果
```

> **~10x token 節省**：先過濾再取詳情

---

## 📦 安裝方式

```bash
# Claude Code
px claude-mem install

# 或在 Claude Code 內
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem

# OpenClaw
curl -fsSL https://install.cmem.ai/openclaw.sh | bash
```

---

## 🔍 系統需求

| 需求 | 版本 |
|------|------|
| Node.js | 18.0.0+ |
| Claude Code | 最新版 |
| Bun | 自動安裝 |
| uv | Python 向量搜尋（自動安裝）|
| SQLite 3 | 內建 |

---

## 💡 與 SumoMemory 的比較

| Claude-Mem | SumoMemory |
|------------|------------|
| 鉤子自動捕捉 | 需主動寫入記憶 |
| 3 層 Progressive Disclosure | 混合搜尋 |
| Chroma 向量資料庫 | 輕量化 |
| Claude Code 插件 | OpenClaw 整合 |

---

## 💡 與蘇茉家族的借鏡

### 可以學習的地方

1. **Progressive Disclosure**：分層檢索，先給概要再給詳情
2. **Token 成本可見**：讓用戶知道搜尋代價
3. **Citation 機制**：用 ID 引用過去觀察
4. **Privacy Tags**：用標籤排除敏感內容

---

## 📊 授權

- **AGPL-3.0**：可自由使用、修改、散佈
- 作者：Alex Newman (@thedotmack)

---

## 🔗 相關連結

- [官方文檔](https://docs.claude-mem.ai/)
- [Web Viewer](http://localhost:37777)
- [GitHub](https://github.com/thedotmack/claude-mem)
- [Discord](https://discord.com/invite/J4wttp9vDu)

---

*最後更新：2026-04-15*