# SumoNoteBook 使用範例

**版本**: v1.0  
**作者**: 高工蘇茉 (SeniorEngineerSuMo)  
**日期**: 2026-04-05  
**適用**: SumoNoteBook RAG + LanceDB

---

## 📋 概述

SumoNoteBook 是一套會自己長大的百科全書，使用 LanceDB 作為向量資料庫。
資料存放於 `C:\Users\rayray\.openclaw\memory\lancedb-pro sumo_notebook.lance`

### 核心腳本
| 腳本 | 用途 |
|------|------|
| `ingest_notebook.mjs` | 寫入（攝取資料） |
| `query_notebook.mjs` | 讀取（查詢） |

---

## 1️⃣ 寫入範例（攝取資料到 sumo_notebook.lance）

### 基本語法

```bash
cd C:\butler_sumo\library\SumoNoteBook\scripts
node ingest_notebook.mjs [選項]
```

### 選項

| 選項 | 說明 |
|------|------|
| `--rebuild` | 刪除並重建資料表（完整重整） |
| `--limit N` | 限制處理檔案數（除錯用） |
| `--help` | 顯示說明 |

### 正常攝取（增量）

```bash
node ingest_notebook.mjs
```

### 完整重建

```bash
node ingest_notebook.mjs --rebuild
```

### 實際輸出範例

```
============================================================
SumoNoteBook RAG Ingestion v2 (OpenAI SDK)
============================================================
Ollama: http://localhost:11434/v1 / nomic-embed-text
LanceDB: C:\Users\rayray\.openclaw\memory\lancedb-pro
Notebook: C:\butler_sumo\library\SumoNoteBook
Mode: INCREMENTAL

[1/5] Connecting to LanceDB...
  ✓ Connected

[2/5] Scanning Markdown files...
  Found 42 .md files

[3/5] Reading and chunking...
  [42/42] Sumo_wiki/concepts/python编程.md

  Total chunks: 156
  Total chars: 89.2 KB

[4/5] Testing Ollama connection...
  ✓ Ollama working (768-dim)

[5/5] Embedding chunks...
  [█████████████████████████████] 156/156 (100%)

  ✓ Embedded: 156  ⚠ Failed: 0

[STORE] Writing to LanceDB...
  ✓ Stored

============================================================
INGESTION COMPLETE
============================================================
  Files: 42
  Chunks: 156
  Time: 12.3s
  Speed: 12.7 chunks/s
```

---

## 2️⃣ 讀取範例（從 SumoNoteBook 查詢）

### 基本語法

```bash
cd C:\butler_sumo\library\SumoNoteBook\scripts
node query_notebook.mjs "你的查詢" [選項]
```

### 選項

| 選項 | 說明 |
|------|------|
| `--top=N` | 返回前 N 筆結果（預設 5） |
| `--json` | 以 JSON 格式輸出 |
| `--help` | 顯示說明 |

### 查詢範例

#### 簡單查詢

```bash
node query_notebook.mjs "Python 程式設計"
```

#### 限制結果數量

```bash
node query_notebook.mjs "機器學習" --top=3
```

#### JSON 輸出（供程式使用）

```bash
node query_notebook.mjs "OpenClaw 外掛" --json
```

#### 實際輸出範例

```
============================================================
TOP 3 RESULTS
============================================================

[1] Sumo_wiki/concepts/python.md (chunk 0) [score: 0.8923]
--------------------------------------------------
Python 是一種高階程式語言，特點包括：
- 語法簡潔、容易學習
- 豐富的第三方套件生態系
- 支援多範式程式設計

[2] Sumo_wiki/summaries/learning_notes.md (chunk 1) [score: 0.8456]
--------------------------------------------------
## Python 學習筆記

### 基本語法
```python
def hello():
    print("Hello, World!")
```

[3] Sumo_wiki/qa/programming_qa.md (chunk 0) [score: 0.8122]
--------------------------------------------------
Q: Python 和 JavaScript 有什麼差別？
A: Python 適合資料科學和後端，JavaScript 適合網頁前端...
```

---

## 3️⃣ Python 範例程式

### 攝取（寫入）資料

```python
import subprocess
import json

def ingest_to_sumo_notebook(rebuild=False):
    """
    將 SumoNoteBook 資料攝取到 LanceDB
    
    Args:
        rebuild: True = 刪除重建, False = 增量新增
    """
    cmd = [
        "node",
        "C:/butler_sumo/library/SumoNoteBook/scripts/ingest_notebook.mjs"
    ]
    if rebuild:
        cmd.append("--rebuild")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=__import__('sys').stderr)
    
    return result.returncode == 0

# 使用範例
if __name__ == "__main__":
    # 增量攝取（新檔案）
    ingest_to_sumo_notebook(rebuild=False)
    
    # 完整重建（重新處理所有檔案）
    # ingest_to_sumo_notebook(rebuild=True)
```

### 查詢（讀取）資料

