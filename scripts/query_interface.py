"""
蘇茉圖書館 - 強化查詢介面
參考 Dataview 的查詢語法，支援類 SQL 的筆記查詢

支援的查詢語法：
- LIST [欄位...] [FROM <資料夾>] [WHERE <條件>] [SORT <欄位> <方向>] [LIMIT <數量>]
- TABLE [欄位...] [FROM <資料夾>] [WHERE <條件>] [SORT <欄位> <方向>] [LIMIT <數量>]

WHERE 條件支援：
- field = "value"  (等於)
- field != "value" (不等於)
- field CONTAINS "value" (包含)
- field > <number> (大於)
- field < <number> (小於)

範例：
- LIST FROM "concepts"
- TABLE file, mtime FROM "summaries" WHERE mtime > 2026-01-01 SORT mtime DESC LIMIT 10
- LIST WHERE size > 1000
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

# ============================================================================
# 設定
# ============================================================================
WIKI_DIR = Path("c:/butler_sumo/library/SumoNoteBook/Sumo_wiki")
RAW_DIR = Path("c:/butler_sumo/library/SumoNoteBook/raw")
SUMMARIES_DIR = WIKI_DIR / "summaries"
CONCEPTS_DIR = WIKI_DIR / "concepts"
BACKLINKS_DIR = WIKI_DIR / "backlinks"
QA_DIR = WIKI_DIR / "qa"


# ============================================================================
# 查詢引擎
# ============================================================================

class Note:
    """筆記物件，代表一個筆記檔案"""
    def __init__(self, filepath: Path):
        self.path = Path(filepath)
        self.file = self.path.stem  # 檔案名（不含副檔名）
        self.name = self.path.name   # 完整檔案名
        self.ext = self.path.suffix  # 副檔名
        
        # 檔案屬性
        stat = self.path.stat()
        self.ctime = datetime.fromtimestamp(stat.st_ctime)
        self.mtime = datetime.fromtimestamp(stat.st_mtime)
        self.size = stat.st_size  # 位元組
        
        # 內容屬性
        self._content = None
        self._tags = None
        self._links = None
        self._outlinks = None
        self._words = None
    
    @property
    def content(self) -> str:
        """延遲載入內容"""
        if self._content is None:
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self._content = f.read()
            except Exception:
                self._content = ""
        return self._content
    
    @property
    def tags(self) -> List[str]:
        """從內容中提取標籤"""
        if self._tags is None:
            # 匹配 #標籤 格式
            self._tags = re.findall(r'#([a-zA-Z\u4e00-\u9fff_]+)', self.content)
        return self._tags
    
    @property
    def links(self) -> List[str]:
        """從內容中提取所有連結（巢狀連結）"""
        if self._links is None:
            # 匹配 [[連結]] 格式
            self._links = re.findall(r'\[\[([^\]]+)\]\]', self.content)
        return self._links
    
    @property
    def outlinks(self) -> List[str]:
        """提取外部連結（http/https）"""
        if self._outlinks is None:
            self._outlinks = re.findall(r'https?://[^\s\)\"\'\]]+', self.content)
        return self._outlinks
    
    @property
    def words(self) -> int:
        """計算字數"""
        if self._words is None:
            # 移除 Markdown 語法後計算
            clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', self.content)  # [文字](連結) -> 文字
            clean = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', clean)  # 圖片
            clean = re.sub(r'[#*`_\[\]{}|\\]', '', clean)  # Markdown 符號
            clean = re.sub(r'<[^>]+>', '', clean)  # HTML 標籤
            self._words = len(clean.strip())
        return self._words
    
    @property
    def concepts(self) -> List[str]:
        """提取概念標籤（來自路徑/concepts/）"""
        if 'concepts' in self.path.parts:
            return [self.file]
        return []
    
    def get_field(self, field: str) -> Any:
        """取得指定欄位的值"""
        field = field.lower().strip()
        
        # 基本欄位
        if field in ('file', 'name', 'filename'):
            return self.name
        elif field == 'path':
            return str(self.path)
        elif field == 'ctime':
            return self.ctime
        elif field == 'mtime':
            return self.mtime
        elif field == 'size':
            return self.size
        elif field == 'words':
            return self.words
        elif field == 'tags':
            return ', '.join(self.tags) if self.tags else ''
        elif field == 'links':
            return len(self.links)
        elif field == 'outlinks':
            return len(self.outlinks)
        elif field == 'concepts':
            return ', '.join(self.concepts) if self.concepts else ''
        elif field == 'ext':
            return self.ext
        else:
            return None
    
    def to_dict(self, fields: List[str]) -> Dict[str, Any]:
        """轉換為字典"""
        result = {}
        for f in fields:
            val = self.get_field(f)
            if isinstance(val, datetime):
                result[f] = val.strftime('%Y-%m-%d %H:%M')
            elif val is None:
                result[f] = ''
            else:
                result[f] = val
        return result


class QueryEngine:
    """查詢引擎"""
    
    def __init__(self):
        self.notes: List[Note] = []
        self._load_notes()
    
    def _load_notes(self):
        """載入所有筆記"""
        self.notes = []
        
        # 掃描所有資料夾
        for note_dir in [SUMMARIES_DIR, CONCEPTS_DIR, QA_DIR, RAW_DIR]:
            if note_dir.exists():
                for f in note_dir.glob("*.md"):
                    try:
                        self.notes.append(Note(f))
                    except Exception as e:
                        print(f"警告：無法載入 {f}: {e}")
    
    def query(self, query_str: str) -> Tuple[str, List[Dict]]:
        """
        執行查詢
        
        支援語法：
        - LIST [欄位...] [FROM <資料夾>] [WHERE <條件>] [SORT <欄位> <方向>] [LIMIT <數量>]
        - TABLE [欄位...] [FROM <資料夾>] [WHERE <條件>] [SORT <欄位> <方向>] [LIMIT <數量>]
        
        範例：
        - LIST
        - TABLE file, mtime, size FROM "summaries"
        - LIST WHERE size > 1000 SORT size DESC
        - LIST FROM "concepts" WHERE tags CONTAINS "python" LIMIT 5
        """
        query_str = query_str.strip()
        if not query_str:
            return self._format_list(['file', 'path', 'mtime'], self.notes)
        
        # 解析查詢
        cmd, fields, where_filter, sort_field, sort_dir, limit, from_folder = self._parse_query(query_str)
        
        # 過濾資料夾
        results = self.notes
        if from_folder:
            folder_map = {
                'summaries': SUMMARIES_DIR,
                'concepts': CONCEPTS_DIR,
                'qa': QA_DIR,
                'raw': RAW_DIR,
                'backlinks': BACKLINKS_DIR,
            }
            target_dir = folder_map.get(from_folder.lower())
            if target_dir:
                results = [n for n in results if n.path.is_relative_to(target_dir)]
        
        # 預設欄位
        if not fields:
            fields = ['file', 'path', 'mtime'] if cmd == 'TABLE' else ['file']
        
        # WHERE 過濾
        if where_filter:
            results = self._apply_where(results, where_filter)
        
        # SORT 排序
        if sort_field:
            results = self._apply_sort(results, sort_field, sort_dir)
        
        # LIMIT 限制
        if limit:
            results = results[:limit]
        
        # 格式化輸出
        if cmd == 'TABLE':
            return self._format_table(fields, results)
        else:
            return self._format_list(fields, results)
    
    def _parse_query(self, query_str: str) -> Tuple:
        """解析查詢字串"""
        cmd = 'LIST'  # 預設命令
        fields = []
        where_filter = None
        sort_field = None
        sort_dir = 'ASC'
        limit = None
        from_folder = None
        
        # 轉小句處理
        upper = query_str.upper()
        
        # 判斷命令
        if upper.startswith('TABLE'):
            cmd = 'TABLE'
            query_str = query_str[5:].strip()
        elif upper.startswith('LIST'):
            cmd = 'LIST'
            query_str = query_str[4:].strip()
        
        # 解析 FROM
        from_match = re.search(r'FROM\s+"([^"]+)"', query_str, re.IGNORECASE)
        if from_match:
            from_folder = from_match.group(1)
            query_str = query_str[:from_match.start()] + query_str[from_match.end():]
        
        # 解析 WHERE
        where_match = re.search(r'WHERE\s+(.+?)(?=\s+SORT|\s+LIMIT|$)', query_str, re.IGNORECASE)
        if where_match:
            where_filter = where_match.group(1).strip()
            query_str = query_str[:where_match.start()] + query_str[where_match.end():]
        
        # 解析 SORT
        sort_match = re.search(r'SORT\s+(\w+)\s*(DESC|ASC)?', query_str, re.IGNORECASE)
        if sort_match:
            sort_field = sort_match.group(1).lower()
            sort_dir = sort_match.group(2) or 'ASC'
            query_str = query_str[:sort_match.start()] + query_str[sort_match.end():]
        
        # 解析 LIMIT
        limit_match = re.search(r'LIMIT\s+(\d+)', query_str, re.IGNORECASE)
        if limit_match:
            limit = int(limit_match.group(1))
            query_str = query_str[:limit_match.start()] + query_str[limit_match.end():]
        
        # 剩餘的當作欄位列表
        remaining = query_str.strip()
        if remaining:
            # 分割欄位（逗號分隔）
            fields = [f.strip().lower() for f in remaining.split(',') if f.strip()]
        
        return cmd, fields, where_filter, sort_field, sort_dir, limit, from_folder
    
    def _apply_where(self, notes: List[Note], where_filter: str) -> List[Note]:
        """應用 WHERE 條件過濾"""
        filtered = []
        
        for note in notes:
            if self._evaluate_condition(note, where_filter):
                filtered.append(note)
        
        return filtered
    
    def _evaluate_condition(self, note: Note, condition: str) -> bool:
        """評估單一條件"""
        condition = condition.strip()
        
        # 處理 CONTAINS
        contains_match = re.match(r'(\w+)\s+CONTAINS\s+"([^"]+)"', condition, re.IGNORECASE)
        if contains_match:
            field = contains_match.group(1).lower()
            value = contains_match.group(2).lower()
            field_val = note.get_field(field)
            if field_val is None:
                return False
            return value in str(field_val).lower()
        
        # 處理 !=
        ne_match = re.match(r'(\w+)\s*!=\s*"([^"]+)"', condition, re.IGNORECASE)
        if ne_match:
            field = ne_match.group(1).lower()
            value = ne_match.group(2)
            field_val = note.get_field(field)
            if field_val is None:
                return False
            return str(field_val) != value
        
        # 處理 =
        eq_match = re.match(r'(\w+)\s*=\s*"([^"]+)"', condition, re.IGNORECASE)
        if eq_match:
            field = eq_match.group(1).lower()
            value = eq_match.group(2)
            field_val = note.get_field(field)
            if field_val is None:
                return False
            return str(field_val) == value
        
        # 處理 > (數值比較)
        gt_match = re.match(r'(\w+)\s*>\s*(\d+(?:\.\d+)?)', condition, re.IGNORECASE)
        if gt_match:
            field = gt_match.group(1).lower()
            value = float(gt_match.group(2))
            field_val = note.get_field(field)
            if field_val is None:
                return False
            try:
                return float(field_val) > value
            except (ValueError, TypeError):
                return False
        
        # 處理 < (數值比較)
        lt_match = re.match(r'(\w+)\s*<\s*(\d+(?:\.\d+)?)', condition, re.IGNORECASE)
        if lt_match:
            field = lt_match.group(1).lower()
            value = float(lt_match.group(2))
            field_val = note.get_field(field)
            if field_val is None:
                return False
            try:
                return float(field_val) < value
            except (ValueError, TypeError):
                return False
        
        # 預設：檢查任何欄位是否包含條件文字
        for field in ['file', 'path', 'tags', 'concepts']:
            val = note.get_field(field)
            if val and condition.lower() in str(val).lower():
                return True
        
        return False
    
    def _apply_sort(self, notes: List[Note], sort_field: str, sort_dir: str) -> List[Note]:
        """應用排序"""
        reverse = sort_dir.upper() == 'DESC'
        
        def get_sort_key(note: Note):
            val = note.get_field(sort_field)
            if val is None:
                return '' if not reverse else '\uffff'
            if isinstance(val, datetime):
                return val
            if isinstance(val, (int, float)):
                return val
            return str(val)
        
        try:
            return sorted(notes, key=get_sort_key, reverse=reverse)
        except Exception:
            return notes
    
    def _format_list(self, fields: List[str], notes: List[Note]) -> Tuple[str, List[Dict]]:
        """格式化 LIST 輸出"""
        results = []
        for note in notes:
            results.append(note.to_dict(fields))
        return "list", results
    
    def _format_table(self, fields: List[str], notes: List[Note]) -> Tuple[str, List[Dict]]:
        """格式化 TABLE 輸出"""
        results = []
        for note in notes:
            results.append(note.to_dict(fields))
        return "table", results


# ============================================================================
# 輸出格式化
# ============================================================================

def format_as_markdown(output_type: str, fields: List[str], results: List[Dict]) -> str:
    """格式化為 Markdown"""
    if not results:
        return "_查無結果_"
    
    lines = []
    
    if output_type == 'table' and fields:
        # 表格標題
        header = ' | '.join(fields)
        separator = ' | '.join(['---'] * len(fields))
        lines.append(f"| {header} |")
        lines.append(f"| {separator} |")
        
        # 資料列
        for row in results:
            row_vals = []
            for f in fields:
                val = row.get(f, '')
                # 處理換行
                val = str(val).replace('\n', ' ')[:100]
                row_vals.append(val)
            lines.append(f"| {' | '.join(row_vals)} |")
    else:
        # 列表格式
        for row in results:
            if 'file' in row:
                lines.append(f"- **{row['file']}**")
                for f in fields:
                    if f != 'file' and row.get(f):
                        lines.append(f"  - {f}: {row[f]}")
            elif fields:
                first_field = fields[0]
                lines.append(f"- {row.get(first_field, '')}")
    
    return '\n'.join(lines)


def format_as_text(output_type: str, fields: List[str], results: List[Dict]) -> str:
    """格式化為純文字"""
    if not results:
        return "查無結果"
    
    lines = []
    
    if output_type == 'table':
        col_widths = {}
        for f in fields:
            col_widths[f] = len(f)
        
        for row in results:
            for f in fields:
                val = str(row.get(f, ''))[:30]
                col_widths[f] = max(col_widths[f], len(val))
        
        # 標題列
        header = '  '.join(f.ljust(col_widths[f]) for f in fields)
        lines.append(header)
        lines.append('-' * len(header))
        
        # 資料列
        for row in results:
            row_str = '  '.join(str(row.get(f, ''))[:col_widths[f]].ljust(col_widths[f]) for f in fields)
            lines.append(row_str)
    else:
        for i, row in enumerate(results, 1):
            if 'file' in row:
                lines.append(f"{i}. {row['file']}")
            elif fields:
                lines.append(f"{i}. {row.get(fields[0], '')}")
    
    return '\n'.join(lines)


# ============================================================================
# 問答整合
# ============================================================================

def search_in_file(filename: str, keywords: List[str]) -> List[str]:
    """在檔案中搜尋關鍵字"""
    filepath = SUMMARIES_DIR / filename
    if not filepath.exists():
        return []
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    results = []
    for kw in keywords:
        if kw.lower() in content.lower():
            results.append(kw)
    return results


def search_all(keywords: List[str]) -> List[Dict]:
    """搜尋所有摘要"""
    results = []
    for f in SUMMARIES_DIR.glob("*.md"):
        matched = search_in_file(f.name, keywords)
        if matched:
            with open(f, "r", encoding="utf-8") as file:
                content = file.read()
            results.append({
                "file": f.name,
                "matched": matched,
                "preview": content[:300]
            })
    return results


def save_qa_result(question: str, answer: str, related_files: List[str]) -> str:
    """將問答結果回存到 wiki"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    qa_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    qa_content = f"""# Q&A：{question[:50]}{"..." if len(question) > 50 else ""}

