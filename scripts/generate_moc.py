"""
SumoNoteBook MOC (Map of Content) Generator
自動建立知識主軸地圖

用法:
    python generate_moc.py [--output Sumo_wiki/MOC.md]
"""

import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ============================================================================
# 設定
# ============================================================================

WIKI_DIR = Path("c:/butler_sumo/library/SumoNoteBook/Sumo_wiki")
CONCEPTS_DIR = WIKI_DIR / "concepts"
SUMMARIES_DIR = WIKI_DIR / "summaries"
OUTPUT_FILE = WIKI_DIR / "MOC.md"

# ============================================================================
# 工具函數
# ============================================================================

def get_all_markdown_files(directory: Path) -> list:
    if not directory.exists():
        return []
    return list(directory.glob("*.md"))

def get_file_content(filepath: Path) -> str:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

def extract_title(content: str) -> str:
    """提取第一個標題"""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return match.group(1) if match else filepath.stem

def extract_tags(content: str) -> list:
    """提取所有標籤"""
    return re.findall(r'#[\w-]+', content)

def extract_links(content: str) -> list:
    """提取 wiki 連結"""
    return re.findall(r'\[\[([^\]]+)\]\]', content)

def categorize_by_tags(files: list) -> dict:
    """根據標籤分類檔案"""
    categories = defaultdict(list)
    
    for f in files:
        content = get_file_content(f)
        tags = extract_tags(content)
        
        if not tags:
            categories['#untagged'].append(f)
            continue
            
        for tag in tags:
            categories[tag].append(f)
    
    return dict(categories)

def find_hub_concepts(files: list, limit: int = 5) -> list:
    """找出最常被連結的概念"""
    link_counts = defaultdict(int)
    
    for f in files:
        content = get_file_content(f)
        links = extract_links(content)
        for link in links:
            link_counts[link] += 1
    
    sorted_links = sorted(link_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_links[:limit]

# ============================================================================
# MOC 產生器
# ============================================================================

def generate_moc() -> str:
    """產生 MOC Markdown"""
    
    all_files = []
    for directory in [CONCEPTS_DIR, SUMMARIES_DIR]:
        all_files.extend(get_all_markdown_files(directory))
    
    # 根據標籤分類
    categories = categorize_by_tags(all_files)
    
    # 找出 Hub 概念
    hub_concepts = find_hub_concepts(all_files)
    
    # 產生 MOC
    moc = f"""# 📚 SumoNoteBook Map of Content

> 自動產生：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 🏆 樞紐概念（最常被連結）

| 概念 | 引用次數 |
|------|----------|
"""
    
    for concept, count in hub_concepts:
        moc += f"| [[{concept}]] | {count} |\n"
    
    moc += """
---

## 📊 知識分類

| 分類 | 檔案數 |
|------|--------|
"""
    
    for tag, files in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
        moc += f"| {tag} | {len(files)} |\n"
    
    moc += """
---

"""
    
    # 每個分類的詳細內容
    for tag, files in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
        if tag == '#untagged':
            continue
            
        moc += f"""## {tag}

"""
        
        for f in files:
            title = extract_title(get_file_content(f))
            links = extract_links(get_file_content(f))
            link_count = len(links)
            
            moc += f"- [[{title}]] ({link_count} 連結)\n"
        
        moc += "\n"
    
    # 沒有標籤的檔案
    if '#untagged' in categories:
        moc += """## #untagged（未分類）

"""
        for f in categories['#untagged']:
            title = extract_title(get_file_content(f))
            moc += f"- [[{title}]]\n"
    
    moc += f"""
---

## 📝 使用說明

1. **瀏覽樞紐概念** - 這些是被引用最多的概念，是知識網絡的核心
2. **查看知識分類** - 按標籤瀏覽相關檔案
3. **發現缺口** - 看看哪個分類檔案最少，可能需要加強

---

> 🤖 此 MOC 由 SumoNoteBook 自動產生
> 基於 {len(all_files)} 個檔案
"""
    
    return moc

# ============================================================================
# 主程式
# ============================================================================

def main():
    print("=" * 60)
    print("[MOC] SumoNoteBook MOC Generator")
    print("=" * 60)
    
    # 產生 MOC
    moc = generate_moc()
    
    # 儲存
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(moc)
    
    print(f"\n[OK] MOC saved to: {OUTPUT_FILE}")
    
    # 顯示統計
    all_files = []
    for directory in [CONCEPTS_DIR, SUMMARIES_DIR]:
        all_files.extend(get_all_markdown_files(directory))
    
    print(f"\n[STATS]")
    print(f"  Total files: {len(all_files)}")
    
    categories = categorize_by_tags(all_files)
    print(f"  Categories: {len(categories)}")
    
    hub_concepts = find_hub_concepts(all_files)
    if hub_concepts:
        print(f"  Top hub: {hub_concepts[0][0]} ({hub_concepts[0][1]} links)")

if __name__ == '__main__':
    exit(main())