"""
SumoNoteBook 健康檢查腳本 v3.0
===========================
基於 Karpathy LLM Wiki 的 Lint 流程

功能：
- 矛盾檢測（Contradictions）
- 孤兒檔案檢測（Orphan pages）
- 斷裂連結檢測（Broken links）
- 過時內容檢測（Stale claims）
- 自動修復建議
- 缺失交叉引用建議

執行時間：每日 5:21 AM
"""

import os
import re
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional

# ============================================================================
# 設定
# ============================================================================
WIKI_DIR = Path("c:/butler_sumo/library/SumoNoteBook/Sumo_wiki")
RAW_DIR = Path("c:/butler_sumo/library/SumoNoteBook/raw")
CONCEPTS_DIR = WIKI_DIR / "concepts"
SUMMARIES_DIR = WIKI_DIR / "summaries"
BACKLINKS_DIR = WIKI_DIR / "backlinks"
QA_DIR = WIKI_DIR / "qa"
HEALTH_REPORT = WIKI_DIR / "health_report.md"
LOG_FILE = WIKI_DIR / "log.md"

# 信任期限（天）- 超過這個時間沒有更新的摘要被視為「過時」
STALE_DAYS = 30

# ============================================================================
# 工具函數
# ============================================================================

def get_all_markdown_files(directory: Path) -> List[Path]:
    """取得目錄下所有 .md 檔案"""
    if not directory.exists():
        return []
    return list(directory.glob("*.md"))

def extract_wiki_links(content: str) -> List[str]:
    """提取 Markdown 中的 wiki 連結 [[page]]"""
    return re.findall(r'\[\[([^\]]+)\]\]', content)

def extract_outgoing_links(content: str) -> List[str]:
    """提取外部連結 [text](url)"""
    return re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', content)

def get_file_age_days(file_path: Path) -> int:
    """取得檔案年齡（天）"""
    if not file_path.exists():
        return 0
    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
    return (datetime.now() - mtime).days

