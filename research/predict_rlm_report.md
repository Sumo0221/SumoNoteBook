# predict-rlm 研究報告

**研究目標：** https://github.com/Trampoline-AI/predict-rlm  
**研究日期：** 2026-04-27  
**研究者：** 教授蘇茉

---

## 📋 執行摘要

**predict-rlm** 是基於 MIT CSAIL 論文《Recursive Language Models》(arXiv:2512.24601v1) 實現的開源框架，由 Trampoline AI 團隊開發。其核心創新是將長 prompt 外部化為 Python REPL 環境中的變量，讓 LM 能以程式化方式檢視、分解、遞迴呼叫自己處理任意長度的輸入。這是對抗 **context rot**（上下文腐蝕）與突破 context window 限制的一種新型推理範式。

---

## 1. 技術架構

### 1.1 核心概念：RLM（Recursive Language Model）

RLM 的關鍵洞察是：**長 prompt 不應直接餵入神經網路，而應作為 LM 可以象徵性互動的外部環境一部分**。

傳統做法 vs RLM 做法：

| 傳統做法 | RLM 做法 |
|---------|---------|
| 將完整長上下文全部塞進 LM 的 context window | 將 prompt 作為外部變量，LM 用程式化方式互動 |
| 上下文超過限制時效能急劇下降 | 可處理 10M+ token 規模，效能隨模型改進而提升 |
| 需要人類設計的工具調用流程 | LM 自己決定何時、如何呼叫 sub-LM |

### 1.2 系統架構圖（文字版）

```
┌─────────────────────────────────────────────────────────────┐
│                      PredictRLM                             │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    Root LM (outer)                     │  │
│  │              (e.g., GPT-5.4 / openai/gpt-5.4)          │  │
│  │                                                       │  │
│  │  1. Receives task + signature (inputs/outputs/tools)  │  │
│  │  2. Writes Python code in REPL environment            │  │
│  │  3. Calls predict() for structured sub-LM calls       │  │
│  │  4. Iterates: code → execute → observe → decide      │  │
│  │  5. Calls SUBMIT() with final structured output       │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↕                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Pyodide/WASM Sandbox (REPL)               │  │
│  │                                                       │  │
│  │  - Python 執行環境                                      │  │
│  │  - 狀態在迭代間持久化                                   │  │
│  │  - 支援 asyncio.gather() 並行 sub-LM 呼叫              │  │
│  │  - 可_mount_自訂 modules                               │  │
│  │                                                       │  │
│  │  內建工具：                                            │  │
│  │    predict(signature, **kwargs) → 呼叫 sub-LM          │  │
│  │    SUBMIT(output)           → 結束並輸出結果             │  │
│  │                                                       │  │
│  │  可擴充工具（Skills）：                                 │  │
│  │    - pdf skill: pymupdf 讀取/修改 PDF                  │  │
│  │    - spreadsheet skill: openpyxl 操作 Excel           │  │
│  │    - docx skill: python-docx 操作 Word                │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↕                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   Sub-LM (predict)                    │  │
│  │        (e.g., GPT-5.1 / openai/gpt-5.1)                 │  │
│  │                                                       │  │
│  │  - 處理視覺理解（PDF page images）                      │  │
│  │  - 結構化輸出（dates, entities, tables...）            │  │
│  │  - 可並行多個 predict() 呼叫                           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 DSPy Signature 整合機制

```python
class AnalyzeDocuments(dspy.Signature):
    """Analyze documents and produce a structured report.
    
    1. Survey the documents — file names, page counts, document types
    2. Render pages as images and use predict() to extract content
    3. Produce the report following the criteria's format
    """
    documents: list[File] = dspy.InputField()
    analysis: DocumentAnalysis = dspy.OutputField()
```

Signature 是 RLM 的核心契約：
- **InputField**：定義輸入（可用 `desc` 描述用途）
- **OutputField**：定義輸出結構
- **Docstring**：注入策略指示，告訴 LM 如何處理任務

### 1.4 Root LM 與 Sub-LM 的通訊機制

```
Root LM                          Sub-LM
   │                                 │
   │  1. 根據 Signature 決定輸入結構   │
   │  2. 在 REPL 中執行 Python 程式碼   │
   │  3. 呼叫 predict(signature,      │
   │     instructions, **kwargs)       │
   │  ─────────────────────────────►  │
   │                                 │  (使用 sub_lm 模型處理)
   │  4. 接收結構化輸出 dict           │
   │  ◄─────────────────────────────  │
   │  5. 累加到變量中，繼續迭代         │
