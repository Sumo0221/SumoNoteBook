# predict-rlm 應用價值深度研究

**研究目標：** 基於 predict-rlm 研究報告，深入分析如何將 RLM 概念應用到蘇茉家族系統  
**基於報告：** `predict_rlm_report.md`  
**研究日期：** 2026-04-27  
**研究者：** 教授蘇茉

---

## 📋 執行摘要

本報告深入探討如何將 **predict-rlm**（Recursive Language Model）的核心概念應用於蘇茉家族系統。基於之前的研究，RLM 的三大核心價值：**長上下文外部化處理**、**完整軌跡追蹤**、**小模型成本優化**，與蘇茉家族的多個場景高度契合。

**核心發現：**
- 文件分析是最直接的應用場景，可立即提升現有能力
- 軌跡追蹤與長期記憶系統整合具有高價值
- 小模型優化需審慎評估，與現有 MiniMax-M2 策略可能衝突
- 技術整合可行，但需階段性實施

---

## 1. 文件分析研究（PDF、發票、合同比對）

### 1.1 RLM 的長 Context 處理能力如何應用

#### 現有能力分析

蘇茉家族目前使用 `minimax/MiniMax-M2.7` 模型處理文件，具備：
- 圖片理解能力（文件掃描、截圖分析）
- 繁體中文理解
- 繁重的文件分析任務（如研究報告）

#### RLM 帶來的關鍵能力

| 能力 | 傳統方式 | RLM 方式 |
|------|---------|---------|
| **PDF 處理** | 一次性全部塞入 context | 分頁渲染，LM 自己決定讀哪些頁 |
| **長文檔分析** | 受限於 context window（~128K） | 可處理 10M+ token |
| **多文檔比對** | 全部同時處理，高損耗 | LM 主動規劃，哪些一起讀，哪些分開 |
| **發票/合同結構化** | 依賴 prompt engineering | 模型自發分解任務，串行優化 |

#### 技術機制

predict-rlm 的關鍵創新是 **REPL 環境中的程式化處理**：

```python
# 蘇茉家族的 PDF 分析可以被重構為：

class AnalyzeInvoices(dspy.Signature):
    """從 PDF 發票中提取結構化資訊。
    
    1. 先 survey 文檔：頁數、文件類型
    2. 選擇性渲染關鍵頁面（並非全部）
    3. 使用 predict() 提取發票日期、供應商、金額
    4. 合併結果並驗證
    """
    invoices: list[File] = dspy.InputField()
    extracted_data: InvoiceData = dspy.OutputField()
```

在 REPL 環境中，LM 會自己寫類似這樣的程式碼：

```python
import pymupdf, asyncio

# 蘇茉不需設計流程，LM 自己決定
doc = pymupdf.open(invoices[0])
# 決定只處理前 5 頁（模型自己判斷需要多少）
images = ["data:image/png;base64," + base64.b64encode(
    doc[i].get_pixmap(dpi=200).tobytes("png")
).decode() for i in range(min(5, len(doc)))]

# 並行處理多個頁面
results = await asyncio.gather(*[
    predict("page: dspy.Image -> line_items: list[str]", page=img)
    for img in images
])
```

### 1.2 具體可以改善哪些現有功能

#### 優先級 1：研究文件分析

**現有痛點：**
- 研究任務常需處理大量 PDF（論文、報告）
- 全部塞入 context 導致效能下降（context rot）
- 蘇茉需要手動設計分段策略

**改善後：**
- LM 自己決定分段策略和頁面選擇
- 完整軌跡可稽核每個決策
- 新增頁面時無需重新設計流程

**實施方式：**
```python
# 在現有架構上新增一個 RLM 風格的處理層
class ResearchDocumentAnalyzer:
    def __init__(self, agent):
        self.agent = agent  # 現有的蘇茉代理
    
    def analyze(self, pdf_path):
        # 步驟 1：用 OpenClaw 現有工具讀取 PDF
        # 步驟 2：自動分段（借用 RLM 的分頁策略）
        # 步驟 3：並行提取（類似 asyncio.gather）
        # 步驟 4：結構化輸出
```

#### 優先級 2：發票處理（如果蘇茉家族有此需求）

predict-rlm 的 `invoice_processing` 範例展示了完整的發票到 Excel 流程：
- PDF → 結構化資料 → Excel
- Skills 機制（pdf skill + spreadsheet skill）可複用

