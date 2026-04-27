"""
SumoNoteBook Wiki Cleanup Script
清除斷裂連結和空/小頁面

用法:
    python cleanup_wiki.py --dry-run  # 預覽模式
    python cleanup_wiki.py --execute  # 執行清理
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple

# ============================================================================
# 設定
# ============================================================================
WIKI_DIR = Path("c:/butler_sumo/library/SumoNoteBook/Sumo_wiki")
CONCEPTS_DIR = WIKI_DIR / "concepts"
SUMMARIES_DIR = WIKI_DIR / "summaries"
BACKUP_DIR = WIKI_DIR / "backup_cleanup"

# 頁面大小門檻（小於這個 byte 數視為"空"）
SIZE_THRESHOLD = 100

# ============================================================================
# 工具函數
# ============================================================================

def get_all_markdown_files(directory: Path) -> List[Path]:
    """取得目錄下所有 .md 檔案"""
    if not directory.exists():
        return []
    return list(directory.glob("*.md"))

def get_all_wiki_files() -> Set[str]:
    """取得所有 wiki 頁面的檔名（不含副檔名）"""
    files = set()
    for directory in [CONCEPTS_DIR, SUMMARIES_DIR, WIKI_DIR]:
        for f in get_all_markdown_files(directory):
            if f.name not in ['index.md', 'SOUL.md', 'health_report.md', 'log.md']:
                files.add(f.stem)
    return files

def extract_wiki_links(content: str) -> List[str]:
    """提取 Markdown 中的 wiki 連結 [[page]]"""
    return re.findall(r'\[\[([^\]]+)\]\]', content)

def read_file_content(file_path: Path) -> str:
    """安全讀取檔案內容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

def get_file_size(file_path: Path) -> int:
    """取得檔案大小"""
    try:
        return file_path.stat().st_size
    except:
        return 0

# ============================================================================
# 斷裂連結處理
# ============================================================================

def find_broken_links() -> Dict[str, List[str]]:
    """找出所有斷裂的連結"""
    wiki_files = get_all_wiki_files()
    broken_links = {}  # {filename: [broken_link_targets]}
    
    for directory in [CONCEPTS_DIR, SUMMARIES_DIR]:
        for f in get_all_markdown_files(directory):
            content = read_file_content(f)
            links = extract_wiki_links(content)
            
            for link in links:
                # 去除錨點（#）和別名（|）
                link = link.split('#')[0].split('|')[0].strip()
                if link and link not in wiki_files:
                    if f.name not in broken_links:
                        broken_links[f.name] = []
                    broken_links[f.name].append(link)
    
    return broken_links

def fix_broken_links(dry_run: bool = True) -> Tuple[int, List[str]]:
    """修復斷裂的連結（移除它們）"""
    broken_links = find_broken_links()
    total_fixed = 0
    actions = []
    
    for filename, links in broken_links.items():
        filepath = CONCEPTS_DIR / filename
        if not filepath.exists():
            filepath = SUMMARIES_DIR / filename
            
        if not filepath.exists():
            continue
            
        content = read_file_content(filepath)
        original_content = content
        
        for broken_link in links:
            # 移除斷裂連結，但保留其他文字
            # 匹配 [[broken_link]] 或 [[broken_link|alias]] 或 [[broken_link#anchor]]
            patterns = [
                rf'\[\[{re.escape(broken_link)}\]\]',
                rf'\[\[{re.escape(broken_link)}\|([^\]]+)\]\]',
                rf'\[\[{re.escape(broken_link)}#([^\]]+)\]\]',
                rf'\[\[{re.escape(broken_link)}#([^\]]+)\|([^\]]+)\]\]',
            ]
            for pattern in patterns:
                content = re.sub(pattern, broken_link, content)
        
        if content != original_content:
            if dry_run:
                actions.append(f"[DRY-RUN] Would fix {len(links)} links in {filename}")
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                actions.append(f"[FIXED] {len(links)} links in {filename}")
            total_fixed += len(links)
    
    return total_fixed, actions

# ============================================================================
# 空/小頁面處理
# ============================================================================