```python
import subprocess
import json

def query_sumo_notebook(query_text, top_k=5, as_json=False):
    """
    查詢 SumoNoteBook RAG 向量資料庫
    
    Args:
        query_text: 查詢關鍵字
        top_k: 返回結果數量
        as_json: 是否輸出 JSON
    
    Returns:
        list: 查詢結果
    """
    cmd = [
        "node",
        "C:/butler_sumo/library/SumoNoteBook/scripts/query_notebook.mjs",
        query_text,
        f"--top={top_k}"
    ]
    if as_json:
        cmd.append("--json")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if as_json:
        return json.loads(result.stdout)
    else:
        # 解析文字輸出
        results = []
        lines = result.stdout.strip().split("\n")
        current_result = None
        
        for line in lines:
            if line.startswith("[") and "] " in line:
                # 解析標題行: [1] file.md (chunk 0) [score: 0.8923]
                import re
                match = re.match(r'\[(\d+)\] (.+) \(chunk (\d+)\) \[score: ([\d.]+)\]', line)
                if match:
                    if current_result:
                        results.append(current_result)
                    current_result = {
                        "rank": int(match.group(1)),
                        "source_file": match.group(2),
                        "chunk_index": int(match.group(3)),
                        "score": float(match.group(4)),
                        "text": ""
                    }
            elif current_result and not line.startswith("=") and not line.startswith("-"):
                current_result["text"] += line + "\n"
        
        if current_result:
            results.append(current_result)
        
        return results

# 使用範例
if __name__ == "__main__":
    results = query_sumo_notebook("Python 程式設計", top_k=3)
    
    for r in results:
        print(f"[{r['rank']}] {r['source_file']}")
        print(f"    Score: {r['score']:.4f}")
        print(f"    Text: {r['text'][:100]}...")
        print()
```

---

## 4️⃣ 批次處理範例

### 批次攝取多個資料夾

```python
import os
import subprocess
from pathlib import Path

def batch_ingest(folders: list[str], rebuild=False):
    """
    批次攝取多個資料夾到 SumoNoteBook
    
    Args:
        folders: 資料夾路徑列表
        rebuild: 是否重建資料表
    """
    for folder in folders:
        folder_path = Path(folder)
        if not folder_path.exists():
            print(f"⚠ 資料夾不存在: {folder}")
            continue
        
        print(f"📂 處理: {folder}")
        
        # 將資料複製到 SumoNoteBook/raw
        raw_folder = Path("C:/butler_sumo/library/SumoNoteBook/raw")
        # ... 複製檔案邏輯 ...
        
        print(f"  ✓ 複製完成")

    # 執行攝取
    cmd = ["node", "C:/butler_sumo/library/SumoNoteBook/scripts/ingest_notebook.mjs"]
    if rebuild:
        cmd.append("--rebuild")
    
    subprocess.run(cmd)

# 使用範例
batch_ingest([
    "C:/temp/docs/技術文件",
    "C:/temp/docs/會議記錄",
], rebuild=False)
```

---

## 5️⃣ 疑難排解

### 常見問題

| 問題 | 解決方案 |
|------|----------|
| `Table not found` | 先執行 `ingest_notebook.mjs` 建立資料表 |
| `Ollama connection failed` | 確認 Ollama 正在執行：`http://localhost:11434` |
| `Vector dim mismatch` | 檢查 `CONFIG.vectorDim` 是否為 768（nomic-embed-text） |
| `No chunks generated` | 確認 SumoNoteBook 有 .md 檔案 |

### 驗證狀態

```bash
# 確認 LanceDB 資料表存在
node -e "
const { connect } = require('@lancedb/lancedb');
connect('C:\\\\Users\\\\rayray\\\\.openclaw\\\\memory\\\\lancedb-pro')
  .then(db => db.tableNames())
  .then(names => console.log('Tables:', names));
"

# 確認 Ollama 正常
curl http://localhost:11434/api/tags
```

---

## 📊 資料格式

### LanceDB Schema

```javascript
{
  id: string,           // UUID
  text: string,         // chunk 文字內容
  source_file: string,  // 原始檔案路徑
  chunk_index: number,  // chunk 編號
  chunk_start: number,  // 起始位置
  chunk_end: number,    // 結束位置
  vector: float[768]    // 768 維度向量
}
```

### Chunk 設定

| 參數 | 值 | 說明 |
|------|-----|------|
| `maxChunkSize` | 1500 | 最大 chunk 字數 |
| `overlapSize` | 100 | 相鄰 chunk 重疊字數 |
| `minChunkSize` | 80 | 最小 chunk 字數 |
| `embedBatchSize` | 4 | 每批處理 4 個 chunks |
| `vectorDim` | 768 | nomic-embed-text 向量維度 |

---

## 🔗 相關連結

- **SumoNoteBook**: `C:\butler_sumo\library\SumoNoteBook`
- **LanceDB 資料庫**: `C:\Users\rayray\.openclaw\memory\lancedb-pro`
- **memory-lancedb-pro 插件**: `C:\Users\rayray\.openclaw\plugins\memory-lancedb-pro`
- **Option C 整合指南**: `C:\Users\rayray\.openclaw\plugins\memory-lancedb-pro\OPTION_C_DEV_GUIDE.md`

---

*高工蘇茉建立於 2026-04-05*