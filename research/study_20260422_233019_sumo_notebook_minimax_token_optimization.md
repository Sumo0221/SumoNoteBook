# SumoNoteBook + MiniMax Token 節省方案研究報告

**研究日期**：2026-04-22 23:30
**研究主題**：借鏡 NotebookLM + Claude 方法，應用於 SumoNoteBook + MiniMax
**存放位置**：先進研究室 (-5210713325)

---

## 1. NotebookLM + Claude 的核心方法

### 1.1 核心原理：分工架構

NotebookLM + Claude 的核心方法是**分工架構**：

| 工作 | 處理者 | Token 成本 |
|------|--------|------------|
| 大量文件處理、分析、索引 | NotebookLM（Google 提供） | **免費** |
| 查詢意圖理解、流程编排 | Claude | 微量的 Tokens |
| 最終輸出潤飾、格式化 | Claude | 微量的 Tokens |

**關鍵洞察**：讓昂貴的 Claude 專注推理，讓免費的 NotebookLM 負責資料檢索。

實測可節省 **17 倍費用**（來源：DeTools 工具翼零）。

### 1.2 NotebookLM 的關鍵功能：Source Groundings

NotebookLM 最核心的功能是 **Source Groundings**（來源溯源）：

- 可以精確選取文件中的**特定段落**作為回答依據
- 每一個回答都附帶**引用連結**，標明來源
- 不會產生幻覺，因為答案都基於實際文件
- 2M token 上下文窗口，可處理多達 25M 字的資料

**這就是關鍵**：NotebookLM 不是把整份文件丟給 Claude，而是讓 Claude 只取得**需要的片段**。

### 1.3 具體實現方式

透過 MCP（Model Context Protocol）將 NotebookLM 與 Claude 連接：

```
┌──────────────┐     MCP      ┌──────────────┐
│  NotebookLM  │◄─────────────►│    Claude     │
│  (本地 CLI)  │   自動查詢     │  (编排器)    │
└──────────────┘              └──────────────┘
       ▲                              ▲
       │ 免費處理文件                  │ 少量 Token
       │                              │
  ┌────┴────┐                   ┌────┴────┐
  │ 上傳50份 │                   │ 最終輸出 │
  │ 來源    │                   │ 潤飾    │
  └─────────┘                   └─────────┘
```

工作流程：
1. 使用 `notebooklm-py` CLI 上傳文件到 NotebookLM
2. Claude 自動查詢 NotebookLM，獲取答案
3. Claude 只負責编排和最終潤飾
4. 答案直接下載到本地

---

## 2. 應用到 SumoNoteBook + MiniMax 的可行性分析

### 2.1 SumoNoteBook 目前的內容選取方式

SumoNoteBook 已具備完善的搜尋系統：

| 功能 | 說明 |
|------|------|
| **LanceDB 向量搜尋** | 語義相似度匹配 |
| **FTS5 關鍵詞搜尋** | 全文檢索 |
| **Hybrid 混合搜尋** | 向量 + 關鍵詞加權 |
| **RDT 迭代深化** | 根據結果持續優化查詢 |

**現有流程**：
```
用戶查詢 → 搜尋引擎 → 取得 Top-K 結果 → 塞入 Context → 送給 MiniMax
```

**問題點**：
1. 目前的搜尋只返回 **snippet（片段）**，不是完整文件內容
2. 返回的是 200 字以內的摘要，不是原始文件的完整段落
3. 缺少 **Source Groundings** 功能——精確選取特定段落的機制

### 2.2 MiniMax API 特性

| 項目 | 內容 |
|------|------|
| **Model** | MiniMax-M2.7 / MiniMax-M2.5 |
| **Context Window** | 最高 1M tokens |
| **Input Cost** | ~$0.255/1M tokens |
| **Output Cost** | ~$1/1M tokens |

**優勢**：
- 價格遠低於 Claude（Claude Sonnet 4 約 $3/1M input）
- 超長上下文（1M tokens），可一次消化大量文件
- 已整合進 OpenClaw，可直接使用

### 2.3 可優化環節分析