#### 優先級 3：合同比對

predict-rlm 的 `contract_comparison` 範例：
- 輸入兩個 PDF 版本
- 輸出結構化 diff 報告
- 每個差異都有上下文和原因

**對蘇茉家族的價值：** 
- 這正是研究報告中提到的「可解釋性」需求
- 每一個比對決策都有跡可循
- 適合法律、合規等需要稽核軌跡的場景

### 1.3 實作方向建議

#### 方案 A：完全整合 predict-rlm（長期）

**優點：**
- 直接獲得所有 RLM 能力
- 享受未來模型改進的紅利
- 軌跡完全可追蹤

**缺點：**
- 需要 Python 環境（OpenClaw 目前主要是 Node.js）
- 依賴 Pyodide/WASM 沙箱
- 學習曲線較陡

**實施步驟：**
1. 在 OpenClaw 環境中新增 Python 處理節點
2. 將 predict-rlm 包裝為 MCP 工具
3. 定義蘇茉家族的 Signature 集合
4. 遷移現有文件處理流程

#### 方案 B：概念借鑒，局部實現（推薦）

**核心思路：** 不引入完整的 predict-rlm 框架，而是借鑽其核心概念：

| RLM 概念 | 本地實現方式 |
|---------|------------|
| REPL 環境 | 使用 Node.js 子程序模擬 |
| predict() 呼叫 | 使用 MiniMax-M2 進行結構化提取 |
| 分頁策略 | 蘇茉自行實現的頁面選擇邏輯 |
| 軌跡追蹤 | 現有的對話歷史 + 新增决策日誌 |

**實施步驟：**
1. 在 SumoNoteBook 中新增 `document_processor` 模組
2. 實現基於頁面選擇的文件處理邏輯
3. 新增决策軌跡記錄（JSON 格式）
4. 建立 Signature 定義庫（針對常見任務）

#### 方案 C：外掛式整合（短期）

使用外部 Python 服務，蘇茉通過 MCP 呼叫：

```
┌─────────────────┐     MCP      ┌─────────────────┐
│   蘇茉家族       │ ──────────►  │  Python 服務     │
│   (OpenClaw)    │              │  (predict-rlm)  │
│                 │  ◄────────── │                 │
└─────────────────┘   結構化結果  └─────────────────┘
```

**優點：** 不改變現有架構，快速驗證
**缺點：** 額外維護成本，網路延遲

---

## 2. 軌跡追蹤與可解釋性

### 2.1 蘇茉家族現有的可解釋性功能

根據 SumoNoteBook 結構，蘇茉家族已有的可解釋性機制：

| 功能 | 位置 | 說明 |
|------|------|------|
| **記憶軌跡** | `memory/*.md` | 每日記憶日誌 |
| **決策記錄** | `closet/formal/` | 存放技術决策文檔 |
| **研究過程** | `research/*.md` | 研究報告的决策脈絡 |
| **健康報告** | `Sumo_wiki/health_report.md` | 系統狀態追蹤 |
| **對話歷史** | LCM (Lossless Context Management) | 完整對話壓縮管理 |

**現有不足：**
- 决策邏輯分散在各文件中
- 缺乏統一的軌跡標準格式
- 無法關聯「為什麼這樣做」的推理過程

### 2.2 RLM 的軌跡追蹤概念如何整合

predict-rlm 的 `RunTrace` 結構：

```python
class RunTrace:
    status: str                    # completed / max_iterations / error
    steps: list[IterationStep]     # 每一步的详细信息
    usage: TokenUsage              # token 統計
    
class IterationStep:
    iteration: int
    reasoning: str                 # LM 的推理過程
    code: str                      # 執行的程式碼
    output: str                    # 程式輸出
    tool_calls: list[ToolCall]     # 工具呼叫
    predict_calls: list[PredictCall]  # sub-LM 呼叫
    duration_ms: float
```

**整合到蘇茉家族的好處：**

1. **結構化决策記錄** — 蘇茉每個重要决策都有完整的推理鏈
2. **成本追蹤** — 每個任務的 token 消耗一目了然
3. **效能分析** — 識別瓶頸，優化流程
4. **稽核支援** — 對於合規需求可提供完整的决策證據

### 2.3 對長期記憶系統的幫助

#### 現有 Memory Dream 架構