def find_empty_pages() -> List[Tuple[str, int]]:
    """找出所有空/小頁面"""
    empty_pages = []
    
    for directory in [CONCEPTS_DIR, SUMMARIES_DIR]:
        for f in get_all_markdown_files(directory):
            size = get_file_size(f)
            if size < SIZE_THRESHOLD:
                empty_pages.append((f.name, size))
    
    return empty_pages

def delete_empty_pages(dry_run: bool = True) -> Tuple[int, List[str]]:
    """刪除空/小頁面"""
    empty_pages = find_empty_pages()
    total_deleted = 0
    actions = []
    
    for filename, size in empty_pages:
        filepath = CONCEPTS_DIR / filename
        if not filepath.exists():
            filepath = SUMMARIES_DIR / filename
        
        if not filepath.exists():
            continue
        
        if dry_run:
            actions.append(f"[DRY-RUN] Would delete {filename} ({size} bytes)")
        else:
            # 建立備份
            BACKUP_DIR.mkdir(exist_ok=True)
            backup_path = BACKUP_DIR / f"{filename}.bak"
            shutil.copy2(filepath, backup_path)
            
            # 刪除原檔案
            filepath.unlink()
            actions.append(f"[DELETED] {filename} -> backup/{filename}.bak")
        total_deleted += 1
    
    return total_deleted, actions

# ============================================================================
# 主程式
# ============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description='SumoNoteBook Wiki Cleanup')
    parser.add_argument('--dry-run', action='store_true', help='Preview mode')
    parser.add_argument('--execute', action='store_true', help='Execute cleanup')
    args = parser.parse_args()
    
    dry_run = not args.execute
    
    print("=" * 60)
    print("[CLEANUP] SumoNoteBook Wiki Cleanup")
    print("=" * 60)
    print()
    print(f"Mode: {'DRY-RUN (preview)' if dry_run else 'EXECUTE (will make changes)'}")
    print()
    
    # Phase 1: 處理斷裂連結
    print("[1/2] Finding broken links...")
    broken_links = find_broken_links()
    total_broken = sum(len(links) for links in broken_links.values())
    print(f"Found {len(broken_links)} files with {total_broken} broken links")
    
    print()
    print("[2/2] Finding empty/small pages...")
    empty_pages = find_empty_pages()
    print(f"Found {len(empty_pages)} empty/small pages")
    
    print()
    print("=" * 60)
    print("[SUMMARY]")
    print("=" * 60)
    print(f"Broken links: {total_broken} in {len(broken_links)} files")
    print(f"Empty pages: {len(empty_pages)} pages")
    print()
    
    if dry_run:
        print("[MODE] DRY-RUN - No changes will be made")
        print()
        
        # 顯示會進行的動作
        print("[ACTIONS - Broken Links]")
        fixed, link_actions = fix_broken_links(dry_run=True)
        for action in link_actions[:10]:
            print(f"  {action}")
        if len(link_actions) > 10:
            print(f"  ... and {len(link_actions) - 10} more")
        
        print()
        print("[ACTIONS - Empty Pages]")
        deleted, delete_actions = delete_empty_pages(dry_run=True)
        for action in delete_actions[:10]:
            print(f"  {action}")
        if len(delete_actions) > 10:
            print(f"  ... and {len(delete_actions) - 10} more")
        
        print()
        print("=" * 60)
        print("To execute cleanup, run with --execute flag")
        print("=" * 60)
    else:
        print("[MODE] EXECUTING - Changes will be made")
        print()
        
        # 執行清理
        fixed, link_actions = fix_broken_links(dry_run=False)
        deleted, delete_actions = delete_empty_pages(dry_run=False)
        
        print(f"[RESULT] Fixed {fixed} broken links")
        print(f"[RESULT] Deleted {deleted} empty pages")
        
        if BACKUP_DIR.exists():
            print(f"[NOTE] Deleted files backed up to: {BACKUP_DIR}")
        
        print()
        print("=" * 60)
        print("[COMPLETE] Cleanup finished!")
        print("=" * 60)
    
    return 0

if __name__ == '__main__':
    exit(main())