## 問題
{question}

## 回答
{answer}

## 相關檔案
{"".join([f"- [[{f}]]" for f in related_files]) if related_files else "- 無直接相關檔案"}

## 查詢時間：{now}

---
*此問答由 [查詢介面](../scripts/query_interface.py) 自動產生*
"""
    
    qa_file = QA_DIR / f"{qa_id}.md"
    qa_file.parent.mkdir(parents=True, exist_ok=True)
    with open(qa_file, "w", encoding="utf-8") as f:
        f.write(qa_content)
    
    return qa_file.name


def query(question: str) -> Dict:
    """查詢入口（關鍵詞搜尋）"""
    # 提取關鍵詞
    keywords = [w.strip(".,!?()[]{}:;\"'") for w in question.split() if len(w) > 2]
    keywords = [k for k in keywords if k.lower() not in ["什麼", "如何", "怎麼", "為什麼", "哪個", "這個", "那個", "可以", "會", "是", "有", "在"]][:10]
    
    print(f"關鍵詞：{keywords}")
    
    # 搜尋
    results = search_all(keywords)
    
    answer_parts = []
    related_files = []
    
    if results:
        answer_parts.append(f"在知識庫中找到 {len(results)} 個相關筆記：\n")
        for r in results[:5]:
            answer_parts.append(f"- **{r['file']}**：符合 \"{', '.join(r['matched'])}\"\n  {r['preview'][:100]}...\n")
            related_files.append(r['file'])
    else:
        answer_parts.append("在知識庫中沒有找到直接相關的筆記。")
    
    answer = "".join(answer_parts)
    
    # 回存問答
    saved_file = save_qa_result(question, answer, related_files)
    
    return {
        "answer": answer,
        "results": results,
        "saved_as": saved_file
    }


def execute_dataview_query(query_str: str) -> str:
    """執行 Dataview 風格的查詢並返回格式化結果"""
    engine = QueryEngine()
    output_type, results = engine.query(query_str)
    
    # 取得欄位
    fields = []
    if query_str.upper().startswith('TABLE'):
        # 從 TABLE 後面的字串解析欄位
        after_table = query_str[5:].strip()
        if not after_table.startswith('FROM'):
            fields_part = after_table.split('FROM')[0].strip()
            if fields_part:
                fields = [f.strip().lower() for f in fields_part.split(',')]
    
    if not fields:
        fields = ['file', 'path', 'mtime']
    
    return format_as_markdown(output_type, fields, results)


def generate_marp_slides(topic: str) -> str:
    """產生 Marp 簡報（Markdown 格式）"""
    keywords = [w for w in topic.split() if len(w) > 2][:10]
    results = search_all(keywords)
    
    slides = ["---\nmarp: true\ntheme: default\n---\n"]
    
    slides.append(f"# {topic}\n\n<!-- _class: lead -->\n")
    slides.append(f"**蘇茉圖書館 · {datetime.now().strftime('%Y-%m-%d')}**\n\n---\n")
    
    if results:
        slides.append("## 📚 相關筆記\n\n")
        for r in results[:7]:
            slides.append(f"- {r['file']}\n")
    else:
        slides.append("## 📚 相關筆記\n\n尚無相關筆記\n")
    
    slides.append("\n---\n\n## 📊 知識圖譜\n\n")
    if results:
        for r in results[:5]:
            slides.append(f"```\n{r['preview'][:150]}...\n```\n")
    
    slides.append("\n---\n\n## 總結\n\n")
    slides.append(f"- 共找到 {len(results)} 個相關筆記\n")
    slides.append("- 由蘇茉圖書館提供\n")
    
    return "".join(slides)


# ============================================================================
# 主程式
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        query_str = " ".join(sys.argv[1:])
        
        # 判斷是否為 Dataview 查詢
        if query_str.upper().startswith('LIST') or query_str.upper().startswith('TABLE'):
            print("執行 Dataview 查詢...")
            result = execute_dataview_query(query_str)
            print("\n" + result)
        else:
            # 關鍵詞搜詢
            result = query(query_str)
            print(result["answer"])
            print(f"\n已回存至：{result['saved_as']}")
    else:
        # 互動模式
        print("""