根據 `MEMORY_DREAM_ARCHITECTURE.md`：
- **衰減機制**：記憶隨時間自動衰減
- **量化評分**：Importance + Recency + Kind_Bonus
- **多 Agent 共享**：所有蘇茉共享重要記憶

#### RLM 軌跡增强方案

```
┌─────────────────────────────────────────────────────────────┐
│                  Enhanced Memory System                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │  Decision   │ ──► │  RunTrace   │ ──► │  Memory     │   │
│  │  Point      │     │  (structured)│     │  Dream      │   │
│  └─────────────┘     └─────────────┘     └─────────────┘   │
│                                                             │
│  重要决策自動提升記憶分數：                                   │
│  - 高價值决策 → Importance × 1.2                           │
│  - 有完整軌跡 → +0.10 Kind_Bonus                           │
│  - 可解釋性要求 → 自動進入長期保存                            │
└─────────────────────────────────────────────────────────────┘
```

**新增資源：**
- `SumoNoteBook/traces/` — 所有任務的軌跡日誌
- `SumoNoteBook/traces/YYYY-MM-DD/` — 按日期組織
- `traces/index.json` — 軌跡索引（供快速查詢）

**資源估算：**
假設每個研究任務產生 ~5KB 的軌跡 JSON：
- 每天 10 個任務 → 50KB/天
- 一年 → ~18MB
- 可接受範圍內

---

## 3. 小模型成本優化

### 3.1 蘇茉家族目前的模型組合

根據 OpenClaw 設定：

| 用途 | 模型 | 說明 |
|------|------|------|
| **主力** | `minimax/MiniMax-M2.7` | 128K context，高效能 |
| **次要** | `minimax/MiniMax-M2` | 小型任務 |
| **本地** | `qwen2.5:3b` | 可能用於特定場景 |

### 3.2 RLM 概念是否能讓小模型做更多事

#### predict-rlm 的發現

> "RLM(GPT-5-mini) outperforms base GPT-5"

這是 RLM 最驚人的發現之一。但需要注意的是：
- 這是在 OpenAI 模型上的測試
- 需要較大的 root LM（如 GPT-5.4）來協調
- 成本節省來自於用 mini 處理大量 sub-task

#### 對蘇茉家族的適用性分析

**不會直接適用的原因：**

1. **架構差異**
   - predict-rlm 需要「較大的 root LM + 較小的 sub-LM」
   - 蘇茉家族主力是 MiniMax-M2.7，沒有更大的模型協調
   - 如果引入 RLM 概念，反而需要更大的模型做 root

2. **任務類型差異**
   - predict-rlm 的強項是「幾乎需處理每一行」的任務（如文件處理）
   - 蘇茉家族的日常任務不一定符合這個模式

3. **成本計算複雜**
   - RLM 的成本節省來自「用小模型替代大模型處理 sub-task」
   - 但增加了 REPL 環境、軌跡記錄等開銷
   - 實際是否節省需要實際測量

#### 潛在應用場景

如果蘇茉家族有多個較小的 sub-task，RLM 概念可能有效：

```python
# 概念示例
class MultiDocAnalyzer(dspy.Signature):
    """分析多個研究文檔並產生綜合報告。
    
    每個文檔用較小的 sub-LM 處理，root LM 負責協調和整合。
    """
    documents: list[File] = dspy.InputField()
    report: str = dspy.OutputField()

# 使用方式
rlm = PredictRLM(
    MultiDocAnalyzer,
    lm="minimax/MiniMax-M2.7",  # root
    sub_lm="qwen2.5:3b"          # sub-LM 用本地小模型
)
```

**風險：** qwen2.5:3b 的能力可能不足以處理複雜的理解任務

### 3.3 具體的 Cost Saving 估算

#### 估算基礎

假設蘇茉家族每天處理：
- 20 個文件分析任務
- 每個任務平均 50 頁 PDF

#### 傳統方式成本

```python
# 全部塞入 context
total_tokens = 20 * 50 * 5000  # 假設每頁 5000 tokens
# = 5,000,000 tokens
# 以 MiniMax 定價計算...
```

#### RLM 方式成本

```python
# 只將 LM 決策相關的資訊放入 context
# 每個 iteration 只有 ~2000 tokens
total_tokens = 20 * 10 * 2000  # 10 iterations per task
# = 400,000 tokens
# 節省約 92%
```

