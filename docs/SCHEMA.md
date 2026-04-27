# SumoNoteBook Schema 定義

> 基於 Karpathy LLM Wiki 概念的結構化定義

---

## 三層架構

### 1. Raw Sources（原創來源）
存放未處理的原始資料：
- `raw/` - 原始來源檔案
- `raw/processed/` - 處理過但尚未系統化的資料
- `learning/` - 學習筆記

### 2. Wiki（知識庫）
結構化的知識節點：
- `Sumo_wiki/concepts/` - 概念頁面
- `Sumo_wiki/summaries/` - 摘要頁面
- `Sumo_wiki/qa/` - 問答頁面
- `Sumo_wiki/backlinks/` - 反向連結索引
- `Sumo_wiki/agents/` - Agent 技術相關（蘇茉家族、Multi-agent 等）
- `Sumo_wiki/prompts/` - Prompt 設計技巧
- `Sumo_wiki/workflows/` - 工作流程模板
- `Sumo_wiki/research/` - 研究報告（論文、知識）

### 3. Schema（綱要）
定義組織規則的元資料：
- `docs/SCHEMA.md`（本檔）- 結構定義
- `docs/*.md` - 整合指南
- `Sumo_wiki/SOUL.md` - 核心準則

### 4. YouTube Distiller 同步
YouTube 知識蒸餾器的自動同步機制：
- `tools/youtube-distiller/` - YouTube Distiller 工具目錄
- `tools/youtube-distiller/sync_log.md` - 同步日誌
- `SumoNoteBook/raw/shared/` - 同步目標目錄（格式：YYYYMMDD__Main__標題.md）

---

## 兩個關鍵檔案

### index.md（Wiki 目錄）
**目的**：內容導向的快速檢索

**格式**：
```markdown
# 📚 標題

> 一行描述

## 分類

### 概念筆記 (concepts/)
- page1: 頁面描述
- page2: 頁面描述

### 摘要 (summaries/)
- summary1: 摘要描述
```

**自動更新**：
- 每次 INGEST 後自動更新 index.md
- 使用 `<!-- AUTO_UPDATE -->` 標記

### log.md（活動日誌）
**目的**：時間順序的完整記錄

**格式**：
```markdown
# 📋 活動日誌

## [YYYY-MM-DD HH:MM] type | 標題
- 欄位1: 值
- 欄位2: 值
- Report: report.md
```

**Parser 指令**：
```bash
# 最後 5 個 INGEST
grep "^## \[" log.md | grep "ingest" | tail -5

# 今天的活動
grep "^## \[$(date +%Y-%m-%d)\]" log.md

# 本週的 LINT
grep "^## \[" log.md | grep "lint" | tail -10
```

**自動更新**：
- 每次 INGEST/QUERY/LINT 後自動更新
- 使用 `<!-- AUTO_LOG -->` 標記

---

## 三個主要流程

### Ingest（攝入）
將新來源整合進 Wiki：

1. **接收來源**
   - 網址、檔案對話內容、搜尋結果

2. **處理來源**
   - 提取關鍵資訊
   - 識別概念
   - 生成摘要

3. **寫入 Wiki**
   - 建立/更新概念頁面：`Sumo_wiki/concepts/{概念}.md`
   - 建立/更新摘要頁面：`Sumo_wiki/summaries/{摘要ID}.md`
   - 建立反向連結：`Sumo_wiki/backlinks/{頁面ID}.md`

4. **更新 index**
   - 更新 index.md 分類
   - 附加到 log.md

5. **執行 Lint**
   - 自動執行健康檢查確保無斷裂連結

### Query（查詢）
從 Wiki 擷取資訊：

1. **接收問題**
   - 使用 notebook-rag skill 或直接查詢

2. **搜尋相關頁面**
   - 使用關鍵字搜尋
   - 檢查反向連結

3. **生成答案**
   - 綜合相關資訊
   - 引用來源

4. **記錄結果**
   - 附加到 log.md

### Lint（健康檢查）
保持 Wiki 品質：

1. **執行檢查**
   ```bash
   python scripts/health_check_v3.py
   ```

2. **檢查項目**
   - 斷裂連結（Broken links）
   - 孤兒頁面（Orphan pages）
   - 過時內容（Stale content）
   - 矛盾檢測（Contradictions）
   - 空頁面（Empty pages）

3. **生成報告**
   - `Sumo_wiki/health_report.md`

4. **記錄結果**
   - 附加到 log.md

---

## Wiki 連結語法

### 內部連結
```markdown
[[page_name]]           -- 基本連結
[[page_name|顯示文字]]   -- 別名連結
[[page_name#anchor]]     -- 錨點連結
```

### 外部連結
```markdown
[顯示文字](https://...)
```

### 標籤
```markdown
#概念標籤
#multiple_words
```

---

## 檔案命名規範

| 類型 | 目錄 | 命名規則 |
|------|------|----------|
| 概念 | `concepts/` | `kebab-case` 或中文標題 |
| 摘要 | `summaries/` | UUID 或時間戳記 |
| QA | `qa/` | `question_summary` 格式 |
| 反向連結 | `backlinks/` | 對應目標的 UUID |
| Agent 技術 | `agents/` | UUID（來自 summaries 移入）|
| Prompt 設計 | `prompts/` | UUID 或描述性名稱 |
| 工作流程 | `workflows/` | 描述性名稱 |
| 研究報告 | `research/` | UUID（來自 summaries 移入）|

---

## 任務導向分類（新）

基於 prompt-in-context-learning 的實用分類方式：

| 分類 | 說明 |
|------|------|
| **Survey** | 綜合性論文導讀 → `research/` |
| **Prompt Design** | Prompt 設計技巧 → `prompts/` |
| **Chain of Thought** | 思維鏈相關 → `prompts/` |
| **Agent** | 代理人技術 → `agents/` |
| **RAG** | 檢索增強生成 → `research/` |

---

## Cron 排程（建議）

| 時間 | 任務 |
|------|------|
| 每日 05:21 | 健康檢查 (Lint) |
| 每日 06:00 | 同步最新內容 |
| 每週一 | 週報生成 |

---

## 與 AGENTS.md 的整合

在蘇茉的 AGENTS.md 中加入：

```markdown
## SumoNoteBook 操作

### Ingest 新來源
1. 來源處理 → 概念/摘要頁面
2. 更新 index.md
3. 更新 log.md
4. 執行 Lint

### Query 查詢
1. 搜尋相關頁面
2. 綜合答案
3. 記錄到 log.md

### Lint 健康檢查
指令：`/notebook-lint`
或執行：`python c:/butler_sumo/library/SumoNoteBook/scripts/health_check_v3.py`
```

---

## 相關檔案

- `Sumo_wiki/SOUL.md` - SumoNoteBook 靈魂準則
- `Sumo_wiki/index.md` - Wiki 目錄
- `Sumo_wiki/log.md` - 活動日誌
- `Sumo_wiki/health_report.md` - 健康報告
- `scripts/health_check_v3.py` - Lint 腳本

---

> 此 Schema 定義基於 Karpathy LLM Wiki 概念（2026-04-07 高工蘇茉建立）