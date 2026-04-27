# OpenClaw 實戰：一人、六個 AI Agent 的工程實戰

## 基本資訊

| 項目 | 內容 |
|------|------|
| **來源** | 騰訊新聞（騰訊網）|
| **日期** | 2026-04-10 |
| **作者** | 阿里妹轉載（個人技術實踐）|

---

## 這是什麼？

一個 OpenClaw 用戶分享的**大型 AI Agent 系統架構實戰經驗**，展示了如何用 1 個編排者 + 5 個專業 Agent + 6 個 ACP 編碼專家來實現「AI 替你幹活」。

---

## 🏗️ 系統架構

### 團隊配置

| 角色 | 名稱 | 職責 |
|------|------|------|
| **編排者** | Zoe（大龍蝦）| CTO、任務編排、記憶維護 |
| **情報中樞** | AI 哨兵（ainews）| 100+ 資訊源監控 |
| **量化分析** | 交易蜘蛛（Trading）| 21 個 cron 任務、量化工具 |
| **宏觀經濟** | Macro | 四層映射因子包 |
| **內容策略** | 內容蜘蛛（Content）| 54 平台熱榜追蹤 |
| **生活管家** | 管家蜘蛛（Butler）| Apple 生態整合 |

### 系統規模

| 項目 | 數量 |
|------|------|
| **Cron 任務** | 52 個 |
| **Skills** | 118 個（33 全域 + 85 專屬）|
| **LLM 模型** | 29 個註冊 |
| **每日 LLM 呼叫** | 數千次 |
| **運維腳本** | 2086 行 |
| **自動恢復** | 半個月 23 次 |

---

## ⚠️ 三個核心工程問題

### P0 — 全團隊癱瘓 8 小時

**問題**：ainews 的 session 累積到 235K tokens，Gateway 啟動時做 compaction，session 永遠超時 → crash → 無限重啟迴圈。

**修復**（四層）：
1. 手動清理膨脹 session
2. ThrottleInterval: 1→10
3. idleMinutes: 180→30
4. exec.security: → full→allowlist

### P1 — 3500 字報告被「優化」到 800 字

**問題**：交易蜘蛛的收盤速報包含完整數據表格，但 OpenClaw 的 textChunkLimit 自動做 content compaction，數據表格被「智能壓縮」掉了。

### P2 — 資訊過載後關鍵規則失效

**問題**：SOUL.md 堆滿各種規範後，session 膨脹到幾萬 tokens，Agent 開始「選擇性遵守」規則。

---

## 🛠️ 解決方案：雙層控制

### 第一層 — Context Engineering

| 檔案 | 用途 |
|------|------|
| SOUL.md | 憲法（身份定義、決策框架、絕對禁止項）|
| AGENTS.md | 操作規範和協作協議 |
| Skills | 透過 extraDirs 按需加載 |
| shared-context/ | 跨 Agent 共享狀態 |
| Obsidian Vault | 冷存儲（歸檔產出）|

### 第二層 — Harness（框架自動管理）

| 機制 | 觸發條件 | 動作 |
|------|----------|------|
| **compaction** | session > 40K tokens | 提取精華到 memory/ |
| **contextPruning** | context > 6 小時 | cache-ttl 裁剪 |
| **session reset** | 每天 5:00 或空閒 30 分鐘 | 自動重置 |
| **session maintenance** | 檔案 > 7 天 | 自動清理（磁碟上限 100MB）|

### openclaw.json 配置示例

```json
{
  "compaction": {
    "mode": "safeguard",
    "memoryFlush": {
      "enabled": true,
      "softThresholdTokens": 40000,
      "prompt": "Distill to memory/YYYY-MM-DD.md..."
    }
  },
  "contextPruning": {
    "mode": "cache-ttl",
    "ttl": "6h",
    "keepLastAssistants": 3
  },
  "session": {
    "reset": {
      "mode": "daily",
      "atHour": 5,
      "idleMinutes": 30
    },
    "maintenance": {
      "pruneAfter": "7d",
      "maxDiskBytes": 104857600
    }
  },
  "hooks": {
    "bootstrap": ["self-improving-agent"]
  }
}
```

---

## 🧠 五層記憶系統

| 層 | 儲存 | 時間尺度 | 管理方式 |
|----|------|----------|----------|
| L1 身份層 | SOUL.md | 永恆 | 人工確認修改 |
| L2 長期記憶 | MEMORY.md (<3000 tokens) | 長期 | Agent 自主維護 |
| L3 中期記憶 | .learnings/ | 數天~數週 | 自動積累 |

---

## 💡 對蘇茉家族的啟發

| 項目 | 啟發 |
|------|------|
| **Compaction 閾值** | 我們的 softThresholdTokens 設多少？|
| **Context Pruning** | 我們的 TTL 是多少？|
| **Session Reset** | 我們有設每日重置嗎？|
| **記憶分層** | 我們的記憶系統是否也有層次？|

---

## 標籤

#知識儲備 #OpenClaw實戰 #Agent架構 #ContextEngineering #Harness #記憶系統 #Cron任務優化

---

*記錄者：總管蘇茉*
*時間：2026-04-10 09:13*
