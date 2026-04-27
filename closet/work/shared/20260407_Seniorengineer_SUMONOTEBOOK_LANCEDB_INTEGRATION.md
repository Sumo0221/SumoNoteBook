# SumoNoteBook + memory-lancedb-pro 整合記錄

> 本檔案記錄蘇茉家族記憶系統的所有變更與實作。

---

## 📅 更新日誌

### 2026-04-06 - P0 第一階段完成

#### 新增檔案

| 檔案 | 位置 | 說明 |
|------|------|------|
| MEMORY_INDEX.md | `~/.sumo/memory/MEMORY_INDEX.md` | 蘇茉家族記憶索引，借鑒 Claude Code MEMORY.md 設計 |
| CLAUDE_DESIGN.md | `workspace_senior_engineer/CLAUDE_DESIGN.md` | 統一的多層級指令體系（L1-L4） |

#### 更新檔案

| 檔案 | 變更內容 |
|------|----------|
| HEARTBEAT.md | 新增 session_snapshot 增強功能，包括自動摘要、決策擷取、記憶晉升 |

---

## 🎯 P0 任務完成狀態

### ✅ 1. MEMORY.md 索引機制

**實作內容**：
- 建立 `~/.sumo/memory/MEMORY_INDEX.md`
- 前 200 行濃縮索引（蘇茉家族結構、專長領域、共享資源、案例）
- Topic 檔案索引（preferences/decisions/cases/commands/security）
- 每條記憶指向詳細的 topic 檔案或概念筆記

**對應 Claude Code 元件**：MEMORY.md（L2 長期記憶索引）

**設計原則**：
- 借鑒 Claude Code 的 200 行上限設計
- INDEX 作為入口，詳細內容在 topic 檔案
- 支援快速啟動上下文加载

---

### ✅ 2. 統一多層級指令體系

**實作內容**：
- 建立 `CLAUDE_DESIGN.md` 整合 AGENTS.md + SOUL.md + USER.md
- 四層架構：
  - L1 企業層級（張家使命、蘇茉家族規則）
  - L2 用戶層級（老爺偏好、特殊指令）
  - L3 專案層級（工作區定義、專業領域）
  - L4 本地層級（Session 快照、臨時狀態）

**對應 Claude Code 元件**：CLAUDE.md 多層級體系

**整合內容**：
- Workspace 隔離原則
- Cron 路由規範
- 知識管理整合（SumoNoteBook + memory-lancedb-pro + MEMORY_INDEX）

---

### ✅ 3. sessionMemory 增強

**實作內容**：
- 更新 `HEARTBEAT.md` 新增 session_snapshot 功能
- 自動摘要觸發時機（對話結束、任務完成、30分鐘無回應）
- Session 快照寫入位置（sessions/YYYY-MM-DD.md + memory-lancedb-pro）
- 記憶標記格式（@memory category="..." content="..."）

**對應 Claude Code 元件**：Session Memory（L3 工作記憶）

**增強功能**：
- 自動摘要生成
- 決策智慧擷取
- 重要資訊自動晉升至 long-term memory
- 快速恢復上下文

---

## 📊 與 Claude Code 對照表（更新）

| Claude Code 元件 | 蘇茉家族實作 | 狀態 |
|-----------------|-------------|------|
| MEMORY.md | MEMORY_INDEX.md | ✅ 已實作 |
| CLAUDE.md 多層 | CLAUDE_DESIGN.md | ✅ 已實作 |
| Session Memory | HEARTBEAT.md (session_snapshot) | ✅ 已實作 |
| Auto Memory (topic) | Sumo_wiki/concepts/ | ✅ 既有 |
| AutoDream | （待實作 P1） | ⏳ 規劃中 |
| LCM (compact/resume) | OpenClaw LCM | ✅ 既有 |
| Per-agent scope | memory-lancedb-pro scope | ✅ 既有 |

---

## 🔄 P1/P2 任務規劃

### P1 - 短期（1 個月）

- [x] Topic 檔案雙寫機制（memory → Markdown + LanceDB） ✅ 研究完成
- [x] 終端焦點感知（FOCUS-AWARE）實作方案 ✅ 研究完成
- [ ] AutoDream CRON job 概念驗證
- [ ] 每個蘇茉獨立 scope（agent:<id>）

### P2 - 中期（1-2 個月）