def read_file_content(file_path: Path) -> Optional[str]:
    """安全讀取檔案內容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None

def get_all_wiki_files() -> Set[str]:
    """取得所有 wiki 頁面的檔名（不含副檔名）"""
    files = set()
    for directory in [CONCEPTS_DIR, SUMMARIES_DIR, QA_DIR, WIKI_DIR]:
        for f in get_all_markdown_files(directory):
            if f.name not in ['index.md', 'SOUL.md', 'health_report.md']:
                files.add(f.stem)  # 去除副檔名
    return files

def get_all_concepts() -> Dict[str, str]:
    """取得所有概念及其內容"""
    concepts = {}
    if CONCEPTS_DIR.exists():
        for f in get_all_markdown_files(CONCEPTS_DIR):
            content = read_file_content(f)
            if content:
                concepts[f.stem] = content
    return concepts

def get_all_summaries() -> Dict[str, str]:
    """取得所有摘要及其內容"""
    summaries = {}
    if SUMMARIES_DIR.exists():
        for f in get_all_markdown_files(SUMMARIES_DIR):
            content = read_file_content(f)
            if content:
                summaries[f.stem] = content
    return summaries

# ============================================================================
# Lint 檢查類別
# ============================================================================

class LintChecker:
    def __init__(self):
        self.wiki_files = get_all_wiki_files()
        self.concepts = get_all_concepts()
        self.summaries = get_all_summaries()
        self.issues = []
        self.suggestions = []
        
    def check_broken_links(self):
        """檢查斷裂的 wiki 連結"""
        print("[1/6] Checking broken links...")
        broken = []
        
        for directory in [CONCEPTS_DIR, SUMMARIES_DIR, QA_DIR]:
            for f in get_all_markdown_files(directory):
                content = read_file_content(f)
                if not content:
                    continue
                    
                links = extract_wiki_links(content)
                for link in links:
                    # 去除錨點（#）和別名（|）
                    link = link.split('#')[0].split('|')[0].strip()
                    if link and link not in self.wiki_files:
                        broken.append({
                            'file': f.name,
                            'link': link,
                            'line': self._find_line_with_link(content, link)
                        })
        
        if broken:
            self.issues.append(f"[ERROR] Found {len(broken)} broken links")
            for b in broken[:10]:  # 只顯示前10個
                self.issues.append(f"   - {b['file']}: [[{b['link']}]]")
        else:
            self.issues.append("[OK] No broken links")
            
    def _find_line_with_link(self, content: str, link: str) -> int:
        """找到含有連結的行號"""
        for i, line in enumerate(content.split('\n'), 1):
            if link in line:
                return i
        return 0
        
    def check_orphan_pages(self):
        """檢查孤兒頁面（沒有被任何頁面引用）"""
        print("[2/6] Checking orphan pages...")
        
        # 建立所有引用的集合
        referenced = set()
        for directory in [CONCEPTS_DIR, SUMMARIES_DIR, QA_DIR]:
            for f in get_all_markdown_files(directory):
                content = read_file_content(f)
                if content:
                    links = extract_wiki_links(content)
                    for link in links:
                        link = link.split('#')[0].split('|')[0].strip()
                        referenced.add(link)
        
        # 找出孤兒頁面
        orphans = []
        for f in get_all_markdown_files(CONCEPTS_DIR):
            if f.stem not in referenced and f.name != 'SOUL.md':
                orphans.append(f.stem)
                
        if orphans:
            self.issues.append(f"[WARNING] Found {len(orphans)} orphan concepts")
            for o in orphans[:5]:
                self.issues.append(f"   - {o}")
        else:
            self.issues.append("[OK] No orphan pages")
            
    def check_stale_content(self):
        """檢查過時內容"""
        print("[3/6] Checking stale content...")
        stale = []
        
        for f in get_all_markdown_files(SUMMARIES_DIR):
            age = get_file_age_days(f)
            if age > STALE_DAYS:
                stale.append({'file': f.stem, 'days': age})
                
        if stale:
            self.suggestions.append(f"[INFO] Found {len(stale)} stale summaries (>{STALE_DAYS} days)")
            for s in stale[:5]:
                self.suggestions.append(f"   - {s['file']} ({s['days']}天未更新)")
        else:
            self.issues.append("[OK] No stale content")
            
    def check_missing_cross_references(self):
        """檢查缺失的交叉引用"""
        print("[4/6] Checking missing cross-references...")
        
        # 找出可能相關但未連結的概念
        suggestions = []
        concept_names = list(self.concepts.keys())
        
        for i, name1 in enumerate(concept_names):
            for name2 in concept_names[i+1:]:
                # 如果兩個概念名稱相似但未連結
                if self._are_related(name1, name2):
                    if not self._are_linked(name1, name2):
                        suggestions.append((name1, name2))
                        
        if suggestions:
            self.suggestions.append(f"[SUGGEST] Recommend {len(suggestions)} new cross-references")
            for s in suggestions[:5]:
                self.suggestions.append(f"   - {s[0]} ↔ {s[1]}")
        else:
            self.issues.append("[OK] Cross-references complete")
            
    def _are_related(self, name1: str, name2: str) -> bool:
        """判斷兩個概念是否相關"""
        # 簡單判斷：名稱有重疊的詞
        words1 = set(name1.lower().replace('_', ' ').replace('-', ' ').split())
        words2 = set(name2.lower().replace('_', ' ').replace('-', ' ').split())
        return bool(words1 & words2) and len(words1 & words2) >= 1
        
    def _are_linked(self, name1: str, name2: str) -> bool:
        """判斷兩個概念是否已連結"""
        for content in self.concepts.values():
            links = extract_wiki_links(content)
            if name1 in links and name2 in links:
                return True
        return False
        
    def check_contradictions(self):
        """檢查矛盾內容（概念之間的陳述衝突）"""
        print("[5/6] Checking contradictions...")
        
        # 簡化版本：檢查同一概念在不同頁面中的描述衝突
        # 這需要更複雜的 NLP，現在先做簡單檢查
        
        # 檢查同一主題的不同說法
        contradiction_keywords = ['但是', '然而', '不是', '與此相反', '矛盾', '衝突']
        statements = defaultdict(list)
        
        for name, content in self.concepts.items():
            for keyword in contradiction_keywords:
                if keyword in content:
                    # 找到含有矛盾關鍵字的陳述
                    for line in content.split('\n'):
                        if keyword in line and line.strip().startswith('-'):
                            statements[name].append(line.strip())
                            
        if statements:
            self.suggestions.append(f"[WARNING] Found {len(statements)} potential contradictions")
            for name, lines in list(statements.items())[:3]:
                self.suggestions.append(f"   - {name}: {len(lines)} 個矛盾陳述")
        else:
            self.issues.append("[OK] No obvious contradictions")
            
    def check_empty_pages(self):
        """檢查空或幾乎為空的頁面"""
        print("[6/6] Checking empty pages...")
        empty = []
        
        for directory in [CONCEPTS_DIR, SUMMARIES_DIR]:
            for f in get_all_markdown_files(directory):
                content = read_file_content(f)
                if content and len(content.strip()) < 100:
                    empty.append(f.stem)
                    
        if empty:
            self.suggestions.append(f"[INFO] Found {len(empty)} empty/small pages")
            for e in empty[:5]:
                self.suggestions.append(f"   - {e}")
        else:
            self.issues.append("[OK] No empty pages")
            
    def run_all_checks(self) -> Dict:
        """執行所有檢查"""
        print("=" * 60)
        print("[CHECK] SumoNoteBook Lint v3.0")
        print("=" * 60)
        print()
        
        self.check_broken_links()
        self.check_orphan_pages()
        self.check_stale_content()
        self.check_missing_cross_references()
        self.check_contradictions()
        self.check_empty_pages()
        
        return {
            'issues': self.issues,
            'suggestions': self.suggestions,
            'timestamp': datetime.now().isoformat()
        }
        
    def generate_report(self, results: Dict) -> str:
        """產生健康報告"""
        report = f"""# SumoNoteBook 健康報告