**但注意：**
- sub-LM 的呼叫次數增加
- REPL 環境有額外開銷
- 需要更複雜的錯誤處理

#### 結論

| 場景 | 建議 |
|------|------|
| **檔案分析** | RLM 概念有價值，值得探索 |
| **簡單問答** | 不需要，傳統方式更直接 |
| **長上下文任務** | RLM 概念明確優於傳統 |
| **成本優先** | 需實際測量，不確定 |

---

## 4. 技術整合可行性

### 4.1 現有架構分析

#### OpenClaw

- **語言**：Node.js
- **擴充性**：支援 Python 工具（MCP）、subagent
- **限制**：主要設計為 Node.js-first

#### MCP (Model Context Protocol)

- **用途**：連接外部工具（如 filesystem、GitHub）
- **現有工具**：read、write、exec 等
- **擴充方式**：自訂 MCP 伺服器

#### SumoMemory

- **位置**：`SumoNoteBook/memory/`
- **結構**：基於文件的長期記憶
- **增强點**：Memory Dream 架構

#### SumoNoteBook

- **位置**：`C:\butler_sumo\library\SumoNoteBook\`
- **功能**：知識庫、研究報告、腳本
- **索引**：LanceDB + SQLite

### 4.2 RLM 概念整合方案

#### 架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                     蘇茉家族系統                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    OpenClaw (Node.js)                  │  │
│  │                                                        │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │  │
│  │  │  蘇茉代理   │  │   MCP      │  │  軌跡記錄    │    │  │
│  │  │             │  │  工具層     │  │  模組       │    │  │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │  │
│  └─────────┼──────────────┼───────────────┼────────────┘  │
│            │              │               │               │
│            ▼              ▼               ▼               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              MCP Bridge (Python subprocess)          │   │
│  │                                                       │   │
│  │  - RLM 風格的檔案處理邏輯                             │   │
│  │  - 軌跡記錄與輸出                                    │   │
│  │  - 與 predict-rlm 的概念對齊                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│            ┌─────────────┼─────────────┐                    │
│            ▼             ▼             ▼                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  MiniMax    │  │   檔案系統   │  │  SumoNote   │          │
│  │  API        │  │             │  │  Book       │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

#### 實施策略

**階段 1：軌跡記錄系統（1-2週）**

建立統一的軌跡格式，不改變現有流程：

```javascript
// traces/YYYY-MM-DD/task-{id}.json
{
  "taskId": "research-20260427-001",
  "agent": "professor",
  "startTime": "2026-04-27T10:00:00Z",
  "signature": "AnalyzeDocuments",
  "steps": [
    {
      "iteration": 1,
      "action": "survey_documents",
      "input": {"path": "report.pdf"},
      "output": {"pages": 50, "type": "research_paper"},
      "tokens": 1200,
      "duration_ms": 1500
    },
    {
      "iteration": 2,
      "action": "extract_key_findings",
      "input": {"pages": [1, 5, 10, 15]},
      "output": {"findings": ["...", "..."]},
      "tokens": 3400,
      "duration_ms": 4200
    }
  ],
  "finalOutput": {...},
  "status": "completed"
}
```

**階段 2：文件處理增强（2-4週）**

在 MCP 工具層中新增 RLM 風格的文件處理：

```python
# mcp_tools/document_processor.py
import asyncio
from pathlib import Path

class DocumentProcessor:
    """蘇茉家族的文件處理器，借鑒 RLM 概念"""
    
    async def analyze_pdf(self, path: Path, signature: dict):
        """分析 PDF，模拟 RLM 的 REPL 環境"""
        traces = []
        
        # 步驟 1：Survey
        doc = await self._open_pdf(path)
        survey_result = {
            "pages": len(doc),
            "type": self._guess_type(doc)
        }
        traces.append(self._create_trace("survey", survey_result))
        
        # 步驟 2：LM 決策（通过 MiniMax API）
        pages_to_process = await self._decide_pages(
            survey_result, signature
        )
        
        # 步驟 3：並行提取
        extractions = await asyncio.gather(*[
            self._extract_page(doc, page_num)
            for page_num in pages_to_process
        ])
        
        # 步驟 4：整合與輸出
        final_result = self._merge_extractions(extractions)
        traces.append(self._create_trace("extract", final_result))
        
        return final_result, traces
