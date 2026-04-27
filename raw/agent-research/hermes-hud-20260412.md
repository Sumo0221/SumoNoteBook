# Hermes-HUD 研究：AI 意識監控儀表板

> 來源：GitHub - joeynyc/hermes-hudui
> 日期：2026-04-12
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 概述

瀏覽器版的 AI 意識監控工具，為 Hermes（帶持久記憶的 AI Agent）提供 Web UI 監控儀表板。

**官網說明**：「Same data, same soul, same dashboard — now in your browser.」

---

## 🎯 核心功能

| 功能 | 說明 |
|------|------|
| **13 個 Tab** | 身份、記憶、技能、工作階段、Cron Jobs、專案、健康、成本、模式、修正、即時聊天 |
| **即時更新** | 透過 WebSocket 自動更新，無需手動刷新 |
| **4 種主題** | Neural Awakening（青色）、Blade Runner（琥珀）、fsociety（綠色）、Anime（紫色）|
| **CRT 掃描線** | 可選的復古效果 |
| **命令面板** | Ctrl+K 快速操作 |
| **成本追蹤** | 按模型追蹤 token 成本 |

---

## 📊 Tab 內容

| Tab | 內容 |
|-----|------|
| 1. Identity | Agent 身份 |
| 2. Memory | 記憶系統 |
| 3. Skills | 技能列表 |
| 4. Sessions | 工作階段 |
| 5. Cron Jobs | 排程任務 |
| 6. Projects | 專案 |
| 7. Health | 健康狀態 |
| 8. Costs | Token 成本 |
| 9. Patterns | 模式 |
| 10. Corrections | 修正記錄 |
| 11. Live Chat | 即時聊天 |

---

## 🖥️ 技術架構

```
┌─────────────────┐
│   Web Browser   │  ← hermes-hudui (React/Next.js)
└────────┬────────┘
         │ WebSocket
         ↓
┌─────────────────┐
│   Hermes Agent  │
│  ~/.hermes/     │  ← 共享資料目錄
└─────────────────┘
```

---

## 💡 對 Sumo-HUD 的啟發

### 可以借鑒的功能

| Hermes-HUD | Sumo-HUD 實現 |
|-------------|---------------|
| **13 Tab 監控儀表板** | 蘇茉家族控制台 |
| **即時 WebSocket 更新** | 狀態監控 |
| **成本追蹤** | API 使用成本追蹤 |
| **多主題切換** | 視覺化喜好設定 |
| **命令面板** | 快速操作介面 |

### 建議的 Sumo-HUD Tab 設計

| Tab | 內容 |
|-----|------|
| 1. 身份 | 蘇茉家族成員狀態 |
| 2. 記憶 | MemPalace 狀態 |
| 3. 技能 | 各蘇茉技能 |
| 4. 工作階段 | 活躍的 session |
| 5. Cron Jobs | 排程任務狀態 |
| 6. 專案 | 開發中專案 |
| 7. 健康 | 系統健康狀態 |
| 8. 成本 | API 使用成本 |
| 9. 模式 | 使用模式 |
| 10. 修正 | 錯誤修正記錄 |
| 11. 即時聊天 | 與老爺的對話 |

---

## 🚀 安裝方式

```bash
git clone https://github.com/joeynyc/hermes-hudui.git
cd hermes-hudui
./install.sh
hermes-hudui

# 開啟瀏覽器
open http://localhost:3001
```

**需求**：Python 3.11+、Node.js 18+、Hermes agent 運行中

---

## 📁 資料目錄

Hermes-HUD 使用 `~/.hermes/` 作為共享資料目錄：
- identities/
- memory/
- skills/
- sessions/
- cron/
- projects/
- health.json
- costs.json
- patterns/
- corrections/

---

## 🎨 主題

| 主題 | 風格 |
|------|------|
| Neural Awakening | 青色（科技感）|
| Blade Runner | 琥珀（賽博朋克）|
| fsociety | 綠色（駭客風）|
| Anime | 紫色（動漫風）|

---

## 相關連結

- [GitHub](https://github.com/joeynyc/hermes-hudui)
- [Hermes TUI 版本](https://github.com/joeynyc/hermes-hud)
- [Hermes Agent](https://github.com/nousresearch/hermes-agent)

---

*最後更新：2026-04-12*