> 檢查時間：{results['timestamp']}

---

## 問題（需要處理）

"""
        for issue in results['issues']:
            report += f"- {issue}\n"
            
        report += """
---

## 建議（可以改進）

"""
        for suggestion in results['suggestions']:
            report += f"- {suggestion}\n"
            
        report += f"""
---

## Wiki 統計

| 項目 | 數量 |
|------|------|
| 概念頁面 | {len(self.concepts)} |
| 摘要頁面 | {len(self.summaries)} |
| 總 wiki 頁面 | {len(self.wiki_files)} |

---

> 此報告由 SumoNoteBook Lint v3.0 自動產生
"""
        return report
        
    def save_report(self, results: Dict):
        """儲存健康報告"""
        report = self.generate_report(results)
        with open(HEALTH_REPORT, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n[OK] Report saved to: {HEALTH_REPORT}")
        
    def update_log(self, results: Dict):
        """更新 log.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        issues_count = len([i for i in results['issues'] if i.startswith('[ERROR]')])
        suggestions_count = len(results['suggestions'])
        
        log_entry = f"""
## [{timestamp}] lint | Health Check
- Issues: {issues_count}
- Suggestions: {suggestions_count}
- Report: health_report.md
"""
        
        # 讀取現有 log
        if LOG_FILE.exists():
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = "# SumoNoteBook Activity Log\n"
            
        # 插入新記錄（在 AUTO_LOG 之前或檔案末尾）
        if '<!-- AUTO_LOG -->' in content:
            content = content.replace('<!-- AUTO_LOG -->', log_entry + '\n<!-- AUTO_LOG -->')
        else:
            content += log_entry
            
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"[OK] log.md updated")

# ============================================================================
# 主程式
# ============================================================================

def main():
    checker = LintChecker()
    results = checker.run_all_checks()
    checker.save_report(results)
    checker.update_log(results)
    
    print()
    print("=" * 60)
    print("[SUMMARY]")
    print("=" * 60)
    
    issues_count = len([i for i in results['issues'] if i.startswith('[ERROR]')])
    warnings_count = len([i for i in results['issues'] if i.startswith('[WARNING]')]) + len([s for s in results['suggestions'] if s.startswith('[WARNING]') or s.startswith('[INFO]')])
    
    print(f"[ERROR] Issues: {issues_count}")
    print(f"[WARNING] Warnings: {warnings_count}")
    print(f"[SUGGEST] Suggestions: {len(results['suggestions'])}")
    
    if issues_count == 0:
        print("\n[OK] Wiki is healthy!")
    else:
        print(f"\n[WARNING] Need to fix {issues_count} issues")
        
    return 0 if issues_count == 0 else 1

if __name__ == '__main__':
    exit(main())