- [ ] Session 摘要雙寫（ LanceDB + 日記檔）
- [ ] 借鑒「終端焦點感知」調整蘇茉響應策略（待 P1-2 實作後整合）
- [ ] KAIROS 概念研究

---

## 📅 更新日誌

### 2026-04-06 - P1 第二階段完成 ✅

#### 已完成輸出

| 檔案 | 位置 | 說明 |
|------|------|------|
| topic-dual-writer.ts | `plugins/memory-lancedb-pro/src/topic-dual-writer.ts` | 雙寫核心模組（新建） |
| focus-tracker.ts | `plugins/memory-lancedb-pro/src/focus-tracker.ts` | 終端焦點追蹤模組（新建） |
| Topic 目錄結構 | `~/.sumo/memory/topics/` | 8 個 category 目錄已建立 |
| Topic INDEX 檔 | `~/.sumo/memory/topics/{category}/0000_INDEX.md` | 每個 category 的索引檔 |

#### 1. Topic 檔案自動雙寫（LanceDB + Markdown）✅

**實作狀態**：研究完成，核心模組已建立

**實作方案**：

**A. 架構設計**

```
memory-lancedb-pro store() 调用
        │
        ▼
┌───────────────────────────────┐
│   TopicDualWriter Module      │
│   (新建：topic-dual-writer.ts) │
└───────────────┬───────────────┘
                │
        ┌───────┴───────┐
        ▼               ▼
┌──────────────┐  ┌────────────────────────┐
│  LanceDB     │  │  Markdown Topic 檔案    │
│  (主要儲存)  │  │  ~/.sumo/memory/topics/│
└──────────────┘  └────────────────────────┘
```

**B. Topic 檔案結構**

| Category | 路徑 | 格式 |
|----------|------|------|
| preference | `~/.sumo/memory/topics/preferences/{id}.md` | YAML frontmatter + 內容 |
| decision | `~/.sumo/memory/topics/decisions/{id}.md` | YAML frontmatter + 內容 |
| case | `~/.sumo/memory/topics/cases/{id}.md` | YAML frontmatter + 內容 |
| command | `~/.sumo/memory/topics/commands/{id}.md` | YAML frontmatter + 內容 |
| fact | `~/.sumo/memory/topics/facts/{id}.md` | YAML frontmatter + 內容 |

**C. Topic 檔案格式（Frontmatter）**

```yaml
---
id: {uuid}
name: {自動生成標題}
description: {一句話描述}
type: {category}          # preference|decision|case|command|fact
scope: {scope}            # global|agent:xxx|owner:xxx
importance: {0.0-1.0}
created: {ISO timestamp}
updated: {ISO timestamp}
tags: [tag1, tag2]
---

## 內容
{完整的 memory text}
```

**D. 雙寫流程**

```
寫入流程（store/update/delete）：
1. 取得 file lock（防止並發衝突）
2. 寫入 LanceDB
3. 寫入對應 Markdown topic 檔案
4. 更新 MEMORY_INDEX.md 索引（如有必要）
5. 釋放 file lock

原則：
- LanceDB 是主要資料來源（semantic recall）
- Markdown 是人類可讀日誌
- 寫入失敗時，LanceDB 成功視為最終成功，Markdown 非同步重試
```

**E. 實作位置**

```
C:\Users\rayray\.openclaw\plugins\memory-lancedb-pro\src\topic-dual-writer.ts  (新建)
C:\Users\rayray\.openclaw\plugins\memory-lancedb-pro\src\store.ts              (修改：整合 dual-writer)
C:\Users\rayray\.openclaw\.sumo\memory\topics\                                 (新建：topic 檔案根目錄)
```

**F. 雙向同步策略**

Markdown → LanceDB：
- 透過 SumoNoteBook 的 `daily_organizer.py` INGEST 流程
- INGEST 完成後自動呼叫 memory-lancedb-pro 的 importEntry()
- 使用相同的 id 確保一致性

LanceDB → Markdown：
- 在 store/update/delete 時同步寫入
- 使用 uuid 作為檔名（方便交叉引用）

**G. 待建立的核心 Topic 檔案**

基於 MEMORY_INDEX.md 中定義的 Topic 索引，應建立：

| Topic | 位置 | 內容 |
|-------|------|------|
| preferences.md | topics/preferences/index.md | 老爺的個人偏好索引 |
| decisions.md | topics/decisions/index.md | 重要架構/技術決策索引 |
| cases.md | topics/cases/index.md | 成功案例和模式索引 |
| commands.md | topics/commands/index.md | 蘇茉家族指令體系索引 |
| security.md | topics/security.md | 安全規則和敏感資訊 |