╔══════════════════════════════════════════════════════════════╗
║           蘇茉圖書館 - 強化查詢介面 v2.0                       ║
╠══════════════════════════════════════════════════════════════╣
║  支援兩種模式：                                                ║
║                                                               ║
║  1. 關鍵詞搜詢：直接輸入問題                                   ║
║     例：python 教學                                            ║
║                                                               ║
║  2. Dataview 查詢（類 SQL）：                                  ║
║     LIST                          - 列出所有筆記               ║
║     TABLE file, mtime FROM "summaries"  - 表格顯示            ║
║     LIST WHERE size > 1000        - 條件過濾                  ║
║     LIST SORT mtime DESC LIMIT 5  - 排序和限制                ║
║                                                               ║
║  支援欄位：file, path, ctime, mtime, size, words, tags, links ║
║  離開：輸入 q 或 quit                                          ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        while True:
            try:
                user_input = input("\n查詢> ").strip()
                if user_input.lower() in ['q', 'quit', 'exit']:
                    print("再見！")
                    break
                if not user_input:
                    continue
                
                if user_input.upper().startswith('LIST') or user_input.upper().startswith('TABLE'):
                    result = execute_dataview_query(user_input)
                    print("\n" + result)
                else:
                    result = query(user_input)
                    print(result["answer"])
                    print(f"\n已回存至：{result['saved_as']}")
            except KeyboardInterrupt:
                print("\n再見！")
                break
