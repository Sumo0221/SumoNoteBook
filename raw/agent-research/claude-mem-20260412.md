# Claude-Mem 研究：Claude Code 的持久記憶插件

> 來源：GitHub - thedotmack/claude-mem
> 日期：2026-04-12
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 概述

Claude-Mem 無縫保存跨 session 的上下文，自動捕捉工具使用觀察、生成語意摘要，並讓未來 session 可取用。這讓 Claude 能維持專案知識的連續性，即使 session 結束或重新連接後也能記住。

**官方網站**：https://docs.claude-mem.ai/

---

## 核心功能

| 功能 | 說明 |
|------|------|
| 🧠 Persistent Memory | Context 跨 session 存活 |
| 📊 Progressive Disclosure | 分層記憶檢索，節省 token |
| 🔍 Skill-Based Search | 用自然語言查詢專案歷史 |
| 🖥️ Web Viewer UI | 即時記憶串流（localhost:37777）|
| 🔒 Privacy Control | 用 tags 排除敏感內容 |
| ⚙️ Context Configuration | 細粒度控制哪些 context 被注入 |
| 🤖 Automatic Operation | 自動運作，無需手動 |
| 🔗 Citations | 用 ID 引用過去的觀察 |

---

## 🔄 三層工作流程（節省 10x token）

| 步驟 | 功能 | Token 消耗 |
|------|------|------------|
| **search** | 取得緊湊索引（帶 ID）| ~50-100 tokens/結果 |
| **timeline** | 取得時間上下文 | 中等 |
| **get_observations** | 只對過濾後的 ID 取完整內容 | ~500-1,000 tokens/結果 |

### 工作流程

```javascript
// Step 1: 搜尋索引（便宜）
search(query="認證 bug", type="bugfix", limit=10)

// Step 2: 人工審視，找出相關 ID（如 #123, #456）

// Step 3: 取完整細節（貴）
get_observations(ids=[123, 456])
```

**核心思想**：先用便宜的搜尋過濾，再對少數感興趣的 ID 取完整內容，節省 10x token。

---

## 🏗️ 系統架構

| 元件 | 功能 |
|------|------|
| **5 個 Lifecycle Hooks** | SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd |
| **Worker Service** | HTTP API on port 37777 + Web Viewer |
| **SQLite Database** | 儲存 sessions, observations, summaries |
| **Chroma Vector DB** | 混合語意 + 關鍵詞搜尋 |
| **mem-search Skill** | 自然語言查詢 |

### Lifecycle Hooks

| Hook | 時機 |
|------|------|
| SessionStart | session 開始時 |
| UserPromptSubmit | 提交 prompt 時 |
| PostToolUse | 工具使用後 |
| Stop | 停止時 |
| SessionEnd | session 結束時 |

---

## 📦 安裝方式

```bash
# Claude Code
px claude-mem install

# Gemini CLI
px claude-mem install --ide gemini-cli

# OpenClaw
curl -fsSL https://install.cmem.ai/openclaw.sh | bash
```

### 需求
- Node.js: 18.0.0+
- Claude Code: 最新版（plugin 支援）
- Bun: JavaScript runtime（自動安裝）
- uv: Python package manager（自動安裝）
- SQLite 3: 持久儲存

---

## 📊 與蘇茉家族的對應

| Claude-Mem | 蘇茉家族現狀 | 狀態 |
|-------------|-------------|------|
| Persistent Memory | MemPalace | ✅ 我們有 |
| Progressive Disclosure | SCBKR 格式 | ✅ 我們有 |
| 3-Layer Workflow | ❌ 沒有 | 可以借鑒 |
| Web Viewer UI | ❌ 沒有 | 可以參考 |
| Chroma Vector DB | ❌ 只有純文字 | 可以升級 |
| Lifecycle Hooks | HEARTBEAT.md | ⚠️ 部分對應 |
| OpenClaw 整合 | 本身是 OpenClaw | ✅ |
| Search API | ❌ 沒有 | 可以借鑒 |

---

## 💡 對蘇茉家族最有價值的概念

### 1. 三層工作流程（省 10x token）

先用便宜的搜尋過濾，再對少數感興趣的 ID 取完整內容。

### 2. Web Viewer UI（port 37777）

即時查看記憶狀態的網頁介面。

### 3. Lifecycle Hooks 完整綁定

5 個 hook 覆盖 session 的完整生命週期。

---

## 相關連結

- [官方文檔](https://docs.claude-mem.ai/)
- [GitHub](https://github.com/thedotmack/claude-mem)
- [OpenClaw 整合指南](https://docs.claude-mem.ai/openclaw-integration)

---

*最後更新：2026-04-12*