---

#### 2. 終端焦點感知（FOCUS-AWARE 響應策略）✅

**實作狀態**：研究完成，核心模組已建立

**實作方案**：

**目標**：讓蘇茉能感知用戶的焦點狀態，調整回應頻率和深度。

**A. 概念來源**

借鑒 Claude Code 的 KAIROS 系統：
- KAIROS 是隱藏的 24/7 持續運行代理模式
- 感知用戶的「忙碌程度」來調整 AI 的主動程度
- 在背景運行，不打擾用戶工作流程

**B. 終端狀態分級**

| 等級 | 名稱 | 觸發條件 | 蘇茉行為 |
|------|------|----------|----------|
| FOCUS_HIGH | 🎯 深度專注 | 用戶在終端活跃輸入、視窗聚焦 | 只回應明確請求，零主動通知 |
| FOCUS_MEDIUM | 📊 一般專注 | 有段時間無輸入但終端仍在前台 | 選擇性回應，減少主動打擾 |
| FOCUS_LOW | ☕ 閒置/休息 | 終端最小化、鍵盤長時間無輸入 | 適度主動互動，提供建議 |
| FOCUS_AWAY | 🚶 離開 | 系統idle很長一段時間 | 可主動發送重要通知 |
| FOCUS_IDLE | 😴 深度閒置 | 數小時無任何活動 | 不主動互動，等待喚醒 |

**C. 實作方向**

**信號來源**（按可靠性排序）：
1. **systemEvent 事件**：OpenClaw 的 systemEvent 提供 session 狀態
2. **HEARTBEAT.md 狀態**：現有的心跳檔案可擴展
3. **時間模式**：根據時間段推斷（工作時間/休息時間）
4. **memory-lancedb-pro access tracker**：記錄記憶存取模式

**D. 實作架構**

```
┌─────────────────────────────────────────┐
│        FocusTracker Module              │
│   (新建：focus-tracker.ts)              │
└────────────────┬──────────────────────┘
                 │
    ┌────────────┼────────────┐
    ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│ system  │ │HEARTBEAT│ │ Time    │
│ Event   │ │  .md    │ │ Pattern │
└────┬────┘ └────┬────┘ └────┬────┘
     │           │           │
     └───────────┴───────────┘
                 │
                 ▼
        ┌───────────────┐
        │ FocusLevel    │
        │  Calculator  │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │ Response      │
        │ Strategy      │
        │ Controller    │
        └───────────────┘
```

**E. 關鍵實作點**

1. **FocusTracker 類**：
   - `getCurrentFocusLevel()`: 返回目前的專注等級
   - `recordActivity()`: 記錄用戶活動
   - `onFocusChange(callback)`: 等級變化時通知

2. **與蘇茉響應的整合**：
   - 在 HEARTBEAT.md 中增加 focus_level 欄位
   - 蘇茉主動行為前檢查 focus_level
   - 等級 HIGH 時跳過所有主動通知

3. **適配 OpenClaw**：
   - 利用 systemEvent 中的狀態事件
   - 透過 session_status 查詢 session 狀態
   - 不需要額外的系統監控（尊重隱私）

**F. 實作位置**

```
C:\Users\rayray\.openclaw\plugins\memory-lancedb-pro\src\focus-tracker.ts  (新建)
C:\Users\rayray\.openclaw\workspace_senior_engineer\HEARTBEAT.md           (更新：增加 focus_level)
```

**G. 隱私考量**

- 不監控鍵盤輸入內容
- 不監控視窗標題或 URL
- 只關心「有/無活動」的狀態信號
- 用戶可通過關閉 focus tracking 來停用此功能

---

#### 3. 實作優先順序

| 優先順序 | 任務 | 預計工時 | 風險 |
|----------|------|----------|------|
| P1-1 | TopicDualWriter 核心模組 | 1-2 天 | 低 |
| P1-2 | Topic 檔案結構建立 | 0.5 天 | 低 |
| P1-3 | FocusTracker 核心模組 | 1 天 | 低 |
| P1-4 | HEARTBEAT focus_level 整合 | 0.5 天 | 低 |
| P1-5 | 雙向同步測試驗證 | 1 天 | 中 |
| P1-6 | End-to-end 整合測試 | 1 天 | 中 |

