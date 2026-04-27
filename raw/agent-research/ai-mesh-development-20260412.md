# AI Mesh 開發系統研究：用 Skill、YAML 和 MCP 打造 AI 工作系統

> 來源：Shuo-dun Deng Facebook 貼文
> 日期：2026-04-12（21小時前）
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 核心概念：Mesh Architecture

### 傳統做法 vs Mesh 做法

| 傳統做法 | Mesh 做法 |
|----------|-----------|
| 用 prompt 告訴 AI 下一步做什麼 | 用 Flow（project.yaml）定義流程與相依性 |
| 流程是隱性的 | 流程是明確的 |
| 規模變大就不可維護 | 可穩定擴充 |

### 為什麼傳統做法會失敗？
- 當 Skill 越來越多、加入 MCP 串接外部之後：
- 流程變成隱性的
- 相依關係藏在 prompt 裡
- 系統開始變得不可控、不可維護

---

## 🏗️ 四層金字塔架構

```
┌─────────────────────────────────────┐
│ 第一層 Flow                         │
│ project.yaml - 控制順序與回退       │
├─────────────────────────────────────┤
│ 第二層 Task Nodes                   │
│ planner · worker - 執行開發任務     │
├─────────────────────────────────────┤
│ 第三層 System Nodes                 │
│ formatter · evaluator · memory      │
├─────────────────────────────────────┤
│ 第四層 Artifacts                    │
│ specs · builds · reports · memory  │
└─────────────────────────────────────┘
```

---

## 🔄 核心流程

### 基本流程：Planner → Worker → Evaluator

| 節點 | 職責 | 關鍵原則 |
|------|------|----------|
| **planner** | 澄清需求、定義允收標準、拆成任務 | 不碰程式 |
| **worker** | 依據任務實作 | 不定義允收標準 |
| **evaluator** | 逐條比對允收標準 | 不改實作 |

### 進階流程：加入 Formatter

```
Planner → Worker → Formatter → Evaluator
```

**Formatter 的定位**：
- 不是做加工，而是驗證 worker 的產出格式是否正確
- 是 check 前的守門員，格式不對就退回 worker 重做
- 不讓格式問題污染 check 的驗收過程

**為什麼要在 worker 和 evaluator 中間？**
1. 分離「格式檢查」與「內容驗收」
2. 失敗成本不同，該分開處理
3. evaluator 上游必須乾淨
4. 不能放在 evaluator 之後

**Formatter 輸出**：
- `format_valid: true` → 繼續走到 evaluator
- `format_valid: false` → 退回 worker，附上格式錯誤清單

---

## 🔙 失敗回退邏輯

### 三種失敗類型

| 失敗類型 | 回退到 | 原因 |
|----------|--------|------|
| **fail_apply** | worker | 實作層問題 |
| **fail_proposal** | proposal | 提案層問題 |
| **fail_discuss** | discuss | 討論層問題 |

### 為什麼要分開？
- 格式錯誤是 worker 低階失誤，退回 worker 重跑就好
- check 抓到的失敗可能要退到 proposal 甚至 discuss，層級完全不同

---

## 💾 Memory 的關鍵角色

### 為什麼要加 Memory？
- check 完無論 pass 或 fail 都要寫入 memory
- 讓下一輪的 discuss 可以參考歷史
- 哪些允收標準常常 fail
- 哪種需求描述常造成 fail_discuss
- 哪類任務 worker 常做錯
- **沒有 memory，每次開新任務都是第一次，同樣的坑會一直踩**

### Memory 結構（最小版）
```json
{
  "task": "開發任務名稱",
  "input": {
    "user_request": "使用者原始需求",
    "acceptance_criteria": [
      { "id": "AC-01", "description": "允收標準描述", "final_status": "passed | failed" }
    ]
  },
  "output": {
    "verdict": "pass | fail",
    "iterations": 3,
    "failure_history": [
      { "round": 1, "failure_type": "fail_apply", "failed_criteria": ["AC-02"] }
    ],
    "final_result": "實作交付內容摘要"
  },
  "time": "2026-04-11"
}
```

### Memory 在各階段的讀寫

| 階段 | 讀/寫 | 目的 |
|------|--------|------|
| discuss | 讀 | 參考過去類似需求的允收標準 |
| proposal | 讀 | 參考過去同類任務的拆解方式 |
| worker | 讀 | 參考過去類似實作的 failure_history |
| evaluator | 寫 | 不管 pass/fail 都寫入本輪結果 |

---

## 📁 標準目錄結構

```
dev_mesh/
├── project.yaml          # 主控檔（Flow + Routing）
├── nodes/
│   ├── planner.yaml     # 規劃層（discuss + proposal）
│   ├── worker.yaml      # 執行層（apply）
│   ├── formatter.yaml   # 格式守門員
│   └── evaluator.yaml    # 驗收層（check）
├── memory/
│   ├── task_history.json
│   ├── acceptance_criteria_lib/
│   └── failure_patterns/
├── artifacts/
│   ├── specs/
│   ├── builds/
│   ├── format_reports/
│   ├── check_reports/
│   └── _logs/
└── readme/
    ├── FLOW_GUIDE.md
    └── README.md
```

---

## 🔧 System Nodes 白話解釋

| System Node | 功能 |
|-------------|------|
| **Notifier** | 告訴你「做完了」（pass/fail/retry 上限） |
| **Verifier** | 兩層 QA：Formatter（格式）+ Evaluator（內容）|
| **Packager** | 整理成可用的交付物 |
| **Bridge** | 和外部世界溝通（Notion/Slack/外部 DB）|
| **Meta Loop** | 系統自我進化（failure_patterns + retry 升級機制）|

---

## 🤔 Flow 為什麼用 YAML 而不是 Markdown？

### 選 YAML 的理由

1. **關注點分離**：Node 的職責是「做事」，Flow 的職責是「決定誰先做、失敗怎麼回退」。混在一起 Node 就不純了。

2. **Mesh 有失敗回退邏輯，更不能寫在 Node 裡**：evaluator 輸出的不只是 pass/fail，還有 failure_type。如果把回退邏輯寫在 evaluator.yaml 裡，evaluator 就必須知道 planner 和 worker 的存在，耦合度立刻爆炸。

3. **可替換性**：換掉 worker 或新增 reviewer，只改 project.yaml 一個檔，Node 完全不動。

4. **可讀性**：打開 project.yaml 一眼看完整條開發流程和所有回退路徑。

### 結論
> Flow 寫在 project.yaml。尤其像這種有回退邏輯的狀態機，routing 更必須集中管理，否則 Node 之間會互相知道太多，變成「耦合」，整個系統會不可維護。

---

## 備註

discuss proposal apply 是借用高見龍老師的 Spectra 架構

---

*最後更新：2026-04-12*