```

Sub-LM 是獨立的較小模型（如 GPT-5.1），用於處理特定子任務，可並行多個呼叫。

### 1.5 REPL 的角色

REPL（Read-Eval-Print Loop）是 RLM 的心臟：

- **隔離執行環境**：Pyodide/WASM 沙箱，狀態跨迭代持久
- **狀態累積**：LM 可逐步建立複雜結果，不丟失中間狀態
- **遞迴呼叫支援**：sub-LM 呼叫結果可存入變量，支援長輸出任務
- **程式化推理**：LM 用程式碼（非純 token）操作 context，如同代數運算

---

## 2. 論文分析

### 2.1 Recursive Language Models 論文主要論點

**論文資訊：**
- 作者：Alex L. Zhang, Tim Kraska, Omar Khattab（MIT CSAIL）
- 发布：arXiv:2512.24601v1（2025-12-31）

**核心主張：**
1. **Context Rot 問題**：即使 frontier 模型，隨 context 長度增加，輸出品質也會快速退化
2. **外部化環境**：將長 prompt 從 neural network 外部化為符號環境，LM 用程式碼互動
3. **遞迴呼叫自己**：LM 可在程式中構造子任務，然後遞迴呼叫自己處理
4. **觀察 1**：RLM 可擴展到 10M+ token 規模，成本相當或更低
5. **觀察 2**：Sub-calling 對資訊密集任務（幾乎需處理每行輸入的任務）至關重要
6. **觀察 3**：LM 效能隨 context 長度和任務複雜度退化，RLM 退化較慢
7. **觀察 4**：成本在中等分位數相當，尾端變異性高（因軌跡長度差異）
8. **觀察 5**：不同模型有不同的上下文管理與 sub-calling 策略

**任務類型與複雜度：**
| 任務 | 資訊密度 | 隨長度 scaling |
|------|---------|----------------|
| S-NIAH（大海撈針） | 常數（找固定針） | ~常數 |
| BrowseComp-Plus | 多文件多跳問答 | ~常數文件數 |
| OOLONG | 幾乎需處理每一行 | 線性 |
| OOLONG-Pairs | 需要所有 pair | 二次方 |

### 2.2 與傳統 Agent 框架的區別

| 維度 | Claude Code (傳統 Agent) | RLM (predict-rlm) |
|------|------------------------|-------------------|
| **輸入處理** | 全部塞入 context | 作為外部變量，通過 REPL 程式化存取 |
| **Sub-agent 呼叫** | 人類設計的工作流，每步需顯式發出 | LM 自己決定何時、如何呼叫 sub-LM |
| **Context 限制** | 受限於 context window | 可處理 10M+ token |
| **Context Rot** | 存在，長任務會退化 | 較少，LM 只接觸精選片段 |
| **可解釋性** | 有限，需推理猜測 | 完全可追蹤，每個步驟可見 |
| **任務分解** | 依賴人類預設邏輯 | emergent，模型自己學會分解策略 |
| **長輸出任務** | 受限於 LM 輸出 token 限制 | 可通過變量累積，理論無限制 |

---

## 3. 實際應用

### 3.1 框架適合的場景

1. **文件處理與分析**
   - PDF 分析、發票處理、合同比對
   - 多文件資訊彙總

2. **長上下文任務**
   - 代碼庫理解、文件集合分析
   - 需要「幾乎讀遍每一行」的任務

3. **需要可解釋性的任務**
   - 需要追蹤決策過程的任務
   - 需要稽核軌跡的合規場景

4. **成本敏感場景**
   - 小模型（如 GPT-5-mini）通過 RLM 可超越大模型
   - 選擇何時用 base LM 何時用 RLM

### 3.2 Bitter Lesson-Proof 的實際意義

> "RLMs improve as LMs improve — Unlike harnesses, which can cap or constrain the base model's capabilities, the performance, speed, and cost of RLM calls correlate directly with improvements to base model capabilities."

**Bitter Lesson（苦澀的教訓）**：1990年代以來，AI 進展主要來自利用計算而非人工設計的知識結構。

RLM 的設計哲學：
- **不人為約束**：不像傳統 harness 那樣限制模型能力
- **直接受益於模型改進**：基礎模型變強，RLM 自動變強
- **未來保證**：如果 base model 明天能處理 10M tokens，RLM 就能處理 100M

### 3.3 可解釋性的價值

完整軌跡記錄（`RunTrace`）包含：
- 每個 iteration 的 reasoning、code、output
- 每個 tool call 和 predict call
- Token 使用量和耗時
- 可匯出為 JSON，便於：
  - 稽核決策過程
  - 識別最佳化機會
  - 餵入 GEPA 等工具自動優化 RLM 策略

---

## 4. 程式碼研究

### 4.1 主要模組與類別

```
predict_rlm/
├── PredictRLM          # 主類，擴展 DSPy RLM
│   ├── signature       # DSPy Signature
│   ├── lm             # Root LM
│   ├── sub_lm         # Sub-LM (predict 工具用)
│   ├── max_iterations # 最大 REPL 迭代次數
│   ├── skills         # Skill 清單
│   └── tools          #額外工具函數
│
├── File                # 統一檔案類型
│   ├── path           # 檔案路徑
│   └── from_dir()     # 工廠方法
│
├── Skill               # 可複用技能包
│   ├── name           # 識別名
│   ├── instructions   # 策略指示
│   ├── packages       # PyPI 套件（micropip 安裝）
│   ├── modules        # 自訂 Python modules
│   └── tools          # 工具函數
│
├── RunTrace            # 執行軌跡
│   ├── status         # completed/max_iterations/error
│   ├── steps[]        # 每步 IterationStep
│   └── usage          # Token 使用統計
│
└── skills/
    ├── pdf            # PDF 讀取/渲染
    ├── spreadsheet    # Excel 操作
    └── docx           # Word 文件操作
