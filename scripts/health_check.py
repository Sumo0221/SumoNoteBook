"""
蘇茉圖書館 - 健康檢查腳本 v2.0
掃描百科全書，找出矛盾、重複、缺漏，自動更新關聯
參考 Obsidian 插件：Vault Statistics, Find Orphaned Files and Broken Links

新增功能 (v2.0)：
- Vault 統計資訊（筆記數、檔案數、附件數、連結數）
- 孤兒檔案檢測（orphan files）
- 斷裂連結檢測（broken links）
- 損壞檔案檢測（corrupted files）
- 檔案類型統計

執行時間：每日 5:21 AM
"""

import os
import re
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple, Optional

# ============================================================================
# 設定
# ============================================================================
WIKI_DIR = Path("c:/butler_sumo/library/SumoNoteBook/Sumo_wiki")
RAW_DIR = Path("c:/butler_sumo/library/SumoNoteBook/raw")
CONCEPTS_DIR = WIKI_DIR / "concepts"
SUMMARIES_DIR = WIKI_DIR / "summaries"
BACKLINKS_DIR = WIKI_DIR / "backlinks"
PROCESSED_DIR = RAW_DIR / "processed"

# 附件副檔名
ATTACHMENT_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp',
                   '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                   '.zip', '.rar', '.7z', '.mp3', '.mp4', '.wav', '.avi'}


# ============================================================================
# Vault 統計
# ============================================================================

