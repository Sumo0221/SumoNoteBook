"""
蘇茉圖書館 - 強化模板系統
參考 Templater 插件，支援動態內容插入

支援的模板語法：
- {{DATE}}      - 當前日期 (2026-04-05)
- {{TIME}}      - 當前時間 (14:30:25)
- {{YYYY}}      - 年份 (2026)
- {{MM}}        - 月份 (04)
- {{DD}}        - 日期 (05)
- {{HH}}        - 小時 (14)
- {{MIN}}       - 分鐘 (30)
- {{WEEKDAY}}   - 星期幾 (星期一)
- {{TITLE}}     - 標題（可自訂）
- {{FILENAME}}  - 檔案名（可自訂）
- {{TAGS}}      - 標籤（可自訂）
- {{USER}}      - 使用者名稱
- {{VAULT}}     - 保險庫名稱

內建模板：
- daily_note    - 每日筆記模板
- meeting       - 會議記錄模板
- reading       - 讀書筆記模板
- project      - 專案筆記模板

使用範例：
```python
from template_system import TemplateEngine, apply_template, create_daily_note

# 套用模板
content = apply_template("今天是 {{DATE}}，標題：{{TITLE}}", title="測試")

# 建立每日筆記
daily = create_daily_note()

# 使用引擎
engine = TemplateEngine()
result = engine.execute("daily_note", title="我的筆記", tags=["python"])
```

命令列使用：
python template_system.py daily "我的標題"
python template_system.py meeting "會議主題" --tags "工作,規劃"
"""

import os
import re
from pathlib import Path
from datetime import datetime, date
from typing import Dict, Any, Optional, List
import json

# ============================================================================
# 設定
# ============================================================================
WIKI_DIR = Path("c:/butler_sumo/library/SumoNoteBook/Sumo_wiki")
TEMPLATES_DIR = WIKI_DIR / "templates"

# 預設使用者（可從環境變數或設定檔讀取）
DEFAULT_USER = "老爺"
DEFAULT_VAULT = "SumoNoteBook"


# ============================================================================
# 內建模板
# ============================================================================

BUILTIN_TEMPLATES = {
    "daily_note": """---
created: {{DATE}} {{TIME}}
tags: {{TAGS}}
---

# {{TITLE}}

## 今日目標

- [ ] 

## 今日記錄

### 早上


### 下午


### 晚上


## 明日待辦

- 

## 備註


---

*由蘇茉圖書館模板系統自動產生*
""",

    "meeting": """---
created: {{DATE}} {{TIME}}
tags: {{TAGS}}
type: meeting
---

# {{TITLE}}

## 會議資訊
- **日期**：{{DATE}}
- **時間**：{{TIME}}
- **與會者**：{{USER}}

## 議程

1. 

## 討論內容


## 決議事項

1. 

## 待辦事項

| 事項 | 負責人 | 截止日期 |
|------|--------|----------|
|      |        |          |

---

*由蘇茉圖書館模板系統自動產生*
""",

    "reading": """---
created: {{DATE}} {{TIME}}
tags: {{TAGS}}
type: reading
---

# {{TITLE}}

## 書籍資訊
- **閱讀日期**：{{DATE}}
- **類別**：{{CATEGORY}}

## 重點摘要


## 我的心得


## 行動計畫


## 相關筆記
- 

---

*由蘇茉圖書館模板系統自動產生*
""",

    "project": """---
created: {{DATE}} {{TIME}}
tags: {{TAGS}}
type: project
status: planning
---

# {{TITLE}}

## 專案概述
{{DESCRIPTION}}

## 目標
1. 

## 時間軸
- **開始日期**：{{DATE}}
- **預計完成**：

## 資源需求
- 人力：
- 技術：
- 其他：

## 風險評估
| 風險 | 可能性 | 影響 | 對策 |
|------|--------|------|------|
|      |        |      |      |

## 進度追蹤

### Phase 1 - 規劃
- [ ] 

### Phase 2 - 執行
- [ ] 

### Phase 3 - 收尾
- [ ] 

## 相關連結


---

*由蘇茉圖書館模板系統自動產生*
""",

    "quick_note": """---
created: {{DATE}} {{TIME}}
tags: {{TAGS}}
---

# {{TITLE}}

## 內容


## 相關


---

*由蘇茉圖書館模板系統自動產生*
""",
}


# ============================================================================
# 模板引擎
# ============================================================================

