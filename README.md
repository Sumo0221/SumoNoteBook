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
│   ├── templates\           # 自訂模板
│   ├── daily\               # 每日筆記
│   └── qa\                  # 問答記錄
│
└── scripts\                # 腳本
    ├── daily_organizer.py   # 每日整理（4:12 AM）
    ├── health_check.py      # 健康檢查（5:21 AM）
    ├── query_interface.py  # 強化查詢介面
    └── template_system.py  # 強化模板系統
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

### 查詢知識庫（強化版）

#### 關鍵詞搜詢
```bash
python c:/butler_sumo/library/SumoNoteBook/scripts/query_interface.py "你的問題"
```

#### Dataview 查詢（類 SQL）
```bash
# 列出所有筆記
python c:/butler_sumo/library/SumoNoteBook/scripts/query_interface.py "LIST"

# 表格顯示摘要
python c:/butler_sumo/library/SumoNoteBook/scripts/query_interface.py "TABLE file, mtime, size FROM summaries"

# 條件查詢
python c:/butler_sumo/library/SumoNoteBook/scripts/query_interface.py "LIST WHERE size > 1000"

# 排序和限制
python c:/butler_sumo/library/SumoNoteBook/scripts/query_interface.py "LIST FROM concepts SORT file ASC LIMIT 10"

# 組合查詢
python c:/butler_sumo/library/SumoNoteBook/scripts/query_interface.py "TABLE file, mtime, words FROM summaries WHERE words > 500 SORT mtime DESC LIMIT 5"
```

**支援的查詢語法：**
| 語法 | 說明 |
|------|------|
| `LIST` / `TABLE` | 列表/表格顯示 |
| `FROM <資料夾>` | 指定查詢資料夾（summaries/concepts/qa/raw） |
| `WHERE <條件>` | 條件過濾 |
| `SORT <欄位> <方向>` | 排序（ASC/DESC） |
| `LIMIT <數量>` | 限制結果數量 |

**支援的欄位：**
- `file` - 檔案名
- `path` - 完整路徑
- `ctime` - 建立時間
- `mtime` - 修改時間
- `size` - 檔案大小（位元組）
- `words` - 字數
- `tags` - 標籤
- `links` - 連結數
- `outlinks` - 外部連結數
- `concepts` - 概念

**WHERE 條件支援：**
- `field = "value"` - 等於
- `field != "value"` - 不等於
- `field CONTAINS "value"` - 包含
- `field > <數字>` - 大於
- `field < <數字>` - 小於

### 使用模板系統

```bash
# 列出所有可用模板
python c:/butler_sumo/library/SumoNoteBook/scripts/template_system.py list

# 建立每日筆記
python c:/butler_sumo/library/SumoNoteBook/scripts/template_system.py daily "我的標題"

# 建立會議記錄
python c:/butler_sumo/library/SumoNoteBook/scripts/template_system.py meeting "會議主題" --tags "工作,規劃"

# 從模板建立自訂筆記
python c:/butler_sumo/library/SumoNoteBook/scripts/template_system.py create quick_note "標題" -t "標籤1,標籤2"
```

**內建模板：**
| 模板名 | 說明 |
|--------|------|
| `daily_note` | 每日筆記（含目標、記錄、待辦） |
| `meeting` | 會議記錄（含議程、討論、決議） |
| `reading` | 讀書筆記（含摘要、心得、行動） |
| `project` | 專案筆記（含時間軸、風險、進度） |
| `quick_note` | 快速筆記 |

**模板佔位符：**
- `{{DATE}}` - 當前日期 (2026-04-05)
- `{{TIME}}` - 當前時間 (14:30:25)
- `{{YYYY}}` / `{{MM}}` / `{{DD}}` - 年/月/日
- `{{WEEKDAY}}` - 星期幾
- `{{TITLE}}` - 標題
- `{{TAGS}}` - 標籤
- `{{USER}}` - 使用者名稱
- `{{VAULT}}` - 保險庫名稱

### 程式碼中使用

```python
# 查詢介面
from scripts.query_interface import execute_dataview_query, query

# Dataview 查詢
result = execute_dataview_query('TABLE file, mtime FROM summaries WHERE words > 100')
print(result)

# 關鍵詞搜詢
result = query("python 程式設計")

# 產生 Marp 簡報
from scripts.query_interface import generate_marp_slides
slides = generate_marp_slides("Python 程式設計")
```

```python
# 模板系統
from scripts.template_system import (
    TemplateEngine,
    apply_template,
    create_daily_note,
    create_meeting_note,
    create_quick_note
)

# 套用模板
content = apply_template("今天是 {{DATE}}，標題：{{TITLE}}", title="測試")

# 建立每日筆記
daily = create_daily_note(title="我的每日筆記", tags=["日常"])

# 使用引擎
engine = TemplateEngine()
result = engine.execute("meeting", title="專案會議", tags=["工作"])

# 從模板建立檔案
from scripts.template_system import create_note_from_template
create_note_from_template(
    "project",
    Path("c:/butler_sumo/library/SumoNoteBook/Sumo_wiki/my_project.md"),
    title="新專案",
    description="專案描述"
)
```

## ⏰ 自動排程

建議使用 Windows Task Scheduler 或 cron：

| 時間 | 任務 | 腳本 |
|------|------|------|
| 4:12 AM | 每日整理 | daily_organizer.py |
| 5:21 AM | 健康檢查 | health_check.py |

## 🔧 健康檢查（強化版 v2.0）

健康檢查報告現在包含：

### Vault 統計
- 📄 筆記數量
- 📁 檔案總數
- 📎 附件數量
- 🔗 連結總數
- 🌐 外部連結數
- 📝 總字數
- 💾 總大小
- 📊 檔案類型分布
- 🏷️ 熱門標籤

### 健康檢測
- 🔍 重複內容檢測
- 📄 孤兒筆記檢測（摘要未被引用）
- 🗂️ 孤兒檔案檢測（檔案未被任何筆記引用）
- 🔗 斷裂連結檢測（引用了不存在的檔案）
- ⚠️ 損壞檔案檢測
- 📌 缺失概念檢測

## 🔧 技術特點

- **Obsidian 相容格式**：所有筆記都是標準 Markdown
- **強化查詢介面**：支援類 SQL 的 Dataview 查詢語法
- **強化模板系統**：支援動態內容插入的 Templater 風格模板
- **雙向連結**：每個筆記都有反向連結指向原始資料
- **自動分類**：概念筆記自動建立關聯
- **問答回存**：每次查詢結果都會保存到 wiki
- **Vault 統計**：完整的知識庫統計資訊
- **健康檢查**：自動檢測問題並提供修復建議

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

## 📚 升級說明

### v1.0 → v2.0 更新內容

1. **query_interface.py** - 完全重寫
   - 新增 Dataview 風格查詢語法
   - 支援 LIST/TABLE/WHERE/SORT/LIMIT
   - 支援互動式命令列模式

2. **template_system.py** - 全新功能
   - 5 個內建模板（daily_note, meeting, reading, project, quick_note）
   - 支援動態日期時間變數
   - 支援自訂模板檔案
   - 命令列工具

3. **health_check.py** - 大幅強化
   - 新增 VaultStats 類別
   - 新增孤兒檔案檢測
   - 新增斷裂連結檢測
   - 新增損壞檔案檢測
   - 新增檔案類型統計
   - 新增熱門標籤統計