class VaultStats:
    """Vault 統計資訊"""
    
    def __init__(self):
        self.notes_count = 0        # 筆記數量（.md 檔案）
        self.files_count = 0        # 總檔案數量
        self.attachments_count = 0  # 附件數量
        self.links_count = 0        # 連結總數
        self.outlinks_count = 0     # 外部連結數
        self.total_words = 0        # 總字數
        self.total_size = 0         # 總大小（位元組）
        self.file_type_stats: Dict[str, int] = {}  # 各類型檔案統計
        self.tags_counter: Counter = Counter()     # 標籤統計
        self.concepts_list: List[str] = []         # 概念列表
    
    def scan(self) -> 'VaultStats':
        """執行掃描"""
        all_files: List[Path] = []
        
        # 掃描 wiki 目錄
        if WIKI_DIR.exists():
            for f in WIKI_DIR.rglob("*"):
                if f.is_file():
                    all_files.append(f)
        
        # 掃描 raw/processed 目錄
        if PROCESSED_DIR.exists():
            for f in PROCESSED_DIR.rglob("*"):
                if f.is_file():
                    all_files.append(f)
        
        # 遍歷統計
        link_targets: Set[str] = set()  # 連結目標集合
        
        for f in all_files:
            self.files_count += 1
            
            # 統計大小
            try:
                self.total_size += f.stat().st_size
            except Exception:
                pass
            
            ext = f.suffix.lower()
            
            # 根據類型統計
            if ext == '.md':
                self.notes_count += 1
                self._analyze_markdown(f, link_targets)
            elif ext in ATTACHMENT_EXTS:
                self.attachments_count += 1
                self.file_type_stats[ext] = self.file_type_stats.get(ext, 0) + 1
            else:
                self.file_type_stats[ext] = self.file_type_stats.get(ext, 0) + 1
        
        # 連結數
        self.links_count = len(link_targets)
        
        return self
    
    def _analyze_markdown(self, filepath: Path, link_targets: Set[str]):
        """分析 Markdown 檔案"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 計算字數（淨內容）
            clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
            clean = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', clean)
            clean = re.sub(r'[#*`_\[\]{}|\\]', '', clean)
            words = len(clean.strip())
            self.total_words += words
            
            # 提取標籤
            tags = re.findall(r'#([a-zA-Z\u4e00-\u9fff_]+)', content)
            self.tags_counter.update(tags)
            
            # 提取連結
            links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
            link_targets.update(links)
            
            # 外部連結
            outlinks = re.findall(r'https?://[^\s\)\"\'\]]+', content)
            self.outlinks_count += len(outlinks)
            
            # 概念筆記
            if 'concepts' in filepath.parts:
                self.concepts_list.append(filepath.stem)
        
        except Exception as e:
            print(f"警告：無法分析 {filepath}: {e}")
    
    def format_report(self) -> str:
        """格式化統計報告"""
        lines = []
        
        lines.append("## 📊 Vault 統計\n")
        lines.append("| 項目 | 數值 |")
        lines.append("|------|------|")
        lines.append(f"| 筆記數量 | {self.notes_count} |")
        lines.append(f"| 檔案總數 | {self.files_count} |")
        lines.append(f"| 附件數量 | {self.attachments_count} |")
        lines.append(f"| 連結總數 | {self.links_count} |")
        lines.append(f"| 外部連結 | {self.outlinks_count} |")
        lines.append(f"| 總字數 | {self.total_words:,} |")
        
        # 大小格式化
        if self.total_size > 1024 * 1024:
            size_str = f"{self.total_size / (1024*1024):.1f} MB"
        elif self.total_size > 1024:
            size_str = f"{self.total_size / 1024:.1f} KB"
        else:
            size_str = f"{self.total_size} B"
        lines.append(f"| 總大小 | {size_str} |")
        lines.append("")
        
        # 檔案類型統計
        if self.file_type_stats:
            lines.append("### 📁 檔案類型分布\n")
            sorted_types = sorted(self.file_type_stats.items(), key=lambda x: x[1], reverse=True)
            for ext, count in sorted_types[:10]:
                ext_name = ext if ext else '(無副檔名)'
                lines.append(f"- {ext_name}: {count}")
            lines.append("")
        
        # 熱門標籤
        if self.tags_counter:
            lines.append("### 🏷️ 熱門標籤\n")
            top_tags = self.tags_counter.most_common(10)
            for tag, count in top_tags:
                lines.append(f"- #{tag}: {count}")
            lines.append("")
        
        return "\n".join(lines)


# ============================================================================
# 健康檢測
# ============================================================================

class HealthChecker:
    """健康檢查"""
    
    def __init__(self):
        self.duplicates: List[List[str]] = []
        self.orphans: List[str] = []
        self.orphan_files: List[Path] = []  # 孤兒檔案
        self.broken_links: List[Dict] = []  # 斷裂連結
        self.corrupted_files: List[Path] = []  # 損壞檔案
        self.missing_concepts: List[Dict] = []  # 缺失概念
        
        self.summaries: Dict[str, str] = {}
        self.concepts: Dict[str, List[str]] = {}
        self.all_note_ids: Set[str] = set()
        self.all_file_refs: Set[str] = set()
    
    def scan(self) -> 'HealthChecker':
        """執行掃描"""
        self._scan_summaries()
        self._scan_concepts()
        self._scan_backlinks()
        self._build_reference_sets()
        
        # 執行各項檢測
        self.find_duplicates()
        self.find_orphans()
        self.find_orphan_files()
        self.find_broken_links()
        self.check_corrupted_files()
        self.check_missing_concepts()
        
        return self
    
    def _scan_summaries(self):
        """掃描摘要"""
        self.summaries = {}
        for f in SUMMARIES_DIR.glob("*.md"):
            try:
                with open(f, "r", encoding="utf-8") as file:
                    self.summaries[f.stem] = file.read()
                self.all_note_ids.add(f.stem)
            except Exception as e:
                print(f"警告：無法讀取摘要 {f}: {e}")
    
    def _scan_concepts(self):
        """掃描概念"""
        self.concepts = defaultdict(list)
        for f in CONCEPTS_DIR.glob("*.md"):
            try:
                with open(f, "r", encoding="utf-8") as file:
                    content = file.read()
                    # 找出所有相關檔案
                    for line in content.split("\n"):
                        if "- [[" in line:
                            fname = line.split("[[")[1].split("]]")[0]
                            self.concepts[f.stem].append(fname)
                            self.all_file_refs.add(fname)
            except Exception as e:
                print(f"警告：無法讀取概念 {f}: {e}")
    
    def _scan_backlinks(self):
        """掃描反向連結"""
        for f in BACKLINKS_DIR.glob("*.md"):
            try:
                self.all_note_ids.add(f.stem)
            except Exception:
                pass
    
    def _build_reference_sets(self):
        """建立引用集合"""
        # 從所有 markdown 內容建立引用集合
        for note_dir in [SUMMARIES_DIR, CONCEPTS_DIR]:
            if note_dir.exists():
                for f in note_dir.glob("*.md"):
                    try:
                        with open(f, "r", encoding="utf-8") as file:
                            content = file.read()
                            # Wiki 連結
                            links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
                            self.all_file_refs.update(links)
                    except Exception:
                        pass
    
    def find_duplicates(self):
        """找出重複內容"""
        content_hash = defaultdict(list)
        
        for sid, content in self.summaries.items():
            # 用前200字元的hash檢測相似
            key = content[:200].strip()
            content_hash[key].append(sid)
        
        for key, sids in content_hash.items():
            if len(sids) > 1:
                self.duplicates.append(sids)
    
    def find_orphans(self):
        """找出孤兒筆記（沒有被任何概念引用的摘要）"""
        orphans = []
        for sid in self.summaries:
            if sid not in self.all_file_refs:
                orphans.append(sid)
        self.orphans = orphans
    
    def find_orphan_files(self):
        """找出孤兒檔案（在 wiki 目錄下但未被任何筆記引用）"""
        orphan_files = []
        
        if not WIKI_DIR.exists():
            return
        
        # 建立所有被引用的檔案集合（用於判斷）
        all_refs = set()
        for note_dir in [SUMMARIES_DIR, CONCEPTS_DIR]:
            if note_dir.exists():
                for f in note_dir.glob("*.md"):
                    try:
                        with open(f, "r", encoding="utf-8") as file:
                            content = file.read()
                            # 提取所有 wiki 連結
                            links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
                            for link in links:
                                # 移除 anchor（# 前的部分）
                                anchor_idx = link.find('#')
                                if anchor_idx > 0:
                                    link = link[:anchor_idx]
                                all_refs.add(link)
                                all_refs.add(link + '.md')
                    except Exception:
                        pass
        
        # 檢查每個 md 檔案是否被引用
        for f in WIKI_DIR.rglob("*.md"):
            if f.is_file():
                # 取得檔案的基本名稱（不含路徑前綴）
                relative_path = f.relative_to(WIKI_DIR)
                path_str = str(relative_path)
                stem = f.stem
                
                # 檢查是否被引用
                is_referenced = (
                    path_str in all_refs or
                    stem in all_refs or
                    str(relative_path).replace('\\', '/') in all_refs
                )
                
                # 排除 index.md 和健康報告等系統檔案
                system_files = {'index', 'health_report'}
                if stem in system_files:
                    is_referenced = True
                
                if not is_referenced:
                    orphan_files.append(f)
        
        self.orphan_files = orphan_files
    
    def find_broken_links(self):
        """找出斷裂連結（引用了不存在檔案的連結）"""
        broken = []
        
        if not WIKI_DIR.exists():
            return
        
        # 建立所有有效檔案的集合
        valid_files: Set[str] = set()
        if WIKI_DIR.exists():
            for f in WIKI_DIR.rglob("*.md"):
                relative = f.relative_to(WIKI_DIR)
                valid_files.add(str(relative))
                valid_files.add(str(relative).replace('\\', '/'))
                valid_files.add(f.stem)
        
        # 檢查所有筆記的連結
        for note_dir in [SUMMARIES_DIR, CONCEPTS_DIR, WIKI_DIR]:
            if not note_dir.exists():
                continue
            for f in note_dir.glob("*.md"):
                try:
                    with open(f, "r", encoding="utf-8") as file:
                        content = file.read()
                    
                    # 找出所有 wiki 連結
                    links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
                    
                    for link in links:
                        # 移除 anchor
                        anchor_idx = link.find('#')
                        if anchor_idx > 0:
                            link = link[:anchor_idx]
                        
                        link_md = link + '.md'
                        
                        # 檢查是否有效
                        is_valid = (
                            link in valid_files or
                            link_md in valid_files or
                            link in self.all_note_ids
                        )
                        
                        # 排除 URL 和外部連結
                        is_external = link.startswith('http') or '/' in link
                        
                        if not is_valid and not is_external:
                            broken.append({
                                'file': f.relative_to(WIKI_DIR),
                                'link': link,
                                'type': 'broken_wiki_link'
                            })
                
                except Exception as e:
                    print(f"警告：無法檢查連結 {f}: {e}")
        
        self.broken_links = broken
    
    def check_corrupted_files(self):
        """檢查損壞的檔案"""
        corrupted = []
        
        for note_dir in [SUMMARIES_DIR, CONCEPTS_DIR]:
            if note_dir.exists():
                for f in note_dir.glob("*.md"):
                    try:
                        # 嘗試讀取並解碼
                        with open(f, "r", encoding="utf-8") as file:
                            content = file.read()
                            # 嘗試讀取多行確保沒有問題
                            lines = content.split('\n')
                            # 簡單的完整性檢查
                            if content and not content.endswith('\n'):
                                # 檔案不以換行結尾可能是損壞的
                                pass
                    except UnicodeDecodeError:
                        corrupted.append(f)
                    except Exception:
                        corrupted.append(f)
        
        self.corrupted_files = corrupted
    
    def check_missing_concepts(self):
        """檢查缺失的概念引用"""
        missing = []
        
        for sid, content in self.summaries.items():
            # 檢查概念標記是否有對應的概念檔案
            concept_tags = re.findall(r'#(\w+)', content)
            for tag in concept_tags:
                concept_file = CONCEPTS_DIR / f"{tag}.md"
                if not concept_file.exists():
                    missing.append({
                        'note': sid,
                        'concept': tag
                    })
        
        self.missing_concepts = missing
    
    def auto_fix_concepts(self):
        """自動修復概念關聯"""
        fixed_count = 0
        
        for sid, content in self.summaries.items():
            # 從摘要內容提取概念
            words = re.findall(r'\b[A-Za-z\u4e00-\u9fff]{{3,}}\b', content)
            concepts_found = list(set([w.lower() for w in words]))[:10]
            
            # 確保每個概念都有檔案
            for concept in concepts_found:
                concept_file = CONCEPTS_DIR / f"{concept}.md"
                if not concept_file.exists():
                    with open(concept_file, "w", encoding="utf-8") as f:
                        f.write(f"# 概念：{concept}\n\n## 相關檔案\n- [[{sid}]]\n")
                    fixed_count += 1
        
        return fixed_count


# ============================================================================
# 報告產生
# ============================================================================

def generate_report(
    stats: VaultStats,
    checker: HealthChecker,
    fixed: int = 0
) -> str:
    """產生完整的健康報告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    report_lines = [
        "# 蘇茉圖書館 健康報告 v2.0",
        "",
        f"## 檢查時間：{now}",
        "",
        "---",
        "",
    ]
    
    # Vault 統計
    report_lines.append(stats.format_report())
    report_lines.append("---\n")
    
    # 重複檢測
    report_lines.append("## 🔍 重複檢測\n")
    if checker.duplicates:
        report_lines.append(f"\n發現 {len(checker.duplicates)} 組重複：\n")
        for dup in checker.duplicates:
            report_lines.append(f"- {'、'.join(dup)}\n")
    else:
        report_lines.append("\n沒有發現重複內容\n")
    
    report_lines.append("---\n")
    
    # 孤兒筆記
    report_lines.append("## 📄 孤兒筆記\n")
    if checker.orphans:
        report_lines.append(f"\n發現 {len(checker.orphans)} 個孤兒筆記（摘要未被引用）：\n")
        for o in checker.orphans:
            report_lines.append(f"- [[summaries/{o}]]\n")
    else:
        report_lines.append("\n所有摘要都有被引用\n")
    
    report_lines.append("---\n")
    
    # 孤兒檔案
    report_lines.append("## 🗂️ 孤兒檔案\n")
    if checker.orphan_files:
        report_lines.append(f"\n發現 {len(checker.orphan_files)} 個孤兒檔案（未被任何筆記引用）：\n")
        for f in checker.orphan_files[:20]:  # 最多顯示20個
            report_lines.append(f"- {f.relative_to(WIKI_DIR)}\n")
        if len(checker.orphan_files) > 20:
            report_lines.append(f"- ...還有 {len(checker.orphan_files) - 20} 個\n")
    else:
        report_lines.append("\n所有檔案都有被引用\n")
    
    report_lines.append("---\n")
    
    # 斷裂連結
    report_lines.append("## 🔗 斷裂連結\n")
    if checker.broken_links:
        report_lines.append(f"\n發現 {len(checker.broken_links)} 個斷裂連結：\n")
        seen = set()
        for bl in checker.broken_links[:20]:  # 最多顯示20個
            key = f"{bl['file']}->{bl['link']}"
            if key not in seen:
                seen.add(key)
                report_lines.append(f"- [[{bl['file']}]] → [[{bl['link']}]]\n")
        if len(checker.broken_links) > 20:
            report_lines.append(f"- ...還有 {len(checker.broken_links) - 20} 個\n")
    else:
        report_lines.append("\n所有連結都正常\n")
    
    report_lines.append("---\n")
    
    # 損壞檔案
    report_lines.append("## ⚠️ 損壞檔案\n")
    if checker.corrupted_files:
        report_lines.append(f"\n發現 {len(checker.corrupted_files)} 個損壞檔案：\n")
        for f in checker.corrupted_files:
            report_lines.append(f"- {f.relative_to(WIKI_DIR) if WIKI_DIR in f.parents else f}\n")
    else:
        report_lines.append("\n沒有發現損壞檔案\n")
    
    report_lines.append("---\n")
    
    # 缺失概念
    report_lines.append("## 📌 缺失概念\n")
    if checker.missing_concepts:
        report_lines.append(f"\n發現 {len(checker.missing_concepts)} 個缺失概念引用：\n")
        seen_concepts = set()
        for mc in checker.missing_concepts[:10]:
            key = mc['concept']
            if key not in seen_concepts:
                seen_concepts.add(key)
                report_lines.append(f"- #{mc['concept']} (在 [[{mc['note']}]] 中引用)\n")
        if len(checker.missing_concepts) > 10:
            report_lines.append(f"- ...還有 {len(checker.missing_concepts) - 10} 個\n")
    else:
        report_lines.append("\n所有概念引用都正常\n")
    
    report_lines.append("---\n")
    
    # 自動修復
    if fixed > 0:
        report_lines.append(f"\n✅ 已自動修復 {fixed} 個概念檔案\n")
    
    report_lines.append("\n---\n")
    report_lines.append("*此報告由蘇茉圖書館健康檢查腳本 v2.0 自動產生*")
    
    return "\n".join(report_lines)


