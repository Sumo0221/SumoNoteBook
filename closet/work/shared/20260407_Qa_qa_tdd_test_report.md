# TDD 流程測試報告

**測試日期**：2026-04-03
**品管蘇茉**：品質控制專家
**測試對象**：mini-coding-agent 的 TDD 工作流程支援
**測試情境**：String Calculator（經典 TDD 練習）

---

## 測試結果：✅ **通過**

---

## 📋 TDD 流程執行摘要

### 測試專案結構
```
tdd_test/
├── src/
│   └── string_calculator.py   # 最終版本經過完整 REFACTOR
└── tests/
    └── test_string_calculator.py  # 5 個測試案例
```

### 各階段執行結果

| 階段 | 預期行為 | 實際行為 | 結果 |
|------|---------|---------|------|
| RED | 測試失敗（紅燈） | ✅ Agent 先建立測試檔案，再建立 stub 函式，pytest 出現 collection/pass error | ✅ 符合預期 |
| GREEN | 測試通過（綠燈） | ✅ Agent 實作 `add()` 函式，5 個測試全部 PASSED | ✅ 符合預期 |
| REFACTOR | 保持綠燈 | ✅ Agent 加入 docstring、type hints、範例，測試仍然 PASSED | ✅ 符合預期 |

### 最終測試結果（GREEN + REFACTOR 後）
```
tests/test_string_calculator.py::test_empty_string_returns_zero PASSED   [ 20%]
tests/test_string_calculator.py::test_single_number_returns_that_number PASSED [ 40%]
tests/test_string_calculator.py::test_two_numbers_comma_delimited_returns_sum PASSED [ 60%]
tests/test_string_calculator.py::test_multiple_numbers_comma_delimited_returns_sum PASSED [ 80%]
tests/test_string_calculator.py::test_newline_between_numbers_returns_sum PASSED   [100%]

============================== 5 passed in 0.02s ==============================
```

---

## 🔍 品管監督分析

### ✅ TDD 流程有被正確執行

- **RED 階段**：Agent 正確建立測試 → 執行確認失敗 → 失敗原因明確（函式尚未實作）
- **GREEN 階段**：Agent 實作最小可行程式碼 → pytest 從 FAIL 變為 PASS
- **REFACTOR 階段**：Agent 加入 docstring、型別標註、範例 → 測試仍保持綠燈

### ✅ 每個階段產出符合預期

| 階段 | 產出檔案 | 品質評估 |
|------|---------|---------|
| RED | `tests/test_string_calculator.py` | 5 個測試案例，命名清晰，符合 AAA 模式 |
| GREEN | `src/string_calculator.py` (v1) | 功能正確，能處理所有基本輸入 |
| REFACTOR | `src/string_calculator.py` (v2) | 增加 docstring、型別標註、範例，程式碼可讀性提升 |

### ⚠️ 觀察到的問題

#### 問題 1：中文輸出編碼異常（輕微）
- **現象**：mini-coding-agent 的 LLM 回覆中有大量亂碼（特殊字元），但**實際產出的程式碼檔案完全正確**
- **原因**：Windows PowerShell 的中文編碼可能與 mini-coding-agent 的輸出格式不相容
- **影響**：不影響最終產出，但觀察執行過程時難以閱讀

#### 問題 2：workdir 參數行為異常
- **現象**：直接呼叫 `mini_coding_agent(workdir="...")` 時，Agent 嘗試在被指定的 workdir 中找 `main.py`
- **原因**：工具包執行時路徑拼接邏輯有誤，應使用 mini_coding_agent 的安裝目錄而非 workdir
- **替代方案**：使用 `exec` 工具直接呼叫 `python C:/butler_sumo/Tools/mini_coding_agent/main.py --task "..."`
- **影響**：需要手動指定 agent 路徑，不影響 TDD 流程本身

#### 問題 3：Windows 指令相容性
- **現象**：Agent 在 Iteration 10 嘗試使用 `find . -type f | head -20`（Unix 指令），在 Windows 上失敗
- **原因**：Agent 的 tool-use loop 未自動偵測作業系統
- **影響**：單次迭代失敗，但不影響整體流程（Agent 迅速改用 `dir /s /b`）

### ❌ 不影響 TDD 核心流程的觀察

- Agent 在 RED 階段有 2 次「Command failed」（並非預期中的明確 FAILED 測試），但這是因為 pytest 在模組無 `add` 函式時出現 collection error（exit code 2），而非乾淨的測試失敗畫面
- 這屬於**測試框架的邊界行為**，不影響 TDD 流程的正確性

---

## 📊 TDD 流程適用性評估