class TemplateEngine:
    """模板引擎"""
    
    def __init__(self, custom_dir: Optional[Path] = None):
        self.custom_dir = custom_dir or TEMPLATES_DIR
        self._template_cache: Dict[str, str] = {}
    
    def get_builtin_template(self, name: str) -> Optional[str]:
        """取得內建模板"""
        return BUILTIN_TEMPLATES.get(name.lower())
    
    def get_template(self, name: str) -> Optional[str]:
        """取得模板（先檢查快取，再檢查自訂資料夾，最後檢查內建）"""
        name_lower = name.lower()
        
        # 檢查快取
        if name_lower in self._template_cache:
            return self._template_cache[name_lower]
        
        # 檢查自訂模板
        if self.custom_dir.exists():
            template_file = self.custom_dir / f"{name}.md"
            if template_file.exists():
                try:
                    with open(template_file, "r", encoding="utf-8") as f:
                        content = f.read()
                    self._template_cache[name_lower] = content
                    return content
                except Exception as e:
                    print(f"警告：無法讀取模板 {template_file}: {e}")
        
        # 檢查內建模板
        builtin = self.get_builtin_template(name_lower)
        if builtin:
            self._template_cache[name_lower] = builtin
            return builtin
        
        return None
    
    def list_templates(self) -> Dict[str, str]:
        """列出所有可用模板"""
        templates = {}
        
        # 內建模板
        templates.update({f"builtin:{k}": v[:100] + "..." for k, v in BUILTIN_TEMPLATES.items()})
        
        # 自訂模板
        if self.custom_dir.exists():
            for f in self.custom_dir.glob("*.md"):
                try:
                    with open(f, "r", encoding="utf-8") as file:
                        content = file.read()
                    templates[f"custom:{f.stem}"] = content[:100] + "..."
                except Exception:
                    pass
        
        return templates
    
    def save_custom_template(self, name: str, content: str) -> Path:
        """儲存自訂模板"""
        self.custom_dir.mkdir(parents=True, exist_ok=True)
        template_file = self.custom_dir / f"{name}.md"
        with open(template_file, "w", encoding="utf-8") as f:
            f.write(content)
        self._template_cache[name.lower()] = content
        return template_file
    
    def execute(self, template_name: str, **variables) -> str:
        """
        執行模板
        
        Args:
            template_name: 模板名稱
            **variables: 變數字典
        
        Returns:
            處理後的內容
        """
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"找不到模板：{template_name}")
        
        return apply_template(template, **variables)


# ============================================================================
# 模板應用函數
# ============================================================================

def get_weekday_name(dt: Optional[datetime] = None) -> str:
    """取得星期幾的中文名稱"""
    if dt is None:
        dt = datetime.now()
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return weekdays[dt.weekday()]


def apply_template(template: str, **variables) -> str:
    """
    將模板中的佔位符替換為實際值
    
    Args:
        template: 模板字串
        **variables: 變數值
    
    Returns:
        處理後的字串
    """
    now = variables.pop('datetime', datetime.now())
    if not isinstance(now, datetime):
        now = datetime.now()
    
    # 日期時間相關
    replacements = {
        '{{DATE}}': now.strftime('%Y-%m-%d'),
        '{{TIME}}': now.strftime('%H:%M:%S'),
        '{{YYYY}}': now.strftime('%Y'),
        '{{MM}}': now.strftime('%m'),
        '{{DD}}': now.strftime('%d'),
        '{{HH}}': now.strftime('%H'),
        '{{MIN}}': now.strftime('%M'),
        '{{SS}}': now.strftime('%S'),
        '{{WEEKDAY}}': get_weekday_name(now),
        '{{ISO_DATE}}': now.isoformat(),
    }
    
    # 使用者定義的變數
    user_vars = {
        '{{TITLE}}': variables.get('title', variables.get('TITLE', '無標題')),
        '{{FILENAME}}': variables.get('filename', variables.get('FILENAME', '')),
        '{{TAGS}}': variables.get('tags', variables.get('TAGS', '')),
        '{{USER}}': variables.get('user', variables.get('USER', DEFAULT_USER)),
        '{{VAULT}}': variables.get('vault', variables.get('VAULT', DEFAULT_VAULT)),
        '{{DESCRIPTION}}': variables.get('description', variables.get('DESCRIPTION', '')),
        '{{CATEGORY}}': variables.get('category', variables.get('CATEGORY', '')),
        '{{STATUS}}': variables.get('status', variables.get('STATUS', '')),
    }
    replacements.update(user_vars)
    
    # 處理 TAGS 格式（list -> string）
    if 'tags' in variables and isinstance(variables['tags'], list):
        replacements['{{TAGS}}'] = ','.join(variables['tags'])
        replacements['{{TAGS:ARR}}'] = ' '.join([f'#{t}' for t in variables['tags']])
    else:
        replacements['{{TAGS:ARR}}'] = ''
    
    # 執行替換
    result = template
    for placeholder, value in replacements.items():
        if value is not None:
            result = result.replace(placeholder, str(value))
    
    # 處理未設定的佔位符
    result = re.sub(r'\{\{(\w+)\}\}', '', result)
    
    return result


def create_daily_note(**variables) -> str:
    """建立每日筆記"""
    engine = TemplateEngine()
    return engine.execute("daily_note", **variables)


