# DeerFlow - 位元組跳動的超級 Agent 框架

> 來源：GitHub - bytedance/deer-flow
> 日期：2026-04-14
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 概述

**全名**：Deep Exploration and Efficient Research Flow
**公司**：ByteDance（位元組跳動）
**排名**：2026 年 2 月 28 日 GitHub Trending #1

**標語**：「An open-source long-horizon SuperAgent harness that researches, codes, and creates.」

---

## 🎯 核心理念

用戶只需要一句話，就能讓 coding agent 幫你完成所有設定和開發任務。

---

## 🔧 支援的模型

| 模型 | 推薦程度 |
|------|----------|
| **Doubao-Seed-2.0-Code** | 推薦 |
| **DeepSeek v3.2** | 推薦 |
| **Kimi 2.5** | 推薦 |
| GPT-4o | 支援 |
| Claude Sonnet 4.6 | 支援 |
| Qwen3 | 支援 |

---

## 🏗️ 架構特色

### 1. 標準模式 vs Gateway 模式

| 模式 | 架構 | 行程數 |
|------|------|--------|
| **標準模式** | LangGraph Server + Gateway API | 4 processes |
| **Gateway 模式**（實驗性）| Gateway API 直接處理 Agent | 3 processes |

### 2. 部署規模

| 用途 | CPU | RAM | SSD |
|------|-----|-----|-----|
| 本地開發 | 4-8 vCPU | 8-16 GB | 20 GB |
| Docker 開發 | 8 vCPU | 16 GB | 25 GB |
| 長期運行伺服器 | 16 vCPU | 32 GB | 40 GB |

---

## 🛠️ 核心功能

### 1. Sub-Agents
- 協調多個子代理
- 每個子代理擅長不同任務

### 2. Memory（長期記憶）
- 持久化記憶
- 可載入範例記憶資料

### 3. Sandbox（沙盒）
- 安全執行環境
- 隔離危險操作

### 4. Skills & Tools
- 可擴展的技能系統
- MCP Server 整合

### 5. Claude Code 整合
- 可以呼叫 Claude Code
- Codex CLI 支援

---

## 🔌 MCP Server 支援

DeerFlow 支援 MCP Server，可以連接外部工具和服務。

---

## 🌐 InfoQuest 整合

BytePlus 開發的智慧搜尋和爬蟲工具集，已整合到 DeerFlow。

---

## 📋 與蘇茉家族的對比

| 項目 | DeerFlow | 蘇茉家族 |
|------|----------|----------|
| **定位** | 超級 Agent harness | 多 Agent 協調框架 |
| **核心** | LangGraph | sessions_spawn |
| **Sub-agents** | ✅ 有 | ✅ 有（12 個蘇茉）|
| **Memory** | ✅ 有 | ✅ 有（SumoMemory、MemPalace）|
| **Sandbox** | ✅ 有 | ❌ 目前沒有 |
| **Skills** | ✅ 可擴展 | ✅ 可擴展 |
| **MCP** | ✅ 支援 | ❌ 目前沒有 |

---

## 💡 對蘇茉家族的啟發

### 1. Gateway 模式
- 把 Agent 執行直接嵌入 API
- 簡化架構，減少行程數
- 可以研究如何簡化我們的架構

### 2. 沙盒安全
- DeerFlow 有專門的沙盒環境
- 我們可以考慮加入類似機制
- 特別是執行外部腳本時

### 3. 記憶系統
- DeerFlow 的記憶系統設計
- 可以借鑒到 SumoMemory

---

## 🔗 連結

- GitHub：https://github.com/bytedance/deer-flow
- 官網：https://deerflow.tech

---

*最後更新：2026-04-14*