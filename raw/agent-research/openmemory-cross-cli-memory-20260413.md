# OpenMemory - 跨 CLI 共享長期記憶

> 來源：GitHub - vancelin/openmemory
> 日期：2026-04-13
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 專案概述

讓所有 AI CLI（Claude Code、OpenCode、Codex CLI、Gemini CLI）共享長期記憶，**無需手動啟停**。

---

## 🎯 核心理念

> 「Share long-term memory across all your AI agents — no manual start/stop needed.」

---

## 🔄 運作方式

```
終端機 1: claude → OpenMemory 啟動 (refcount=1)
終端機 2: opencode → 共用同一個伺服器 (refcount=2)
終端機 3: gemini → 共用同一個伺服器 (refcount=3)
終端機 4: codex → 共用同一個伺服器 (refcount=4)
終端機 1: 關閉 → 仍然運行 (refcount=3)
...
最後一個關閉 → 自動停止 (refcount=0)
```

---

## ✨ 特色

| 特色 | 說明 |
|------|------|
| **零設定** | 不需要 API Key、不需要 Docker、不需要外部服務 |
| **自動生命週期** | 第一個 CLI 啟動時伺服器啟動，最後一個關閉時自動停止 |
| **跨工具記憶** | 所有 CLI 共用同一個記憶庫 |
| **參考計數** | 安全的多終端機使用，自動清理 |
| **崩潰復原** | 伺服器意外停止時自動重置計數器 |

---

## 🏗️ 架構

```
┌─────────────┐ ┌────────────┐ ┌──────────────┐ ┌──────┐
│ Claude Code │ │ OpenCode  │ │ Gemini CLI  │ │Codex │
│  HTTP MCP  │ │  HTTP MCP │ │  HTTP MCP   │ │ STDIO│
└──────┬──────┘ └──────┬────┘ └──────┬──────┘ └──┬───┘
       │               │             │            │
       └───────────────┼─────────────┘          │
                       ▼                        │
              ┌─────────────────┐         Python │
              │ OpenMemory MCP  │          Proxy │
              │   伺服器        │◄──────────────┘
              │ localhost:8080  │
              └─────────────────┘
```

---

## 🔧 技術規格

| 項目 | 說明 |
|------|------|
| **嵌入方式** | 合成式嵌入（不需要 API Key）|
| **向量資料庫** | SQLite |
| **記憶架構** | HSG 分層記憶 |
| **MCP 工具** | store, query, list, get, reinforce, delete |

---

## 🛠️ MCP 工具

| 工具 | 說明 |
|------|------|
| `openmemory_store` | 儲存記憶（文字、事實）|
| `openmemory_query` | 語意搜尋 |
| `openmemory_list` | 列出最近的記憶 |
| `openmemory_get` | 依 ID 取得單筆記憶 |
| `openmemory_reinforce` | 提升記憶顯著性 |
| `openmemory_delete` | 依 ID 刪除記憶 |

---

## 💡 對蘇茉家族的啟發

### 1. 參考計數機制
- 可以用類似方式管理蘇茉家族各 Agent 的啟動/停止
- 最後一個 Agent 關閉時自動停止服務

### 2. 跨工具記憶共享
- 不同 AI CLI 共用同一個記憶庫
- 蘇茉家族可以實現跨 Session 的記憶共享

### 3. 合成式嵌入（不需要 API Key）
- 可以用本地模型做嵌入，不需要昂貴的 API

---

## 📦 安裝需求

- Python 3.10+
- Node.js 18+
- curl、lsof（標準工具）

---

## 🔗 連結

- GitHub：https://github.com/vancelin/openmemory
- 基於：OpenMemory（CaviraOSS）

---

*最後更新：2026-04-13*