```

**階段 3：完整 RLM 整合（長期可選）**

如果前兩個階段成功，可考虑：
- 引入 predict-rlm Python 套件
- 建立專門的 Python 服務
- 實現完整的 predict() 和 SUBMIT() 機制

### 4.3 需要修改哪些系統

| 系統 | 修改內容 | 優先級 | 難度 |
|------|---------|--------|------|
| **OpenClaw 配置** | 新增 MCP 工具註冊 | 高 | 低 |
| **軌跡記錄模組** | 新增 `traces/` 目錄和寫入邏輯 | 高 | 低 |
| **MCP 工具層** | 新增文件處理 Python 模組 | 中 | 中 |
| **SumoNoteBook** | 新增 `traces/` 索引 | 中 | 低 |
| **Memory Dream** | 整合軌跡作為記憶來源 | 低 | 高 |
| **預測模型整合** | 引入 predict-rlm 套件 | 低 | 高 |

### 4.4 風險評估

| 風險 | 等級 | 緩解策略 |
|------|------|---------|
| **額外維護成本** | 中 | 階段性實施，先驗證價值再擴展 |
| **Python 環境依賴** | 中 | 確保環境穩定，提供 fallback |
| **過度工程** | 高 | 從軌跡記錄開始，避免一開始就完整 RLM |
| **模型能力不匹配** | 中 | 選擇適合蘇茉家族的 Signature |
| **與現有流程衝突** | 低 | 保持向後兼容，逐步遷移 |

---

## 5. 優先順序建議

### 優先級排序

| 優先級 | 項目 | 理由 | 預期價值 |
|--------|------|------|---------|
| **P0** | 軌跡記錄系統 | 低風險，立即可做 | 高可解釋性 |
| **P1** | 文件處理邏輯增强 | 提升現有能力 | 中等成本節省 |
| **P2** | 與 Memory Dream 整合 | 長期價值 | 高 |
| **P3** | 小模型實驗 | 可選，需測量 | 不確定 |

### 實施時間線

```
Week 1-2:
├── 建立 traces/ 目錄結構
├── 實現基本的 JSON 軌跡格式
└── 在現有任務中添加軌跡記錄

Week 3-4:
├── 開發 document_processor.py
├── 實現基於頁面選擇的 PDF 處理
└── 測試與驗證

Week 5-8:
├── 整合到 MCP 工具層
├── 與 SumoNoteBook 索引整合
└── 性能測量與優化

未來（可選）:
├── 考慮引入完整的 predict-rlm
└── 小模型實驗
```

---

## 6. 風險與限制

### 技術限制

1. **Context Rot 依然存在** — RLM 概念只能緩解，不能完全消除
2. **Python 環境** — OpenClaw 主要 Node.js，需要額外處理
3. **模型能力** — MiniMax-M2.7 未必適合做 RLM 的 root LM

### 營運限制

1. **學習曲線** — 團隊需要理解 RLM 概念
2. **維護成本** — 新增的模組需要維護
3. **複雜度增加** — 系統架構變得更複雜

### 不建議的場景

- 即時性要求極高的簡單查詢
- 資源極度受限的環境
- 沒有明確文件處理需求的場景

---

## 7. 總結

### 核心建議

1. **立即行動**：建立軌跡記錄系統，這是低風險、高價值的改進
2. **中期目標**：增强文件處理邏輯，借鑒 RLM 的頁面選擇策略
3. **長期可選**：考慮完整整合 predict-rlm 或其概念

### 關鍵洞察

- RLM 的核心價值不在於「用小模型替代大模型」，而在於「讓 LM 自己决定如何處理長上下文」
- 軌跡追蹤是蘇茉家族可以立即採用的能力，與現有可解釋性需求高度契合
- 完全整合 predict-rlm 需要較大改動，建议先驗證概念價值

### 下一步行動

1. 在 SumoNoteBook/research/ 中建立 `traces/` 目錄
2. 實現基本的軌跡 JSON 格式
3. 在教授蘇茉的下個研究任務中啟用軌跡記錄

---

## 附錄：預測相關資源

- **predict-rlm GitHub**: https://github.com/Trampoline-AI/predict-rlm
- **論文**: https://arxiv.org/abs/2512.24601v1
- **DSPy**: https://dspy.ai/
- **Pyodide**: https://pyodide.org/

---

*報告完成時間：2026-04-27*  
*研究者：教授蘇茉（先進研究室）*