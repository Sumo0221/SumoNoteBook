# 工程師蘇茉 - TDD 學習筆記

> 記錄日期：2026-04-03
> 學習目標：掌握 Test-Driven Development (TDD) 測試驅動開發流程

---

## 📚 研究摘要

### TDD 核心概念

**Test-Driven Development (TDD)** 是一種軟體開發方法論，其核心原則是：

> **「先寫測試，再寫程式碼」**

### RED-GREEN-REFACTOR 循環

```
     ┌─────────────────────────────────────┐
     │                                     │
     ▼                                     │
┌─────────┐     ┌─────────┐     ┌─────────┐│
│   RED   │────►│  GREEN  │────►│REFACTOR ││
│ 寫測試   │     │ 讓它通過 │     │  重構   ││
└─────────┘     └─────────┘     └────┬────┘│
                                     │     │
                                     └─────┘
```

#### 1️⃣ RED - 寫一個會失敗的測試
- 先撰寫測試案例
- 測試應該描述功能預期行為
- 此階段測試會失敗（因為還沒有實作）

#### 2️⃣ GREEN - 撰寫最小可行程式碼
- 用最少、最快的辦法讓測試通過
- 可以硬編碼返回值
- 不追求完美，只求通過

#### 3️⃣ REFACTOR - 重構改善程式碼
- 消除重複
- 改善命名和結構
- 保持測試通過

---

## 🔧 在蘇茉家族開發工作中的應用

### 使用情境

當老爺或家族成員提出以下需求時，應用 TDD 流程：

1. **新功能開發** - API、功能模組
2. **Bug 修復** - 先寫測試重現 Bug
3. **重構** - 確保重構不改變行為

### 整合 mini-coding-agent

使用 mini-coding-agent 時指定 TDD 流程：

```
mini_coding_agent(
  task="""使用 TDD 流程開發 [功能]
  
  流程要求：
  1. 先建立 tests/ 目錄和測試檔案
  2. 執行測試確認 RED（失敗）
  3. 撰寫程式碼讓測試通過 GREEN
  4. 重構 REFACTOR
  5. 重複直到完成"""
)
```

### 程式碼範例（Python/pytest）

**步驟 1：寫測試（RED）**
```python
# tests/test_calculator.py
import pytest
from calculator import add

def test_add_two_numbers():
    """兩數相加應該返回正確結果"""
    result = add(2, 3)
    assert result == 5
```

執行結果：🔴 FAILED

**步驟 2：寫程式（GREEN）**
```python
# calculator.py
def add(a, b):
    return a + b
```

執行結果：🟢 PASSED

**步驟 3：重構（REFACTOR）**
```python
# calculator.py
def add(a: int, b: int) -> int:
    """兩數相加並返回結果"""
    return a + b
```

執行結果：🟢 PASSED（仍保持綠燈）

---

## 📁 建議的專案結構

```
project/
├── src/                    # 原始碼
│   └── calculator.py
├── tests/                  # 測試檔案
│   ├── __init__.py
│   └── test_calculator.py
├── pyproject.toml          # 專案配置
└── README.md
```

---

## 💡 整合建議

### 1. 開發流程整合

```
收到需求
    │
    ▼
分析需求 → 撰寫測試（RED）
    │
    ▼
執行測試 → 🔴 失敗
    │
    ▼
撰寫程式（GREEN）→ 🟢 通過
    │
    ▼
重構程式（REFACTOR）→ 🟢 通過
    │
    ▼
完成 ✓
```

### 2. 與老爺的協作

- 收到開發需求時，主動說明將使用 TDD 流程
- 每個功能完成後，展示測試結果
- 重構前先確認老爺需求無誤

### 3. 測試覆蓋範圍

| 類型 | 說明 | 範例 |
|-----|------|------|
| Happy Path | 正常輸入正確輸出 | add(2, 3) == 5 |
| Edge Cases | 邊界條件 | add(0, 0), add(-1, 1) |
| Error Cases | 錯誤處理 | div(1, 0) 應拋例外 |

---

## 📝 蘇茉家族的 TDD 守則

1. **收到開發需求** → 先問老爺是否需要 TDD 流程
2. **嚴格遵守循環** → RED → GREEN → REFACTOR
3. **測試命名清晰** → 描述行為，不模糊
4. **單一職責** → 每個測試只驗證一件事
5. **持續綠燈** → 重構後確保測試仍然通過

---

## 🛠️ 常用工具

- **Python**: pytest, unittest
- **JavaScript**: Jest, Vitest
- **命令列**: `pytest -v` 查看測試結果

---

## 📖 延伸學習

- [Kent Beck - TDD: By Example](https://www.amazon.com/dp/0321146530)
- [Pytest Documentation](https://docs.pytest.org/)
- [Jest Tutorial](https://jestjs.io/docs/tutorial)

---

*筆記建立：2026-04-03*
*下次複習：2026-04-10*