```
目前流程（高 Token）：
┌──────────────┐
│ 用戶查詢     │
└──────┬───────┘
       ▼
┌──────────────────┐
│ 混合搜尋 Top-10  │  ← 只取 200 字 snippet
└──────┬───────────┘
       ▼
┌──────────────────┐
│ 塞入完整 context │  ← 問題：context 可能包含不相關內容
└──────┬───────────┘
       ▼
┌──────────────────┐
│ MiniMax 回應     │  ← 花費大量 Token
└──────────────────┘

優化後流程（省 Token）：
┌──────────────┐
│ 用戶查詢     │
└──────┬───────┘
       ▼
┌──────────────────┐
│ 精確段落選取     │  ← 只取與查詢相關的完整段落
└──────┬───────────┘
       ▼
┌──────────────────┐
│ Source Grounds   │  ← 附加引用資訊
└──────┬───────────┘
       ▼
┌──────────────────┐
│ MiniMax 回應     │  ← 只處理必要的內容
└──────────────────┘
```

---

## 3. 具體實施建議

### 3.1 新增 Source Groundings 功能

仿效 NotebookLM，在 SumoNoteBook 新增「精確段落選取」：

```python
# 概念：回傳完整相關段落，而非僅 200 字 snippet
def search_with_source_grounding(query, top_k=5):
    """
    1. 先用向量搜尋找到相關文件
    2. 讀取這些文件的完整內容
    3. 用滑動窗口找出與查詢最相關的段落
    4. 回傳這些段落（附加檔案位置、行號）
    """
    results = hybrid_search(query, top_k)
    grounded_results = []
    
    for r in results:
        # 讀取完整文件
        with open(r['file_path'], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找出最相關的段落（滑動窗口）
        relevant_passages = find_relevant_passages(content, query)
        
        grounded_results.append({
            'file_path': r['file_path'],
            'title': r['title'],
            'passages': relevant_passages,  # 完整段落，而非 200 字
            'source_id': generate_citation_id(),
        })
    
    return grounded_results
```

### 3.2 實作「段落級引用」

NotebookLM 的核心價值是**每一個回答都標明來源**。建議：

| 功能 | 說明 |
|------|------|
| **passage_id** | 段落的唯一識別符 |
| **file_path** | 來源檔案 |
| **line_range** | 行號範圍（如 "lines 45-67"） |
| **content** | 段落完整內容 |

### 3.3 實作「漸進式上下文載入」

目前的問題是一次性把所有內容塞給 MiniMax。建議改為：

1. **Level 1**：只傳送查詢 + 最相關的一段話
2. **Level 2**：若 MiniMax 表示資訊不足，再補充更多段落
3. **Level 3**：最後才開放大上下文（1M tokens）

類似這樣：

```
用戶: "蘇茉家族的記憶系統是什麼？"

Level 1 (最精簡):
  - 傳送: query + MEMORY.md 的相關段落
  - 花費: ~500 tokens

Level 2 (需要更多):
  - 補充: memory/ 資料夾的其他相關檔案
  - 花費: ~2000 tokens

Level 3 (完整上下文):
  - 開放: 全部相關文件
  - 花費: ~5000 tokens
```

### 3.4 預期 Token 節省效果

| 場景 | 目前 | 優化後 | 節省比例 |
|------|------|--------|----------|
| 簡單查詢 | ~3000 tokens | ~500 tokens | **~85%** |
| 複雜研究 | ~15000 tokens | ~3000 tokens | **~80%** |
| 文件分析 | ~50000 tokens | ~10000 tokens | **~80%** |

### 3.5 需要的技術改動

| 項目 | 優先級 | 說明 |
|------|--------|------|
| **段落分割器** | P0 | 將文件切成有意義的段落 |
| **相關性評分** | P0 | 評估每個段落與查詢的相關性 |
| **Source Grounding 格式** | P0 | 統一的引用格式 |
| **漸進式載入** | P1 | Level-based context loading |
| **Citation 產生器** | P1 | 自動產生引用 ID |
| **UI 整合** | P2 | 在回應中顯示引用連結 |

---

## 4. 結論

### 4.1 NotebookLM + Claude 的核心價值

1. **分工**：讓免費的工具處理重型工作
2. **精確選取**：只傳送相關段落，而非整份文件
3. **引用回溯**：每個答案都標明來源

### 4.2 SumoNoteBook + MiniMax 的可行方向

SumoNoteBook 已有類似的搜尋引擎，只需加強：

1. **從 snippet 到 passage**：不要只傳 200 字，要傳完整段落
2. **增加引用資訊**：每個回答都要有 source grounding
3. **漸進式載入**：不要一次傳送全部，先傳最相關的

### 4.3 下一步行動建議

1. **工程師蘇茉**實作段落分割器
2. **工程師蘇茉**實作 Source Grounding 格式
3. **教授蘇茉**持續優化 RDT 引擎

---

*研究完成時間：2026-04-22 23:30 GMT+8*
