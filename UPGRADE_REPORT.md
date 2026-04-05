# SumoNoteBook 升級報告

## 升級日期
2026-04-06

## 升級背景

原本的 SumoNoteBook 只是一個被動的 RAG 檢索系統，沒有結構化的維護機制。高工蘇茉研究並實作了 Karpathy 的個人知識庫概念。

---

## 升級內容

### 1. 新增 SOUL.md（知識庫靈魂準則）

**位置**：`Sumo_wiki/SOUL.md` (8.1 KB)

**內容**：
- 三層架構：Raw Sources → Wiki → Schema
- 三個核心流程：Ingest、Query、Lint
- 兩個特殊檔案：index.md（總索引）、log.md（活動日誌）
- 7 條蘇茉家族共同維護準則
- 命名規則和品質標準

### 2. 新增 log.md（活動日誌）

**位置**：`Sumo_wiki/log.md` (492 bytes)

**用途**：追蹤 INGEST/LINT 活動的時間軸

### 3. 更新 index.md

**位置**：`Sumo_wiki/index.md`

**更新內容**：新增核心準則區塊，引用 SOUL.md

---

## 三層架構說明

```
Layer 1: RAW SOURCES (raw/)
  - 原始資料，老爺放置檔案
  - 尚未結構化

Layer 2: WIKI (Sumo_wiki/)
  - 結構化的蘇茉家族知識
  - concepts/ - 概念原子筆記
  - summaries/ - 原始檔案摘要
  - backlinks/ - 反向連結索引

Layer 3: SCHEMA (SOUL.md)
  - 定義如何 Ingest/Query/Lint 的規則
```

---

## 三個核心流程

### Ingest（攝取）
- 觸發時機：raw/ 中有新檔案（每日 4:12 AM 自動執行）
- 流程：掃描 → 建立摘要 → 提取概念 → 建立反向連結 → 記錄到 log.md

### Query（查詢）
- 觸發時機：老爺或蘇茉提出知識問題時
- 優先順序：concepts/ → summaries/ → backlinks/

### Lint（維護）
- 觸發時機：定期檢查（每週日 6:00 AM）
- 檢查：矛盾、過時資訊、孤立頁面、斷裂連結

---

## 7 條維護準則

1. Wiki 必須自我描述：每個頁面解釋自己是什麼
2. 標題命名：使用描述性標題
3. 最小承諾：每個 ingest 至少更新 index.md
4. 質疑細節：不確定的內容要標記
5. 保持更新：新資訊優先
6. 拒絕抄襲：內容必須原創或改寫
7. 回應請求：有問必答，有查必記

---

## 向量搜索功能修復

### 問題
query_notebook.mjs 查詢時所有 score 都是 0.0000

### 根因
LanceDB JS SDK 回傳 `_distance` 不是 `_score`

### 修復
修改 query_notebook.mjs：
```javascript
// 舊：r._score ?? 0
// 新：r._distance ?? r._score ?? 0 → 轉換為相似度 (1 - distance)
```

---

## 未來改進方向

1. 修改 daily_organizer.py 和 health_check.py 自動更新 log.md
2. 清理 concepts/ 中的孤兒檔案
3. 建立自動化 Lint 腳本
4. 實作真正的 Option C（在 memory-lancedb-pro 中加入對 sumo_notebook table 的查詢）

---

## 升級後的檔案結構

```
SumoNoteBook/
├── raw/                          # Layer 1: 原始資料
│   ├── processed/                 # 已處理的檔案
│   └── ...
├── Sumo_wiki/                    # Layer 2: 知識庫
│   ├── SOUL.md              # 🆕 知識庫靈魂準則（新增）
│   ├── log.md               # 🆕 活動日誌（新增）
│   ├── index.md              # 🆕 更新：加入核心準則區塊
│   ├── concepts/             # 概念原子筆記
│   ├── summaries/            # 原始檔案摘要
│   ├── backlinks/            # 反向連結索引
│   ├── qa/                   # 問答記錄
│   └── daily/                # 每日筆記
├── learning/                   # 蘇茉學習筆記
│   ├── engineer/
│   ├── lawyer/
│   ├── professor/
│   └── ...
├── scripts/                     # 現有腳本
│   ├── ingest_notebook.mjs
│   ├── query_notebook.mjs
│   └── ...
└── README.md
```

---

*升級者：高工蘇茉 (Senior Engineer SuMo)*
*記錄者：總管蘇茉 (TotalControlSuMo)*