---

#### 4. 輸出檔案變更

| 檔案 | 變更類型 | 說明 |
|------|----------|------|
| `topic-dual-writer.ts` | 新建 | 雙寫核心模組 |
| `focus-tracker.ts` | 新建 | 終端焦點追蹤模組 |
| `~/.sumo/memory/topics/` | 新建 | Topic 檔案根目錄（8 個 category） |
| `MEMORY_INDEX.md` | 更新 | P1 完成狀態、Topic 目錄更新 |
| `SUMONOTEBOOK_LANCEDB_INTEGRATION.md` | 更新 | P1 研究與實作方案 |

---

## 📚 相關檔案

| 檔案 | 位置 | 用途 |
|------|------|------|
| MEMORY_INDEX.md | `~/.sumo/memory/MEMORY_INDEX.md` | 家族記憶索引 |
| CLAUDE_DESIGN.md | `workspace_senior_engineer/CLAUDE_DESIGN.md` | 多層級指令體系 |
| HEARTBEAT.md | `workspace_senior_engineer/HEARTBEAT.md` | Session 快照 |
| SOUL.md | `workspace_senior_engineer/SOUL.md` | 高工蘇茉身份 |
| AGENTS.md | `workspace_senior_engineer/AGENTS.md` | 工作區定義 |
| USER.md | `workspace_senior_engineer/USER.md` | 用戶偏好 |
| claude_code_memory_research.md | `workspace_senior_engineer/claude_code_memory_research.md` | 研究報告 |

---

## 🗂️ SumoNoteBook 結構（更新）

```
C:\butler_sumo\library\SumoNoteBook\
├── Sumo_wiki/
│   ├── SOUL.md              # SumoNoteBook 靈魂準則
│   ├── index.md             # 總索引
│   ├── log.md               # 活動日誌
│   ├── concepts/            # 概念筆記（topic 檔案）
│   │   ├── preferences.md  # 老爺偏好
│   │   ├── decisions.md     # 重要決策
│   │   ├── cases.md        # 成功案例
│   │   ├── commands.md      # 蘇茉指令
│   │   └── security.md     # 安全規則
│   ├── summaries/          # 摘要
│   ├── backlinks/          # 反向連結
│   ├── qa/                 # 問答記錄
│   └── daily/              # 每日筆記
├── raw/                     # 原始資料
└── scripts/                # 腳本
```

---

---

## P2 任務完成（2026-04-06）

### 1. AutoDream CRON Job（記憶整理）概念驗證 ✅

**實作狀態**：概念驗證完成，核心模組已建立

**觸發條件（Triple Gate）**：

| 條件 | 閾值 | 說明 |
|------|------|------|
| 時間閘 | ≥ 24 小時 | 距離上次執行 |
| Session 閘 | ≥ 5 sessions | 累計 session 數 |
| Lock 檔案 | 不存在或已過期 | 防並發執行 |

**實作架構**：

```
┌─────────────────────────────────────────────────────────┐
│                   AutoDream Engine                       │
│            (auto-dream.ts, 新建)                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Triple Gate Check                                      │
│  ├── 時間閘：上次執行 ≥ 24h                              │
│  ├── Session 閘：累計 ≥ 5 sessions                      │
│  └── Lock 檔案：防並發                                   │
│           │                                             │
│           ▼                                             │
│  ┌─────────────────┐                                    │
│  │  Step 1: Scan   │  掃描 MEMORY_INDEX 中的孤立 topic  │
│  └────────┬────────┘                                    │
│           ▼                                              │
│  ┌─────────────────┐                                    │
│  │  Step 2: Cluster│  合併相似 topic（cosine + Jaccard） │
│  └────────┬────────┘                                    │
│           ▼                                              │
│  ┌─────────────────┐                                    │
│  │  Step 3: Delete │  刪除過時或矛盾記憶                 │
│  └────────┬────────┘                                    │
│           ▼                                              │
│  ┌─────────────────┐                                    │
│  │ Step 4: Update  │  更新 MEMORY_INDEX.md              │
│  └─────────────────┘                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**A. 核心功能**

| 功能 | 演算法 | 閾值 |
|------|--------|------|
| 相似 Topic 合併 | Cosine Similarity + Jaccard Overlap | ≥ 0.88 / ≥ 0.50 |
| 孤立 Topic 檢測 | 比對 LanceDB ID vs Topic 檔案 | 無對應則歸檔 |
| 過時記憶刪除 | 時間衰減 + 低重要性 | > 90 天且 importance < 0.3 |
| 記憶去重 | Greedy Clustering | 2+ 相似記憶合併 |

**B. State 持久化**

```typescript
interface AutoDreamState {
  lastRunTime: number;       // Unix timestamp ms
  sessionCount: number;      // Sessions since last run
  lastRunResult: string;      // "success" | "skipped" | "failed"
  memoriesScanned: number;
  memoriesMerged: number;
  memoriesDeleted: number;
  errors: string[];
}
```

**C. CRON 排程**

- 預設排程：`0 3 * * *`（每日凌晨 3:00 AM）
- 每分鐘檢查一次（60 秒 interval）
- 每日最多執行一次（防重複）

**D. 與 HEARTBEAT.md 整合**

```typescript
// 在 HEARTBEAT.md 中顯示
## AutoDream Status

