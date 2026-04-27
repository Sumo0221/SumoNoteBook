# Claude Code 記憶機制深度研究報告

**研究日期**：2026-04-06  
**研究者**：高工蘇茉（SeniorEngineerSuMo）  
**參考來源**：YouTube 影片 + Claude Code 官方文件 + 多方技術分析

---

## 一、Claude Code 六維記憶體系分析

### 1.1 四層記憶架構總覽

Claude Code 的記憶系統並非單一功能，而是一套**分層的持久化上下文系統**，模仿人類認知架構：

| 層次 | 名稱 | 誰寫入 | 儲存位置 | 生命週期 | 加載時機 |
|------|------|--------|----------|----------|----------|
| **L1** | CLAUDE.md（指令記憶） | 開發者 | 專案根目錄 / ~/.claude/ | 永久（隨 Git） | 每次對話開始 |
| **L2** | Auto Memory（長期記憶） | Claude 自動 | ~/.claude/projects/*/memory/ | 永久（跨 session） | MEMORY.md 前 200 行啟動載入，topic 檔案按需讀取 |
| **L3** | Session Memory（工作記憶） | Claude 自動 | 本地對話記錄 | 單次 session（可 resume） | 對話過程 / resume 時注入 |
| **L4** | AutoDream（記憶整理） | Claude 子代理 | 修改 L2 檔案 | 週期性（約 24h / 5+ sessions） | 後台運行，無需手動觸發 |

> 影片標題的「六維」可能包括：指令記憶、長期記憶、Session Memory、AutoDream，加上隱藏的 KAIROS 主動監控系統（共 5 維），以及對話歷史管理（compact/resume/task）。

---

### 1.2 L1 — 指令記憶 (Instruction Memory)

**核心檔案**：`CLAUDE.md`（多層級）

#### 多層級體系

| 範圍 | 路徑 | 用途 |
|------|------|------|
| 企業級 | `/etc/claude-code/CLAUDE.md`（Mac/Linux）或 `C:\Program Files\ClaudeCode\CLAUDE.md`（Win） | 公司程式規範、安全策略 |
| 用戶級 | `~/.claude/CLAUDE.md` | 個人偏好（全專案通用） |
| 專案級 | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 團隊共享指令（進版控制） |
| 本地級 | `./CLAUDE.local.md` | 個人專案偏好（gitignore） |
| 子目錄級 | `./.claude/rules/*.md` | 特定模組的規則 |

**載入順序**（由低到高）：Managed → User → Project → Local  
**設計原則**：越具體的規則優先權越高，衝突時高優先級覆蓋低優先級。

**內容分類**：

✅ **適合寫入 CLAUDE.md**：
- 專案架構概覽（技術棧、目錄結構）
- 編碼規範（命名、測試模式）
- 部署流程（命令、環境變數）
- 資料庫結構（表名、欄位說明）
- 不可違反的硬規則（如「禁止修改 docs/human/ 目錄」）

❌ **不適合寫入 CLAUDE.md**：
- 臨時狀態資訊（應放 Auto Memory）
- 個人偏好（應放 ~/.claude/CLAUDE.md 或 memory）
- 過於頻繁變化的資料
- 環境變數的值（安全風險）
- 大段程式碼

**關鍵設計**：`@include` 指令 — 支援檔案引用，可將大型規則集拆分到多個檔案。

---

### 1.3 L2 — 長期記憶 (Auto Memory)

**核心機制**：Claude 自己寫給未來自己的筆記。當用戶糾正錯誤、表達偏好、或做出重要決策時，Claude 自動判斷是否值得記住。

#### 儲存結構

```
~/.claude/projects/<project-path-hash>/memory/
├── MEMORY.md          # 索引檔（前 200 行啟動載入）
├── daily-workflow.md  # 按主題組織的 topic 檔案
├── video-rules.md
├── pro-business-status.md
└── ... (20+ topic 檔案)
```

#### Frontmatter 格式

每個 topic 檔案以 YAML frontmatter 開頭：

```yaml
---
name: video-first-frame-rule
description: 視頻首幀必須是完整封面，不能有任何 fade-in
type: feedback
---
```

#### 五種記憶類型

| 類型 | 說明 | 例子 |
|------|------|------|
| 👤 user | 用戶個人偏好和習慣，跨專案通用 | 用戶偏好 TypeScript strict mode |
| 💬 feedback | 用戶糾正後的經驗教訓 | 視頻首幀不能有 fade-in |
| 📁 project | 專案級狀態和決策 | Pro 會員 20 人/週，需增長策略 |
| 📚 reference | 技術文件和服務配置清單 | 12 個外部服務的環境變數清單 |
| ❌ code（已廢棄） | 早期用於存程式碼片段，現不推薦 | — |

#### MEMORY.md 索引設計（200 行上限）

Claude Code 啟動時只載入 MEMORY.md 前 200 行（或 25KB，取較小值）。這意味著：
- MEMORY.md 職責是「索引」而非「儲存」
- 每條都是一行索引 + 簡短描述，指向詳細的 topic 檔案
- 超過 200 行時，Claude 會收到警告並被要求將內容拆分到 topic 檔案

#### 觸發時機

Claude 並非每個 session 都寫 memory，基於以下信號：
- 用戶糾正錯誤（「不對，應該是...」）
- 明確偏好（「以后都用...」）
- 反覆出現的主題
- 重要的架構決策

---

### 1.4 L3 — Session Memory（工作記憶）

**用途**：維持對話上下文，記錄當前任務的臨時狀態。

**特點**：
- 單次 session 生命週期
- 支援 `--continue` / `--resume` 恢復
- 可注入啟動上下文

---

### 1.5 L4 — AutoDream（記憶整理）

**核心概念**：如果 KAIROS 是 Claude Code 的清醒狀態，AutoDream 就是它的睡眠週期。

#### 觸發條件（三重門）：
1. 距離上次執行 ≥ 24 小時
2. 累計 ≥ 5 個 session
3. 鎖檔案存在（防並發）

#### 行為描述

從洩漏的 system prompt 中可見：

> *"You are performing a dream — a reflective pass over your memory files. Synthesize what you've learned recently into durable, well-organized memories so that future sessions can orient quickly."*

AutoDream 的功能：
1. **去重**：合併重複的記憶條目
2. **時間歸一化**：整理時間戳
3. **記憶合併**：將多個相關記憶合併為結構化條目
4. **組織整理**：確保未來 session 能快速定位

#### 與 KAIROS 的關係

KAIROS 是隱藏的 24/7 持續運行代理模式，AutoDream 是其「睡眠時的記憶整理」功能。兩者都被包裝在 feature flag 後（`tengu_onyx_plover`），預設關閉。

---

## 二、對照我們的系統

### 2.1 蘇茉家族現有記憶架構

```
┌─────────────────────────────────────────────────────────┐
│                    蘇茉家族記憶架構                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌──────────────┐    ┌───────────┐  │
│  │  SumoNoteBook│    │memory-lancedb│    │  AGENTS  │  │
│  │ （知識庫）   │    │    -pro     │    │  .md     │  │
│  │             │    │  (向量資料庫) │    │          │  │
│  │ raw/        │    │              │    │ SOUL.md  │  │
│  │ Sumo_wiki/  │    │ Auto-capture │    │ AGENTS.md│  │
│  │ scripts/    │    │ Auto-recall  │    │ USER.md  │  │
│  └─────────────┘    │ smartExtract │    └───────────┘  │
│                     │ Weibull衰減  │                   │
│                     │ 三層晉升     │                   │
│                     └──────────────┘                   │
│                                                         │
│  ┌──────────────────────────────────────────────┐      │
│  │              OpenClaw LCM                    │      │
│  │         (對話歷史壓縮管理)                    │      │
│  │   lcm_expand / lcm_grep / lcm_describe       │      │
│  └──────────────────────────────────────────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 各元件對應關係

| Claude Code 元件 | 我們的對應元件 | 說明 |
|-----------------|--------------|------|
| CLAUDE.md（指令） | AGENTS.md + SOUL.md + USER.md | 定義各蘇茉的身份、行為、服務對象 |
| Auto Memory（長期記憶） | memory-lancedb-pro（向量資料庫） | 跨 session 持久記憶，支援 semantic recall |
| MEMORY.md（索引） | 目前無直接對應 | — |
| Session Memory | LCM 對話歷史 | OpenClaw 原生的對話壓縮管理 |
| AutoDream（記憶整理） | 目前無對應 | — |
| topic 檔案（按主題組織） | concepts/ + qa/ + summaries/ | Sumo_wiki 下的分類資料夾 |
| `.claude/rules/*.md` | 目前無對應 | — |

### 2.3 SumoNoteBook 的定位

**SumoNoteBook**（`C:\butler_sumo\library\SumoNoteBook\`）是一套**以文件為中心的知識管理系統**：

```
Sumo_wiki/
├── index.md          # 總目錄
├── health_report.md  # 健康檢查報告
├── concepts/         # 概念筆記（相當於 topic 檔案）
├── summaries/        # 摘要（相當於 Claude 的壓縮記憶）
├── backlinks/        # 反向連結
├── templates/        # 模板系統
├── daily/            # 每日筆記
└── qa/               # 問答記錄
```

**相當於 Claude Code 的什麼？**

- `summaries/` ≒ Auto Memory 的 topic 檔案
- `concepts/` ≒ 概念化的記憶索引
- `daily/` ≒ 日記式的 Session Memory
- `raw/` ≒ 原始資料輸入

**但關鍵差異**：
- Claude Code 的 Auto Memory 是**主動寫入**（Claude 自動總結）
- SumoNoteBook 的 summaries/ 是**被動整理**（每日腳本處理）

### 2.4 memory-lancedb-pro 的能力

當前已具備：
- ✅ 混合檢索（向量 + BM25）
- ✅ 交叉編碼器重排序
- ✅ Smart Extraction（6 類 LLM 分類）
- ✅ Weibull 衰減 + 三層晉升
- ✅ Auto-capture + auto-recall
- ✅ 多 scope 隔離
- ✅ 噪音過濾
- ❌ **無 MEMORY.md 索引機制**
- ❌ **無 AutoDream 自動整理**
- ❌ **無 topic 檔案按需載入**

---

## 三、改進建議

### 3.1 借鑒 Claude Code 的設計原則

1. **分層而非單一**：記憶應按生命週期和用途分層
2. **索引與內容分離**：MEMORY.md 作為索引，詳細內容在 topic 檔案
3. **200 行上限**：防止索引膨脹，強制拆分
4. **Claude 自動寫入**：而非只依賴用戶手動記錄
5. **週期性整理**：後台自動整理、去重、合併

### 3.2 可以實作的功能（附優先順序）

#### P0 — 立即實作（1-2 週）

**1. 建立 MEMORY.md 索引機制**

```
對應：Claude Code 的 MEMORY.md
現況：memory-lancedb-pro 無索引概念
做法：
- 在 workspace 目錄建立 .sumo/memory/MEMORY.md
- 作為向量記憶的「人類可讀索引」
- 前 200 行為啟動時讀取的濃縮摘要
- 向量記憶仍是主要 semantic recall 來源
```

**2. Topic 檔案自動分類**

```
對應：Claude Code 的 ~/.claude/projects/*/memory/*.md
現況：Sumo_wiki 有手動分類，但非自動生成
做法：
- 當 memory-lancedb-pro 存储新記憶時
- 自動生成對應的 topic 檔案（如 preferences.md, decisions.md）
- 格式模仿 Claude 的 frontmatter 結構
```

#### P1 — 短期實作（1 個月）

**3. 雙寫機制（Dual-write）**

```
現況：memory-lancedb-pro 和 SumoNoteBook 是獨立的兩套系統
問題：事實寫入 memory/YYYY-MM-DD.md，但 memory_recall 找不到
做法：
- memory_store 時同時寫入 LanceDB + Markdown 檔案
- Markdown 檔案作為「人類可讀日誌」
- LanceDB 作為「機器可讀 semantic recall」
```

**4. 指令記憶增強**

```
對應：CLAUDE.md 多層級體系
現況：AGENTS.md / SOUL.md / USER.md 分散
做法：
- 建立統一的「蘇茉家族指令體系」
  - ~/.sumo/CLAUDE.md（全家通用規則）
  - ~/.sumo/agents/CLAUDE_main.md / CLAUDE_engineer.md（各蘇茉專屬）
  - ./CLAUDE.md（工作區專案指令）
- 實作類似 @include 的檔案引用語法
```

#### P2 — 中期實作（1-2 個月）

**5. AutoDream 自動整理（概念驗證）**

```
對應：AutoDream 記憶整理
現況：無自動整理機制
做法：
- 設計一個 CRON job（每 24h / 5+ sessions）
- 掃描 memory-lancedb-pro 中的記憶
- 自動去重、合併、分類
- 更新 MEMORY.md 索引
```

**6. Session Memory 增強**

```
對應：Claude 的 Session Memory + compact/resume
現況：依賴 OpenClaw LCM
做法：
- 在 /new 對話時自動總結上一個 session
- 將摘要同時寫入 LanceDB（重要 decision/fact）+ 日記檔案
- 支援 --resume 恢復豐富的上下文
```

**7. Subagent 獨立記憶**

```
對應：Claude Code 的 subagent persistent memory
現況：每個蘇茉有獨立 workspace，但共享同一個 LanceDB scope
做法：
- 每個蘇茉（agent）有獨立的 scope
- 跨蘇茉的共用知識放在 global scope
- 類似 Claude 的 agent:<id> scope 設計
```

#### P3 — 長期願景

**8. KAIROS 持續監控（概念研究）**

```
對應：KAIROS 24/7 後台代理
現況：無此機制
說明：
- 這是 Claude Code 尚未公開的功能
- 涉及 heartbeat tick、終端焦點感知、15 秒預算限制
- 蘇茉家族目前不需要這麼積極的自主代理
- 但其中的「終端焦點感知」概念值得借鑒
```

---

## 四、具體改進建議清單

### 4.1 高優先順序

| # | 建議 | 對應 Claude | 實作難度 | 預期效益 |
|---|------|------------|---------|---------|
| 1 | 建立 `.sumo/memory/MEMORY.md` 索引機制 | MEMORY.md | 低 | 提升啟動上下文品質 |
| 2 | 實作 Topic 檔案自動分類（memory → .md 檔案） | Auto Memory topic files | 中 | 雙寫一致性 |
| 3 | 建立統一的蘇茉家族指令體系（多層級 CLAUDE.md） | CLAUDE.md 多層體系 | 低 | 更好的行為一致性 |
| 4 | 啟用並優化 memory-lancedb-pro 的 sessionMemory | Session Memory | 低 | 更好的跨對話記憶 |

### 4.2 中期優化

| # | 建議 | 對應 Claude | 實作難度 | 預期效益 |
|---|------|------------|---------|---------|
| 5 | 實作 AutoDream CRON job（記憶整理） | AutoDream | 高 | 記憶去重、自動化維護 |
| 6 | Session 摘要雙寫（ LanceDB + 日記檔） | compact/resume | 中 | 豐富的 resume 體驗 |
| 7 | 每個蘇茉獨立 scope（agent:<id>） | Per-agent memory | 中 | 更好的記憶隔離 |
| 8 | 借鑒「終端焦點感知」調整蘇茉響應策略 | KAIROS terminal awareness | 低 | 更智慧的蘇茉響應 |

---

## 五、結論

Claude Code 的六維記憶體系展示了 AI 代理記憶設計的最佳實踐：

1. **指令記憶（L1）**：人類編寫，永久有效，分層次結構
2. **長期記憶（L2）**：AI 自動寫入，主題分類，索引分層
3. **工作記憶（L3）**：對話內即時摘要，可恢復
4. **整理記憶（L4）**：後台自動整理，避免記憶膨脹

**蘇茉家族目前的差距**：
- ✅ 有 AGENTS.md / SOUL.md（指令層）
- ✅ 有 memory-lancedb-pro（向量長期記憶）
- ✅ 有 SumoNoteBook（文件知識庫）
- ❌ 無 MEMORY.md 索引機制
- ❌ 無 AI 自動總結寫入的記憶
- ❌ 無自動整理（AutoDream）
- ❌ 無 topic 檔案的按需載入

**建議行動**：
1. **立即**：建立 `.sumo/memory/MEMORY.md` 索引機制
2. **立即**：建立統一的蘇茉家族指令體系
3. **短期**：實作 Topic 檔案雙寫
4. **中期**：實作 AutoDream 概念驗證

---

## 參考資源

1. [Claude Code 官方 Memory 文件](https://code.claude.com/docs/en/memory)
2. [AI Insight — Claude Code Memory 機制分析](https://www.ai-insight.org/reports/claude-code-memory-2026)
3. [Advanced Claude Code Deep Dive — Ch08 Memory System](https://book.cuiliang.ai/advanced-claude-code-deep-dive/part-2/ch08-memory-system.html)
4. [ThePlanetTools — KAIROS and AutoDream](https://theplanettools.ai/blog/claude-code-kairos-autodream-ai-never-sleeps)
5. [memory-lancedb-pro GitHub](https://github.com/CortexReach/memory-lancedb-pro)
6. [SumoNoteBook 文件系統](C:\butler_sumo\library\SumoNoteBook\)

---

*報告完成：高工蘇茉 2026-04-06*