# ============================================================================
# 主程式
# ============================================================================

def health_check():
    """主健康檢查流程"""
    print(f"[{datetime.now()}] 蘇茉圖書館 健康檢查開始 (v2.0)")
    
    # 確保目錄存在
    for d in [CONCEPTS_DIR, SUMMARIES_DIR, BACKLINKS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    
    # 執行 Vault 統計
    print("正在掃描 Vault 統計...")
    stats = VaultStats().scan()
    print(f"  筆記: {stats.notes_count}, 檔案: {stats.files_count}, "
          f"附件: {stats.attachments_count}, 連結: {stats.links_count}")
    
    # 執行健康檢測
    print("正在執行健康檢測...")
    checker = HealthChecker()
    checker.scan()
    
    print(f"  重複: {len(checker.duplicates)} 組")
    print(f"  孤兒筆記: {len(checker.orphans)} 個")
    print(f"  孤兒檔案: {len(checker.orphan_files)} 個")
    print(f"  斷裂連結: {len(checker.broken_links)} 個")
    print(f"  損壞檔案: {len(checker.corrupted_files)} 個")
    
    # 自動修復
    print("正在自動修復...")
    fixed = checker.auto_fix_concepts()
    if fixed:
        print(f"  已修復 {fixed} 個概念檔案")
    
    # 產生報告
    report = generate_report(stats, checker, fixed)
    report_file = WIKI_DIR / "health_report.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n[{datetime.now()}] 健康檢查完成")
    print(f"報告已存至：{report_file}")
    
    return report


if __name__ == "__main__":
    health_check()