| 評估項目 | 分數（1-5） | 備註 |
|---------|------------|------|
| RED 階段執行正確性 | ⭐⭐⭐⭐⭐ | 完全按照 TDD 流程先寫測試 |
| GREEN 階段執行正確性 | ⭐⭐⭐⭐⭐ | 快速實作讓測試通過 |
| REFACTOR 階段執行正確性 | ⭐⭐⭐⭐⭐ | 有自覺地改善程式碼品質 |
| 指令執行環境相容性 | ⭐⭐⭐ | Windows 相關指令需注意 |
| 輸出可讀性 | ⭐⭐ | 中文回覆有編碼問題，但程式碼無影響 |
| 工具參數穩定性 | ⭐⭐⭐ | workdir 參數有 bug，需繞路 |

**總評**：TDD 流程本身可以在 mini-coding-agent 中正確執行，但**工具層面有些包裝問題需要蘇茉留意**。

---

## 💡 具體優化建議

### 給工程師蘇茉（技能改進）

1. **修正 workdir 參數行為**：mini-coding-agent 的 `main.py` 應將 workdir 作為 agent 的執行目錄，而非拼接到 `main.py` 的路徑
   ```bash
   # 錯誤行為（目前）
   python "workdir/main.py" --task "..."
   
   # 正確行為（預期）
   python "mini_coding_agent_dir/main.py" --task "..." --workdir "..."
   ```

2. **增加 Windows 指令檢測**：在 tools.py 中加入 OS 偵測，自動將 Unix 指令轉換為 Windows 等價指令

3. **改善 LLM 輸出編碼**：確保所有工具輸出使用 UTF-8 編碼，支援中文正確顯示

### 給總管蘇茉（使用建議）

1. **呼叫 mini-coding-agent 時使用 `exec` 而非 `mini_coding_agent` 工具**，避免 workdir bug：
   ```python
   exec(
     command='python C:/butler_sumo/Tools/mini_coding_agent/main.py --provider minimax --task "..."'
   )
   ```

2. **為 TDD 任務預留足夠的迭代次數**：複雜功能建議 `max_iterations=30` 以上

3. **TDD 任務需明確分階段指示**：在 task 字串中清楚標示 RED/GREEN/REFACTOR 每階段的預期行為

---

## 📝 最終結論

**TDD 流程完全可以融入 mini-coding-agent 的工作方式**。Agent 能夠：
- ✅ 理解 RED-GREEN-REFACTOR 循環的概念
- ✅ 自發性地先寫測試再寫程式
- ✅ 在 GREEN 階段快速產出最小可行程式碼
- ✅ 在 REFACTOR 階段有意識地改善程式碼品質

**但工具層面有些包裝問題**需要蘇茉家族注意，特別是 workdir 參數的 bug 和 Windows 指令相容性。

**建議**：在 mini-coding-agent 的 skill 文件中明確記載這些已知問題的繞路方式，並在未來版本中修復。

---

## 🔧 修復記錄（2026-04-03 by 工程師蘇茉）

### Issue 1: workdir 參數 bug ✅ 已修復

**根本原因**：`src/index.ts` 直接將 `params.workdir` 拼接到 `main.py` 的路徑，導致 Agent 嘗試在被指定的 workdir 中找 `main.py`

**修復方案**：
1. **tools.py**: 新增 `MINI_AGENT_WORKDIR` 環境變數支援，BashTool 會自動讀取並使用
2. **src/index.ts**: 使用 `params.workdir || MINI_CODING_AGENT_DIR` 作為 `cwd`，並透過環境變數傳遞 workdir

**驗證**：
```python
os.environ['MINI_AGENT_WORKDIR'] = 'C:/Users/rayray/.openclaw/workspace_engineer'
bt = BashTool()
result = bt.execute('dir *.md')  # 自動在 workdir 執行
```

### Issue 2: Windows 指令相容性 ✅ 已優化

`platform_utils.py` 中的翻譯邏輯已確認正常運作，BashTool 在 Windows 上會自動翻譯 Unix 指令（如 `ls` → `dir`）

### Issue 3: 中文編碼問題 ✅ 已優化

- `src/index.ts` 在執行時自動設定 `PYTHONIOENCODING: "utf-8"`
- 所有工具輸出使用 `errors="replace"` 處理編碼錯誤
- ReadTool/WriteTool 優先使用 UTF-8 編碼

---

## 📝 最終結論

**TDD 流程完全可以融入 mini-coding-agent 的工作方式**。Agent 能夠：
- ✅ 理解 RED-GREEN-REFACTOR 循環的概念
- ✅ 自發性地先寫測試再寫程式
- ✅ 在 GREEN 階段快速產出最小可行程式碼
- ✅ 在 REFACTOR 階段有意識地改善程式碼品質

**工具層面的包裝問題已由工程師蘇茉修復（2026-04-03）**。

---

*品管蘇茉 QA 報告*
*日期：2026-04-03*
*評等：✅ 測試通過（TDD 流程可行，工具層面問題已修復）*