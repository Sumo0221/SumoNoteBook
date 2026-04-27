# SumoNoteBook RAG System

## Overview

本地 RAG（Retrieval-Augmented Generation）系統，讓蘇茉能夠語義搜索 SumoNoteBook 知識庫。

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Markdown Files │───▶│  Ingestion Script │───▶│    LanceDB      │
│  (SumoNoteBook) │    │  (embed + chunk) │    │  sumo_notebook  │
└─────────────────┘    └──────────────────┘    └────────┬────────┘
                                                       │
                        ┌──────────────────┐             │
                        │  Query Script    │◀────────────┘
                        │  (semantic search)│
                        └────────┬─────────┘
                                 │
                        ┌────────▼─────────┐
                        │  Ollama Embedding │
                        │  (nomic-embed-text)│
                        └──────────────────┘
```

## Components

### 1. Ingestion Script (`ingest_notebook.mjs`)
- 掃描 SumoNoteBook 所有 `.md` 檔案
- 文字分塊（max 1500 chars per chunk，overlap 100）
- 使用 Ollama `nomic-embed-text` 批次 embedding
- 存入 LanceDB `sumo_notebook` 表（768-dim vectors）

### 2. Query Script (`query_notebook.mjs`)
- 對查詢文字做 embedding
- 在 LanceDB 中做 cosine distance 相似度搜索
- 返回 top-K 相關內容

## Usage

### Ingestion（首次或增量更新）

```bash
cd C:\butler_sumo\library\SumoNoteBook\scripts

# 首次攝取（全量重建）
node ingest_notebook.mjs --rebuild

# 增量更新（只新增，保留舊資料）
node ingest_notebook.mjs

# 查看幫助
node ingest_notebook.mjs --help
```

### Query（搜尋知識庫）

```bash
cd C:\butler_sumo\library\SumoNoteBook\scripts

# 語義搜尋
node query_notebook.mjs "蘇茉家族多代理架構" --top=5

# JSON 輸出
node query_notebook.mjs "你的問題" --json

# 自訂回傳數量
node query_notebook.mjs "你的問題" --top=10
```

## Configuration

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `ollama.baseURL` | `http://localhost:11434/v1` | Ollama API endpoint |
| `ollama.model` | `nomic-embed-text` | Embedding 模型 |
| `lancedb.dbPath` | `~/.openclaw/memory/lancedb-pro` | LanceDB 目錄 |
| `lancedb.tableName` | `sumo_notebook` | 表名 |
| `chunking.maxChunkSize` | `1500` | 最大分塊大小 |
| `chunking.overlapSize` | `100` | 重疊大小 |
| `embedBatchSize` | `4` | 批次大小 |

## Current Stats

- **Files indexed**: 117 .md files
- **Total chunks**: 260
- **Total text**: 327 KB
- **Vector dimensions**: 768 (nomic-embed-text)
- **Storage**: LanceDB at `~/.openclaw/memory/lancedb-pro/sumo_notebook/`

## OpenClaw Integration (Phase 4)

### Option A: Dedicated RAG Skill (Recommended)
建立一個 OpenClaw skill，在訊息處理前鉤入 RAG 檢索：
1. 接收用戶訊息
2. 呼叫 `query_notebook.mjs` 取得相關內容
3. 將內容附加為 system prompt context
4. 送給 LLM 生成回覆

### Option B: Extend memory-lancedb-pro Plugin
修改現有 `memory-lancedb-pro` 插件，在 `retrieve()` 方法中：
1. 新增 `sumo_notebook` 表的 vector search
2. 將結果與現有 memory 結果合併
3. 統一返回給 retriever

### Integration Points
- **Trigger**: 每則用戶訊息
- **Context**: 附加到 system prompt 或 user message
- **Top-K**: 建議 3-5 條結果
- **Max context**: 建議不超過 2000 chars

## Troubleshooting

### Ollama 未運行
```bash
ollama serve
# 或在 Windows 上
Start-Process ollama
```

### 400 Bad Request (context length)
- 降低 `maxChunkSize`（目前 1500）
- 或降低 `embedBatchSize`（目前 4）

### LanceDB 向量搜索返回空
- 確認 `sumo_notebook` 表存在：`node -e "import('@lancedb/lancedb').then(async m => { const db = await m.connect('...'); console.log(await db.tableNames()) })"`
- 確認表有資料：`tbl.countRows()`

## Future Enhancements

1. **Incremental updates**: 只重新索引變更的檔案（基於 mtime）
2. **Hybrid search**: 結合 BM25 keyword search + vector search
3. **Reranking**: 使用 cross-encoder 重新排序結果
4. **Auto-ingest**: Cron job 定期更新索引
5. **Metadata filtering**: 支援按目錄/日期過濾

## Files

```
C:\butler_sumo\library\SumoNoteBook\scripts\
├── ingest_notebook.mjs   # 主攝取腳本
├── query_notebook.mjs    # 查詢腳本
├── test_query.mjs        # 測試腳本
├── package.json          # Node.js 依賴
├── package-lock.json
└── README.md             # 本文件
```
