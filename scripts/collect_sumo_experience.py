"""
蘇茉家族經驗收集器
自動從所有蘇茉的 workspace 收集學習心得和經驗

功能：
1. 掃描所有蘇茉 workspace 的 memory 資料夾
2. 找出學習筆記、開發記錄、問題解決經驗
3. 複製到 SumoNoteBook/raw/shared/
4. 自動去重（根據檔名和 hash）

用法:
    python collect_sumo_experience.py --dry-run  # 預覽
    python collect_sumo_experience.py --execute  # 執行
"""

import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set

# ============================================================================
# 設定
# ============================================================================

# 所有蘇茉的 workspace 路徑
SUMO_WORKSPACES = [
    "C:/Users/rayray/.openclaw/workspace",
    "C:/Users/rayray/.openclaw/workspace_professor",
    "C:/Users/rayray/.openclaw/workspace_engineer",
    "C:/Users/rayray/.openclaw/workspace_senior_engineer",
    "C:/Users/rayray/.openclaw/workspace_hacker",
    "C:/Users/rayray/.openclaw/workspace_writer",
    "C:/Users/rayray/.openclaw/workspace_lawyer",
    "C:/Users/rayray/.openclaw/workspace_finance",
    "C:/Users/rayray/.openclaw/workspace_idol",
    "C:/Users/rayray/.openclaw/workspace_fengshui",
    "C:/Users/rayray/.openclaw/workspace_butler",
    "C:/Users/rayray/.openclaw/workspace_qa",
]

# 目標資料夾
SHARED_RAW = Path("C:/butler_sumo/library/SumoNoteBook/raw/shared")
ARCHIVE_RAW = Path("C:/butler_sumo/library/SumoNoteBook/raw/archive")

# 關鍵字（符合這些關鍵字的檔案會被收集）
KEYWORDS = [
    "learning", "learn", "study", "開發", "development",
    "problem", "solve", "解決", "經驗", "experience",
    "note", "筆記", "記錄", "log", "retrospective",
    "research", "研究", "技術", "tech", "skill",
    "mysticism", "命理", "法律", "law", "finance",
    "torrent", "bt", "backup", "memory",
]

# 要跳過的檔案
SKIP_FILES = [
    "SOUL.md", "USER.md", "TOOLS.md", "AGENTS.md", "HEARTBEAT.md",
    "MEMORY.md", "BOOTSTRAP.md", "IDENTITY.md", "index.md",
    "health_report.md", "log.md",
]

# ============================================================================
# 工具函數
# ============================================================================

def get_file_hash(filepath: Path) -> str:
    """計算檔案的 MD5 hash"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()[:8]
    except:
        return ""

def file_contains_keyword(filepath: Path) -> bool:
    """檢查檔案內容是否含有關鍵字"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            return any(kw.lower() in content for kw in KEYWORDS)
    except:
        return False

def should_collect(filepath: Path) -> bool:
    """判斷是否應該收集這個檔案"""
    # 跳過名單
    if filepath.name in SKIP_FILES:
        return False
    
    # 必須是 .md 檔案
    if filepath.suffix.lower() != '.md':
        return False
    
    # 必須含有關鍵字
    return file_contains_keyword(filepath)

def get_workspace_name(workspace_path: str) -> str:
    """從 workspace 路徑取得蘇茉名稱"""
    basename = Path(workspace_path).name
    # workspace_xxx -> xxx
    if basename.startswith("workspace"):
        return basename.replace("workspace", "").replace("_", "").capitalize()
    return "Main"

# ============================================================================
# 收集邏輯
# ============================================================================

def find_files_to_collect() -> Dict[str, List[Path]]:
    """找出所有需要收集的檔案"""
    files_to_collect = {}
    
    for workspace in SUMO_WORKSPACES:
        ws_path = Path(workspace)
        if not ws_path.exists():
            continue
            
        workspace_name = get_workspace_name(workspace)
        files_to_collect[workspace_name] = []
        
        # 掃描 memory 資料夾
        memory_dir = ws_path / "memory"
        if memory_dir.exists():
            for md_file in memory_dir.glob("*.md"):
                if should_collect(md_file):
                    files_to_collect[workspace_name].append(md_file)
        
        # 掃描 workspace 根目錄的 md 檔案
        for md_file in ws_path.glob("*.md"):
            if should_collect(md_file):
                files_to_collect[workspace_name].append(md_file)
    
    return files_to_collect

def collect_files(dry_run: bool = True) -> Dict:
    """收集檔案到 shared 資料夾"""
    files_to_collect = find_files_to_collect()
    
    results = {
        'total_files': 0,
        'collected': [],
        'skipped': [],
        'errors': [],
    }
    
    # 已收集的 hash 用於去重
    collected_hashes = set()
    
    for workspace_name, files in files_to_collect.items():
        for src_file in files:
            results['total_files'] += 1
            
            try:
                # 計算 hash
                file_hash = get_file_hash(src_file)
                file_key = f"{src_file.stem}_{file_hash}"
                
                # 去重檢查
                if file_key in collected_hashes:
                    results['skipped'].append(f"[SKIP] {src_file.name} (duplicate)")
                    continue
                
                # 產生新檔名
                timestamp = datetime.now().strftime("%Y%m%d")
                new_name = f"{timestamp}_{workspace_name}_{src_file.name}"
                
                if dry_run:
                    results['collected'].append(f"[DRY-RUN] Would copy: {src_file.name} -> {new_name}")
                else:
                    dest_file = SHARED_RAW / new_name
                    shutil.copy2(src_file, dest_file)
                    collected_hashes.add(file_key)
                    results['collected'].append(f"[COPIED] {src_file.name} -> {new_name}")
                    
            except Exception as e:
                results['errors'].append(f"[ERROR] {src_file.name}: {str(e)}")
    
    return results

# ============================================================================
# 主程式
# ============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description='蘇茉家族經驗收集器')
    parser.add_argument('--dry-run', action='store_true', help='Preview mode')
    parser.add_argument('--execute', action='store_true', help='Execute collection')
    args = parser.parse_args()
    
    dry_run = not args.execute
    
    print("=" * 60)
    print("[COLLECT] SumoNoteBook 蘇茉家族經驗收集器")
    print("=" * 60)
    print()
    print(f"Mode: {'DRY-RUN (preview)' if dry_run else 'EXECUTE'}")
    print(f"Target: {SHARED_RAW}")
    print()
    
    results = collect_files(dry_run=dry_run)
    
    print(f"Total files found: {results['total_files']}")
    print(f"Would collect: {len(results['collected'])}")
    print(f"Skipped (duplicate): {len(results['skipped'])}")
    print(f"Errors: {len(results['errors'])}")
    
    if results['collected']:
        print()
        print("[ACTIONS]")
        for action in results['collected'][:20]:
            print(f"  {action}")
        if len(results['collected']) > 20:
            print(f"  ... and {len(results['collected']) - 20} more")
    
    if results['errors']:
        print()
        print("[ERRORS]")
        for error in results['errors']:
            print(f"  {error}")
    
    if dry_run:
        print()
        print("=" * 60)
        print("To execute collection, run with --execute flag")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("[COMPLETE] Collection finished!")
        print(f"Files are in: {SHARED_RAW}")
        print("=" * 60)
    
    return 0

if __name__ == '__main__':
    exit(main())