Enabled: Yes
Last Run: 2026-04-06T03:00:00.000Z
Last Result: success
Sessions Since Last Run: 0
Memories Scanned: 42
Memories Merged: 3
Memories Deleted: 7

Next Run: After 5 more sessions or 24h
```

**E. 實作位置**

```
C:\Users\rayray\.openclaw\plugins\memory-lancedb-pro\src\auto-dream.ts  (新建)
```

**F. 關鍵 API**

```typescript
// 取得全域引擎
const engine = getDreamEngine(config);

// 記錄 session（每次新 session 開始時呼叫）
engine.recordSession();

// 檢查是否應該觸發
const { triggered, reason } = engine.shouldTrigger();

// 手動執行
const result = await engine.run();

// CRON 模式
startDreamCron(engine, "0 3 * * *");  // 每日凌晨 3:00
stopDreamCron();
```

---

### 2. 每個蘇茉獨立 Agent Scope 隔離 ✅

**實作狀態**：概念驗證完成，現有架構足以支援

**現有Scope 機制分析**：

memory-lancedb-pro 的 `scopes.ts` 已經具備完善的 scope 隔離機制：

```typescript
// 內建的 Scope Patterns
const SCOPE_PATTERNS = {
  GLOBAL: "global",
  AGENT: (agentId: string) => `agent:${agentId}`,
  CUSTOM: (name: string) => `custom:${name}`,
  REFLECTION: (agentId: string) => `reflection:agent:${agentId}`,
  PROJECT: (projectId: string) => `project:${projectId}`,
  USER: (userId: string) => `user:${userId}`,
};
```

**A. 蘇茉家族的 Scope 對應**

| 蘇茉代號 | Scope Pattern | 說明 |
|----------|---------------|------|
| main | `agent:main` | 總管蘇茉私人記憶 |
| engineer | `agent:engineer` | 工程師蘇茉私人記憶 |
| senior_engineer | `agent:senior_engineer` | 高工蘇茉私人記憶 |
| professor | `agent:professor` | 教授蘇茉私人記憶 |
| hacker | `agent:hacker` | 駭客蘇茉私人記憶 |
| global | `global` | 共享知識（所有蘇茉可讀） |
| shared | `custom:shared` | 團隊共享 topic |
| owner | `owner:francis` | 老爺私人資訊 |

**B. Scope 隔離策略**

```
┌──────────────────────────────────────────────────────────────┐
│                     Scope 隔離架構                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  memory_recall() 查詢流程：                                   │
│                                                              │
│  1. 從 session key 解析 agentId（如 "agent:senior_engineer"）  │
│  2. 呼叫 scopeManager.getScopeFilter(agentId)                │
│  3. 返回允許的 scopes: ["global", "agent:senior_engineer"]   │
│  4. LanceDB 只返回符合 scope 的記憶                           │
│                                                              │
│  memory_store() 寫入流程：                                    │
│                                                              │
│  1. 預設寫入 scope = agent:${agentId}                        │
│  2. 可明確指定 custom scope（如 shared）                       │
│  3. 敏感資訊嚴格隔離（API keys 只在 owner scope）             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**C. 權限矩陣**

| Scope | main | engineer | senior | professor | hacker | global |
|-------|------|----------|--------|----------|--------|--------|
| global | RW | RW | RW | RW | RW | RW |
| agent:main | RW | - | - | - | - | - |
| agent:engineer | - | RW | - | - | - | - |
| agent:senior_engineer | - | - | RW | - | - | - |
| agent:professor | - | - | - | RW | - | - |
| agent:hacker | - | - | - | - | RW | - |
| custom:shared | RW | RW | RW | RW | RW | - |
| owner:francis | R | - | - | - | - | - |

