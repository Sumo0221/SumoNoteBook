#!/usr/bin/env python3
"""
Drawer Cleanup Script - 定時清理 drawer 暫存檔
每天自動執行，清理 temp 和 scratch 目錄中超過 7 天的檔案
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 設定
WORKSPACE_ROOT = Path(r"C:\butler_sumo\library\SumoNoteBook")
DRAWER_PATH = WORKSPACE_ROOT / "drawer"
RETENTION_DAYS = 7  # 保留 7 天

# 要清理的目錄
CLEANUP_DIRS = ["temp", "scratch"]

# 要保留的目錄（不解動）
PROTECTED_DIRS = ["inbox", "processing", "drafts"]


def get_dir_age_days(path: Path) -> int:
    """取得目錄建立後經過的天數"""
    try:
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        age = datetime.now() - mtime
        return age.days
    except Exception:
        return 0


def cleanup_directory(dir_path: Path, dry_run: bool = True) -> list:
    """清理目錄中過期的檔案"""
    cleaned = []
    
    if not dir_path.exists():
        return cleaned
    
    cutoff_date = datetime.now() - timedelta(days=RETENTION_DAYS)
    
    for item in dir_path.iterdir():
        try:
            if item.is_file():
                mtime = datetime.fromtimestamp(item.stat().st_mtime)
                if mtime < cutoff_date:
                    if not dry_run:
                        item.unlink()
                    cleaned.append(str(item))
            elif item.is_dir():
                # 遞迴處理子目錄
                cleaned.extend(cleanup_directory(item, dry_run))
        except Exception as e:
            print(f"  [警告] 無法處理 {item}: {e}")
    
    return cleaned


def main():
    """主程式"""
    print("=" * 60)
    print("Drawer Cleanup Script")
    print(f"保留期限: {RETENTION_DAYS} 天")
    print(f"工作目錄: {DRAWER_PATH}")
    print("=" * 60)
    
    # 檢查是否為 dry run
    dry_run = "--force" not in sys.argv
    
    if dry_run:
        print("[預覽模式] 使用 --force 執行實際清理")
        print()
    
    total_cleaned = 0
    
    for dir_name in CLEANUP_DIRS:
        dir_path = DRAWER_PATH / dir_name
        
        if not dir_path.exists():
            print(f"[略過] {dir_name}/ - 目錄不存在")
            continue
        
        print(f"\n清理 {dir_name}/...")
        cleaned = cleanup_directory(dir_path, dry_run)
        
        if cleaned:
            print(f"  找到 {len(cleaned)} 個過期檔案")
            for item in cleaned[:10]:  # 只顯示前 10 個
                print(f"    - {Path(item).name}")
            if len(cleaned) > 10:
                print(f"    ... 還有 {len(cleaned) - 10} 個")
            total_cleaned += len(cleaned)
        else:
            print(f"  無過期檔案")
    
    print()
    print("=" * 60)
    if dry_run:
        print(f"預計清理: {total_cleaned} 個檔案")
    else:
        print(f"已清理: {total_cleaned} 個檔案")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())