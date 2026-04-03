# 📚 蘇茉圖書館 SumoNoteBook

會自己長大的百科全書

## 📂 目錄結構

```
c:\butler_sumo\library\SumoNoteBook\
├── raw\                    # 原始資料（老爺放這裡）
│   ├── article1.md
│   ├── code.py
│   └── processed\          # 已處理的檔案
│
├── Sumo_wiki\              # 整理好的知識庫（蘇茉維護）
│   ├── index.md            # 總目錄
│   ├── health_report.md    # 健康檢查報告
│   ├── concepts\            # 概念筆記
│   ├── summaries\           # 摘要
│   ├── backlinks\           # 反向連結
│   └── qa\                  # 問答記錄
│
└── scripts\                # 腳本
    ├── daily_organizer.py   # 每日整理（4:12 AM）
    ├── health_check.py      # 健康檢查（5:21 AM）
    └── query_interface.py  # 查詢介面
```

## 🚀 使用方式

### 放置原始資料
將文件丟到 `raw` 資料夾，蘇茉會自動整理。

### 手動執行整理
```bash
python c:/butler_sumo/library/SumoNoteBook/scripts/daily_organizer.py
```

### 手動執行健康檢查
```bash
python c:/butler_sumo/library/SumoNoteBook/scripts/health_check.py
```

### 查詢知識庫
```bash
python c:/butler_sumo/library/SumoNoteBook/scripts/query_interface.py "你的問題"
```

### 查詢並產生簡報
```python
from scripts.query_interface import generate_marp_slides
slides = generate_marp_slides("Python 程式設計")
```

## ⏰ 自動排程

建議使用 Windows Task Scheduler 或 cron：

| 時間 | 任務 | 腳本 |
|------|------|------|
| 4:12 AM | 每日整理 | daily_organizer.py |
| 5:21 AM | 健康檢查 | health_check.py |

## 🔧 技術特點

- **Obsidian 相容格式**：所有筆記都是標準 Markdown
- **雙向連結**：每個筆記都有反向連結指向原始資料
- **自動分類**：概念筆記自動建立關聯
- **問答回存**：每次查詢結果都會保存到 wiki
- **健康檢查**：自動檢測重複、孤兒筆記、斷裂連結

## 📝 筆記格式

### 摘要格式 (summaries/)
```markdown
# 摘要：filename

## 基本資訊
- 原始檔案：filename
- 檔案 ID：abc123
- 建立時間：2026-04-04

## 內容預覽
...

## 概念關鍵詞
...

## 反向連結
> 此摘要由每日整理腳本自動產生
```

### 概念格式 (concepts/)
```markdown
# 概念：concept_name

## 相關檔案
- [[filename1]]
- [[filename2]]

## 建立時間：2026-04-04
```

## 🔗 反向連結格式

每個處理的檔案都會有一個反向連結檔案：
```markdown
# 反向連結：filename

## 檔案 ID：abc123

## 概念關聯
- #python
- #程式設計

## 原始位置
[[../raw/filename]]
```
