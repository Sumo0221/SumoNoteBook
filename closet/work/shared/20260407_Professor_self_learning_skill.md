---
name: self-learning
description: "蘇茉自我學習系統 - 自動分析任務、建議並建立技能。當老爺或蘇茉遇到值得記住的複雜任務模式時，自動建議建立技能。"
metadata:
  openclaw:
    events: ["session:compact:before"]
    emoji: "🤖"
---

# 自我學習技能 (self-learning)

蘇茉的核心能力之一：自動從複雜任務中學習，建立可复用的技能。

## 觸發時機

### 自動觸發（Stop Hook）
- `skill-ask` hook 在每次 `session:compact:before` 時分析對話複雜度
- 複雜度分數 ≥ 0.4 時，自動詢問老爺是否建立技能

### 手動觸發
- 老爺說：「記住這個」、「建立技能」、「下次遇到同樣的任務...」
- 老爺對蘇茉說「你會這項技能嗎？」而蘇茉還沒有

## 技能建立流程

```
[複雜任務完成]
    ↓
[skill-ask hook 注入提示]
    ↓
[蘇茉詢問老爺]
    ↓
[老爺同意]
    ↓
[呼叫 self_learning.py analyze]
    ↓
[呼叫 skill_suggester.py 建立技能檔案]
    ↓
[更新 _registry.md]
    ↓
[完成！]
```

## 快速指令

### 詢問是否建立技能
```bash
python C:\Users\rayray\.openclaw\workspace_engineer\scripts\self_learning.py suggest "<任務描述>"
```

### 匹配現有技能
```bash
python C:\Users\rayray\.openclaw\workspace_engineer\scripts\self_learning.py match "<任務描述>"
```

### 分析並學習
```bash
python C:\Users\rayray\.openclaw\workspace_engineer\scripts\self_learning.py learn --task "<任務>" --result "<結果>"
```

### 互動式建立技能
```bash
python C:\Users\rayray\.openclaw\workspace_engineer\scripts\skill_suggester.py --interactive
```

### 列出所有技能
```bash
python C:\Users\rayray\.openclaw\workspace_engineer\scripts\self_learning.py list
```

## 複雜度評估標準

| 分數 | 等級 | 動作 |
|------|------|------|
| ≥ 0.7 | 高 | 強烈建議建立 |
| 0.5-0.7 | 中 | 建議建立 |
| 0.4-0.5 | 低 | 可選建立 |
| < 0.4 | 極低 | 不建議 |

## 評估維度

1. **任務類型**（+0.35）
   - 關鍵字：分析、研究、實作、開發、建立、創建、實驗

2. **工具多樣性**（+0.30）
   - ≥2 個技術關鍵字時加分

3. **任務長度**（+0.20）
   - >50 字時加分

4. **重複模式**（+0.40）
   - 關鍵字：每次、重複、經常、常常

5. **對話深度**（+0.15）
   - ≥3 條 user 訊息時加分

## 技能存放位置

- **主目錄**：`C:\Users\rayray\.openclaw\workspace_engineer\memory\skills\`
- **類別**：`coding/`, `analysis/`, `research/`, `web/`, `file/`, `tdd/`

## 現有技能

| 技能名稱 | 觸發關鍵字 | 類別 |
|---------|-----------|------|
| mini-claw-code 學習 | mini-claw-code, Rust, coding agent | coding |
| Python 腳本開發 | python, 腳本, 程式, script | coding |
| GitHub 專案分析 | github, 專案, 分析, repo | analysis |
| TDD 測試驅動開發 | tdd, 測試驅動, RED-GREEN-REFACTOR | tdd |

## Stop Hook 狀態

- **Hook 名稱**：`skill-ask`
- **事件**：`session:compact:before`, `session:compact:after`
- **狀態**：✅ 已啟用
- **位置**：`~/.openclaw/hooks/skill-ask/`

## 注意事項

1. 技能建立後，需要重啟 gateway 才能讓 hook 生效
2. 技能查詢使用相似度匹配（threshold 預設 0.3）
3. 若老爺多次拒絕建立，蘇茉會降低詢問頻率
4. 技能註冊表位於 `memory/skills/_registry.md`
