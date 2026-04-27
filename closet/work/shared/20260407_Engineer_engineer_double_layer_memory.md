# 雙層記憶存儲系統 (Double-Layer Memory Storage)

## 概述

Hermes 移植計劃的核心組件，專為工程師蘇茉設計的雙層記憶系統。

---

## 雙層結構

### 第一層：技術層 (Technical Facts)
- **Category**: `fact`
- **用途**: 技術細節、命令、工具使用方式、程式碼片段
- **觸發時機**: 完成技術任務、學到新工具、發現問題解法

### 第二層：原則層 (Decision Records)
- **Category**: `decision`
- **用途**: 重要决策、規劃方向、學習心得、架構選擇
- **觸發時機**: 完成重要規劃、收到新規則、架構變更

---

## 記憶記錄格式

### 事實記錄 (Fact)

```markdown
# 事實記錄 (Fact)
- 類型: fact
- 內容: [具體技術內容]
- 時間: [ISO 8601 時間]
- 標籤: [可選標籤]
```

### 決策記錄 (Decision)

```markdown
# 決策記錄 (Decision)
- 類型: decision
- 內容: [決策內容]
- 時間: [ISO 8601 時間]
- 原因: [為什麼做這個決定]
- 影響: [這個決策的影響範圍]
```

---

## 記憶擷取觸發器

### 自動觸發條件

| 任務類型 | 記憶層 | 觸發關鍵字 |
|---------|-------|-----------|
| 完成技術任務 | fact | task_complete, code_written, bug_fixed |
| 工具學習 | fact | tool_learned, skill_mastered |
| 重要決策 | decision | decision_made, architecture_change |
| 規劃完成 | decision | plan_completed, milestone_reached |
| 錯誤學習 | fact + decision | error_learned, mistake_fixed |

### 觸發時機

1. **任務完成時** - 自動存入相關記憶
2. **收到新規則** - 存入 decision 層
3. **學到新技能** - 存入 fact 層
4. **做出重要選擇** - 存入 decision 層

---

## 驗證機制

### 召回測試
- 使用 `memory_recall` 工具測試記憶召回
- 驗證 fact 和 decision 類別記憶可被正確檢索

### 跨 Session 延續
- 所有記憶寫入 `memory/engineer_double_layer_memory.md`
- 每次新 session 載入此檔案內容
- 使用 OpenClaw 的 `memory_recall` 和 `memory_store` 工具

### 測試流程
```
1. 存入測試記憶
2. 等待新 session (或手動觸發召回)
3. 使用 memory_recall 驗證
4. 確認跨 session 記憶延續
```

---

## API / 工具整合

### 使用 memory_recall 召回記憶
```python
memory_recall(query="技術細節", category="fact")
memory_recall(query="決策", category="decision")
```

### 使用 memory_store 存入記憶
```python
memory_store(
    text="記憶內容",
    category="fact"  # 或 "decision"
)
```

### 直接寫入檔案
```python
# 寫入到 engineer_double_layer_memory.md
```

---

## 與現有系統整合

### 與 MEMORY.md 的區別
- **MEMORY.md**: 通用長期記憶，任何 agent 可用
- **engineer_double_layer_memory.md**: 工程師蘇茉專用，包含技術事實和決策分層

### 與 daily notes 的互動
- daily notes 記錄原始事件
- 雙層記憶系統提取重要內容並結構化

---

## 更新記錄

| 日期 | 更新內容 |
|-----|---------|
| 2026-04-03 | 建立雙層記憶系統結構 |

---

## 待辦事項

- [ ] 建立自動記憶擷取腳本
- [ ] 整合到工程師蘇茉的啟動流程
- [ ] 實作驗證測試
