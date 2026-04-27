# qmd 搜尋引擎整合指南

## 📋 概述

**qmd** 是一個本地 Markdown 搜尋引擎，支援：
- BM25 關鍵字搜尋
- 向量搜尋（Embedding）
- LLM 重排（Re-ranking）
- CLI 命令列工具
- MCP Server（可被 AI Agent 呼叫）

官網：https://github.com/tobi/qmd

---

## 🎯 為什麼要用 qmd？

| 傳統 RAG | qmd 搜尋 |
|----------|----------|
| 簡單關鍵字 | 語義理解 |
| 無排序 | LLM 重排 |
| 慢速 | 快速本地 |
| 需雲端 API | 完全本地 |

---

## 🔧 安裝步驟

### 需求
- Python 3.10+
- rustc（C擴編需要）

### 安裝 qmd

```bash
# 使用 pip 安裝
pip install qmd

# 或使用 cargo（如果你有 Rust）
cargo install qmd
```

### 驗證安裝

```bash
qmd --version
```

---

## ⚙️ 配置步驟

### 1. 初始化 qmd 索引

```bash
cd C:\butler_sumo\library\SumoNoteBook\Sumo_wiki
qmd index --path . --recursive
```

### 2. 配置 qmd

建立 `~/.qmd/config.toml`：

```toml
[server]
host = "127.0.0.1"
port = 8777

[search]
default_limit = 20
rerank = true
rerank_topk = 10

[embedding]
model = "sentence-transformers/all-MiniLM-L6-v2"
device = "cpu"  # 或 "cuda"
```

### 3. 啟動 qmd 伺服器

```bash
qmd serve --path "C:\butler_sumo\library\SumoNoteBook\Sumo_wiki"
```

### 4. 測試搜尋

```bash
qmd search "SumoNoteBook 是什麼" --limit 5
```

---

## 🔌 MCP Server 整合

qmd 作為 MCP Server 可以被 AI Agent 直接呼叫。

### 配置 OpenClaw MCP

在 `openclaw.json` 中加入：

```json
{
  "mcp": {
    "servers": {
      "qmd": {
        "command": "qmd",
        "args": ["mcp", "--path", "C:/butler_sumo/library/SumoNoteBook/Sumo_wiki"]
      }
    }
  }
}
```

### qmd MCP 工具

| 工具 | 說明 |
|------|------|
| `qmd_search` | 搜尋 Wiki 內容 |
| `qmd_index` | 更新索引 |
| `qmd_status` | 查看索引狀態 |

### 使用範例

```markdown
用戶：搜尋 SumoNoteBook 相關內容

Agent：
```
qmd_search({
  query: "SumoNoteBook 架構",
  limit: 5
})
```
```

---

## 🚀 命令列工具

### 搜尋
```bash
# 基本搜尋
qmd search "你的問題"

# 限制結果數
qmd search "問題" --limit 10

# 只搜概念
qmd search "問題" --path concepts/

# 搜摘要
qmd search "問題" --path summaries/
```

### 索引管理
```bash
# 重新索引
qmd index --rebuild

# 新增單一檔案
qmd index --file path/to/file.md

# 查看索引狀態
qmd status
```

### 過濾器
```bash
# 只搜中文
qmd search "問題" --lang zh

# 只搜大於 1000 bytes 的檔案
qmd search "問題" --min-size 1000
```

---

## 📊 效能調優

### 硬體需求

| 模式 | 記憶體 | 速度 |
|------|--------|------|
| CPU | 2GB+ | 慢 |
| GPU | 4GB+ | 快 |

### 索引優化

```bash
# 使用更快但較不精確的搜尋
qmd search "問題" --mode bm25

# 使用語義搜尋（需要 embedding model）
qmd search "問題" --mode semantic
```

---

## 🔄 自動化

### 鉤子（Hooks）

在 `~/.qmd/hooks.toml` 設定：

```toml
[hooks.on_index]
command = "echo '索引已更新'"
```

### Cron 自動重建索引

```bash
# 每天凌晨 3 點重建索引
0 3 * * * qmd index --rebuild --path "C:\butler_sumo\library\SumoNoteBook\Sumo_wiki"
```

---

## 📝 整合到 SumoNoteBook

### 更新 SOUL.md

在 SOUL.md 的 QUERY 流程中加入：

```markdown
#### 方式 C：qmd 搜尋（推薦）

```bash
qmd search "你的問題"
```

或使用 MCP：

```json
{"tool": "qmd_search", "query": "你的問題"}
```
```

---

## ✅ 檢查清單

- [ ] 安裝 qmd
- [ ] 建立索引
- [ ] 配置 MCP Server
- [ ] 測試搜尋
- [ ] 整合到 OpenClaw
- [ ] 設定自動更新索引

---

## ❓ 常見問題

### Q: qmd 找不到結果？
A: 確保索引已建立，嘗試 `--rebuild`

### Q: 記憶體不足？
A: 使用 `--mode bm25` 代替 `--mode semantic`

### Q: MCP 無法連接？
A: 檢查 qmd 伺服器是否運行：`qmd status`