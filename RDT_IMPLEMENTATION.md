# SumoNoteBook RDT 實作報告

## 實作完成

### 日期
2026-04-22

### 工程師蘇茉
已完成 SumoNoteBook 的 RDT（Recursive Depth Transformer）概念實作。

---

## 實作內容

### 1. 新增 RDT 迭代深化引擎
在 `query_interface.py` 中新增了 `RDTEngine` 類別，實現：

- **Prelude 階段**: 初始混合搜尋
- **Recurrent Block 階段**: 迭代深化，根據初步結果自動優化查詢
- **Coda 階段**: 整合所有迭代結果，輸出最終答案

### 2. 核心改進
- 新增 `SearchMode.RDT` 搜尋模式
- 新增 `RDTIteration` 和 `RDTResult` 資料結構
- 實現 `_optimize_query()` 方法：從高分結果提取關鍵概念，生成更精確的查詢
- 實現 `_merge_iterations()` 方法：合併多次迭代的結果，給予新迭代更高權重

### 3. 配置參數
```python
CONFIG = {
    "rdt_max_iterations": 3,        # 最大迭代次數
    "rdt_iteration_threshold": 0.7,   # 分數閾值
    "rdt_context_window": 3,        # 上下文窗口
    "rdt_convergence_threshold": 0.05,  # 收斂閾值
}
```

---

## 新功能說明

### 自動模式選擇
- 短查詢 (< 5 字): 使用關鍵詞搜尋
- 中等查詢: 根據內容自動選擇關鍵詞或混合
- 長查詢: 自動啟用 RDT 模式

### 使用方式
```python
from query_interface import search_rdt, natural_search

# RDT 搜尋
result = search_rdt("複雜的查詢問題")

# 自然語言介面
result = natural_search("查詢內容", use_rdt=True)
```

### 命令列
```bash
python query_interface.py --rdt "查詢內容"
```

---

## 驗證結果
- Python 語法檢查：✅ 通過
- 執行測試：✅ 腳本可正常運行
- 引擎狀態：
  - 向量搜尋：需預先建立索引（目前 OFF 是預期的）
  - 關鍵詞搜尋：✅ ON
  - RDT 搜尋：✅ ON