def create_meeting_note(**variables) -> str:
    """建立會議記錄"""
    engine = TemplateEngine()
    return engine.execute("meeting", **variables)


def create_reading_note(**variables) -> str:
    """建立讀書筆記"""
    engine = TemplateEngine()
    return engine.execute("reading", **variables)


def create_project_note(**variables) -> str:
    """建立專案筆記"""
    engine = TemplateEngine()
    return engine.execute("project", **variables)


def create_quick_note(title: str = "快速筆記", **variables) -> str:
    """建立快速筆記"""
    variables['title'] = title
    engine = TemplateEngine()
    return engine.execute("quick_note", **variables)


# ============================================================================
# 檔案處理
# ============================================================================

def create_note_from_template(
    template_name: str,
    output_path: Path,
    **variables
) -> Path:
    """
    從模板建立筆記檔案
    
    Args:
        template_name: 模板名稱
        output_path: 輸出檔案路徑
        **variables: 變數
    
    Returns:
        建立的檔案路徑
    """
    engine = TemplateEngine()
    content = engine.execute(template_name, **variables)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return output_path


def create_daily_note_file(date_obj: Optional[date] = None, **variables) -> Path:
    """
    建立每日筆記檔案
    
    儲存位置：Sumo_wiki/daily/YYYY-MM-DD.md
    """
    if date_obj is None:
        date_obj = date.today()
    
    daily_dir = WIKI_DIR / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"{date_obj.strftime('%Y-%m-%d')}.md"
    filepath = daily_dir / filename
    
    # 檢查是否已存在
    if filepath.exists() and not variables.get('overwrite', False):
        return filepath
    
    # 設定日期變數
    dt = datetime.combine(date_obj, datetime.now().time())
    variables['datetime'] = dt
    variables.setdefault('title', f"{date_obj.strftime('%Y年%m月%d日')} 每日筆記")
    
    return create_note_from_template("daily_note", filepath, **variables)


# ============================================================================
# 命令列介面
# ============================================================================

def main():
    """命令列主程式"""
    import argparse
    
    parser = argparse.ArgumentParser(description="蘇茉圖書館模板系統")
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='列出所有模板')
    
    # create 命令
    create_parser = subparsers.add_parser('create', help='從模板建立筆記')
    create_parser.add_argument('template', help='模板名稱')
    create_parser.add_argument('title', nargs='?', help='標題')
    create_parser.add_argument('-t', '--tags', help='標籤（逗號分隔）')
    create_parser.add_argument('-o', '--output', help='輸出檔案路徑')
    create_parser.add_argument('--user', help='使用者名稱')
    create_parser.add_argument('--category', help='類別')
    create_parser.add_argument('--description', help='描述')
    
    # daily 命令
    daily_parser = subparsers.add_parser('daily', help='建立每日筆記')
    daily_parser.add_argument('title', nargs='?', help='標題')
    daily_parser.add_argument('-t', '--tags', help='標籤（逗號分隔）')
    daily_parser.add_argument('-d', '--date', help='日期 (YYYY-MM-DD)')
    
    # meeting 命令
    meeting_parser = subparsers.add_parser('meeting', help='建立會議記錄')
    meeting_parser.add_argument('title', nargs='?', help='會議標題')
    meeting_parser.add_argument('-t', '--tags', help='標籤（逗號分隔）')
    
    args = parser.parse_args()
    
    engine = TemplateEngine()
    
    if args.command == 'list':
        print("可用模板：\n")
        templates = engine.list_templates()
        for name, desc in templates.items():
            print(f"  {name}")
            print(f"    {desc}\n")
    
    elif args.command == 'create':
        variables = {}
        if args.title:
            variables['title'] = args.title
        if args.tags:
            variables['tags'] = [t.strip() for t in args.tags.split(',')]
        if args.user:
            variables['user'] = args.user
        if args.category:
            variables['category'] = args.category
        if args.description:
            variables['description'] = args.description
        
        try:
            content = engine.execute(args.template, **variables)
            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"已建立：{output_path}")
            else:
                print(content)
        except ValueError as e:
            print(f"錯誤：{e}")
    
    elif args.command == 'daily':
        variables = {}
        if args.title:
            variables['title'] = args.title
        if args.tags:
            variables['tags'] = [t.strip() for t in args.tags.split(',')]
        
        if args.date:
            from datetime import datetime
            try:
                date_obj = datetime.strptime(args.date, '%Y-%m-%d').date()
            except ValueError:
                print("錯誤：日期格式應為 YYYY-MM-DD")
                return
        else:
            date_obj = None
        
        filepath = create_daily_note_file(date_obj, **variables)
        print(f"已建立每日筆記：{filepath}")
    
    elif args.command == 'meeting':
        variables = {}
        if args.title:
            variables['title'] = args.title
        if args.tags:
            variables['tags'] = [t.strip() for t in args.tags.split(',')]
        
        content = engine.execute('meeting', **variables)
        print(content)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