- **RW** = 讀寫
- **R** = 唯讀（老爺資訊蘇茉只能讀取）
- **-** = 無法存取

**D. SumoNoteBook 的 Shared Topics**

共享資訊透過 SumoNoteBook 的 `shared/` 目錄：

```
C:\butler_sumo\library\SumoNoteBook\
└── Sumo_wiki/
    └── shared/
        ├── index.md              # 共享索引
        ├── family_rules.md       # 張家通用規則
        ├── calendar.md           # 共享行事曆
        └── resources.md          # 共享資源
```

每個蘇茉的 workspace 只看到自己的 `concepts/`、`summaries/`、`daily/`，
但可以讀取 `shared/` 的內容。

**E. 安全敏感資訊隔離**

```
~/.sumo/memory/
├── MEMORY_INDEX.md              # 家族記憶索引（所有蘇茉可讀）
├── .autodream.lock             # AutoDream 鎖檔
├── .autodream.state            # AutoDream 狀態
├── topics/                      # Topic 檔案（按 scope 分類）
│   ├── global/                 # 全球共享 topic
│   ├── agent:senior_engineer/  # 高工蘇茉私人 topic
│   ├── agent:engineer/         # 工程師蘇茉私人 topic
│   ├── custom:shared/          # 團隊共享 topic
│   └── owner:francis/          # 老爺私人資訊（API keys 等）
└── security/
    └── api_keys.md             # API Keys（嚴格隔離）
```

**F. 實作細節**

ClawTeam 的 `clawteam-scope.ts` 已經整合了 `CLAWTEAM_MEMORY_SCOPE` 環境變數：

```typescript
// 解析 CLAWTEAM_MEMORY_SCOPE 環境變數
export function parseClawteamScopes(envValue: string | undefined): string[] {
  if (!envValue) return [];
  return envValue.split(",").map(s => s.trim()).filter(Boolean);
}

// 擴展 ScopeManager 的 accessible scopes
export function applyClawteamScopes(
  scopeManager: MemoryScopeManager,
  scopes: string[],
): void {
  // 1. 註冊未知的 scope
  // 2. 包裝 getAccessibleScopes() 加入額外 scopes
}
```

**G. 驗證方式**

```bash
# 測試 scope 隔離
openclaw memory recall --query "API key" --agent senior_engineer
# 預期：無法取得 owner:francis 的 API keys

openclaw memory recall --query "API key" --agent main
# 預期：可以讀取但不應該寫入
```

---

### 3. 實作優先順序（P2）

| 優先順序 | 任務 | 預計工時 | 風險 |
|----------|------|----------|------|
| P2-1 | AutoDream Engine 整合進 plugin | 1 天 | 低 |
| P2-2 | AutoDream CRON 排程實作 | 0.5 天 | 低 |
| P2-3 | Scope 隔離測試驗證 | 1 天 | 中 |
| P2-4 | Shared Topics 目錄建立 | 0.5 天 | 低 |
| P2-5 | End-to-end 整合測試 | 1 天 | 中 |

---

### 4. 輸出檔案變更（P2）

| 檔案 | 變更類型 | 說明 |
|------|----------|------|
| `auto-dream.ts` | 新建 | AutoDream 核心模組 |
| `SUMONOTEBOOK_LANCEDB_INTEGRATION.md` | 更新 | P2 設計與實作方案 |
| `MEMORY_INDEX.md` | 更新 | 新增 AutoDream Status 章節 |

---

### 5. 下一步行動

1. **P2-1**: 將 `auto-dream.ts` 整合進 memory-lancedb-pro plugin
2. **P2-2**: 實作 CRON job 排程（在 OpenClaw gateway 啟動時注册）
3. **P2-3**: 驗證 scope 隔離（用 `memory_recall --agent xxx` 測試）
4. **P2-4**: 在 SumoNoteBook 建立 `shared/` 目錄結構
5. **P3 規劃**: 
   - Session 摘要雙寫（ LanceDB + 日記檔）
   - KAIROS 概念研究（終端焦點感知進階）

---

*本檔案由高工蘇茉維護*
*版本：1.1 | 更新：2026-04-06（P2 完成）*
