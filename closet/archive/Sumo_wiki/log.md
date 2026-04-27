# 📋 SumoNoteBook 活動日誌

> 按時間排列的 Wiki 活動記錄（Karpathy LLM Wiki 風格）

---

## 📝 格式規範（請遵守）

### 攝入記錄（INGEST）
```markdown
## [YYYY-MM-DD] ingest | 來源標題
- 來源：URL 或檔案路徑
- 概念：[概念1], [概念2], ...
- 新增頁面：page1.md, page2.md
- 更新頁面：page3.md
```

### 查詢記錄（QUERY）
```markdown
## [YYYY-MM-DD] query | 問題摘要
- 使用的頁面：page1.md, page2.md
- 產出：新頁面.md
```

### 健康檢查（LINT）
```markdown
## [YYYY-MM-DD] lint | 健康檢查
- 問題：N 個
- 修復：N 個
- 待處理：M 個
```

### 維護記錄（MAINTENANCE）
```markdown
## [YYYY-MM-DD] maintenance | 維護類型
- 動作：描述
```

---

## 📊 Parser 指令

```bash
# 查看最後 5 個攝入
grep "^## \[" log.md | grep "ingest" | tail -5

# 查看今天的所有活動
grep "^## \[$(date +%Y-%m-%d)\]" log.md

# 查看本週的查詢
grep "^## \[" log.md | grep "query" | tail -10
```

---

## 📜 歷史記錄


## [2026-04-06 23:48] lint | Health Check
- Issues: 1
- Suggestions: 12
- Report: health_report.md


## [2026-04-07 10:05] lint | Health Check
- Issues: 1
- Suggestions: 0
- Report: health_report.md


## [2026-04-07 10:30] lint | Health Check
- Issues: 1
- Suggestions: 0
- Report: health_report.md


## [2026-04-07 10:41] lint | Health Check
- Issues: 0
- Suggestions: 0
- Report: health_report.md


## [2026-04-07 20:27] lint | Health Check
- Issues: 0
- Suggestions: 0
- Report: health_report.md

<!-- AUTO_LOG -->

---

## 📌 重要備註

- 2026-04-06：高工蘇茉建立 SumoNoteBook SOUL.md，定義三層架構
- 2026-04-06：高工蘇茉升級 Lint 流程到 v3.0，新增矛盾檢測
- 2026-04-06：高工蘇茉建立 Obsidian 和 qmd 整合指南

<!-- AUTO_UPDATE -->

---

> 🤖 此檔案遵守 Karpathy LLM Wiki log.md 格式規範