```

### 4.2 DSPy Signature 定義範例

```python
# 字串格式
rlm = PredictRLM(
    "documents, query -> answer: str",
    lm="openai/gpt-5.4",
    sub_lm="openai/gpt-5.1"
)

# 類格式（推薦，支援豐富描述）
class AnalyzeDocuments(dspy.Signature):
    """Analyze documents and produce a structured report.
    
    1. Survey the documents — file names, page counts, document types
    2. Render pages as images and use predict() to extract content
    3. Produce the report following the criteria's format
    """
    documents: list[File] = dspy.InputField(desc="Input PDF documents")
    analysis: str = dspy.OutputField(desc="Structured briefing report")
```

### 4.3 REPL 的互動流程

```
Iteration 循環：

┌──────────────────────┐
│ LM sees previous     │
│ code output          │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ LM writes Python     │
│ code in REPL         │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Sandbox executes     │
│ code (Pyodide/WASM)  │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ LM sees output,      │
│ decides next step    │
└──────────┬───────────┘
           ▼
     ┌─────┴─────┐
     │ SUBMIT()? │───Yes──► 完成，回傳結果
     └─────┬─────┘
           │No
           ▼
     ┌─────┴─────┐
     │iterations?│───Max──► 回傳 fallback
     └─────┬─────┘
           │More
           ▼
      繼續下一輪
```

---

## 5. 關鍵發現總結

### ✅ 優點

1. **突破 Context Window 限制**：可處理 10M+ token，傳統方法無法企及
2. **Context Rot 抗性**：LM 只接觸精選片段，長任務不易退化
3. **Bitter Lesson-Proof**：效能直接受益於基礎模型改進
4. **完全可解釋**：每個決策步驟皆可追蹤
5. **小模型大作為**：GPT-5-mini 通過 RLM 可超越 base GPT-5
6. **多模態支援**：圖像、音訊、視頻處理
7. **非同步工具呼叫**：WASM 沙箱支援並行呼叫

### ⚠️ 限制 / 注意事項

1. **Sub-LM 之後的遞迴**：目前僅實現一層 sub-LM，未來可能支援多層遞迴
2. **變異性高**：複雜任務的 cost 和 runtime 有較大變異
3. **並非所有任務都需要 RLM**：簡單任務 base LM 可能更好
4. **依賴 Pyodide wheel**：C extension 套件需有 Pyodide 支援

---

## 6. 對蘇茉家族的價值評估

### 評估維度

| 維度 | 分數 | 說明 |
|------|------|------|
| **技術創新性** | ⭐⭐⭐⭐⭐ | 基於 MIT 論文，突破性的推理範式 |
| **實用性** | ⭐⭐⭐⭐ | 適合文件處理、長上下文任務 |
| **與蘇茉家族的契合度** | ⭐⭐⭐ | 可借鑒思路，但需評估整合成本 |
| **可解釋性需求** | ⭐⭐⭐⭐⭐ | 蘇茉家族重視可解釋性，高度契合 |
| **実装成熟度** | ⭐⭐⭐⭐ | 生產就緒，有完整文檔和範例 |

### 具體應用場景

1. **文件分析研究**：蘇茉家族的研究任務常需處理大量文件，RLM 可自動分解、提取
2. **可解釋性需求**：研究過程需要追蹤決策邏輯，軌跡功能完美契合
3. **知識庫建構**：長期記憶與知識庫的資訊整合

### 不建議的場景

- 即時性要求極高的簡單查詢（傳統 API 呼叫更直接）
- 資源極度受限的環境（RLM 有額外開銷）

---

## 7. 與現有方案的比較

| 方案 | Context 處理 | 任務分解 | 可解釋性 | 成本效率 | 適用場景 |
|------|-------------|---------|---------|---------|---------|
| **predict-rlm (RLM)** | 外部化，10M+ | 模型自發 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 長上下文、文件處理 |
| **Claude Code** | 全部塞入 | 人類設計 | ⭐⭐⭐ | ⭐⭐⭐ | 程式開發、日常任務 |
| **Context Compression** | 壓縮 | 被動壓縮 | ⭐⭐ | ⭐⭐⭐ | 簡單摘要任務 |
| **Retrieval Agent** | 檢索 | 被動檢索 | ⭐⭐ | ⭐⭐⭐ | 知識檢索場景 |
| **CodeAct Agent** | 全部塞入 | 人類設計 | ⭐⭐⭐ | ⭐⭐ | 程式執行任務 |

---

## 📚 參考資源

- **GitHub 專案**：https://github.com/Trampoline-AI/predict-rlm
- **論文**：https://arxiv.org/abs/2512.24601v1
- **Pyodide**：https://pyodide.org/
- **DSPy**：https://dspy.ai/

---

*報告完成時間：2026-04-27*  
*研究者：教授蘇茉（先進研究室）*
