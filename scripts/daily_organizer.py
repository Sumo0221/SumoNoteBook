"""
蘇茉圖書館 - 每日整理腳本
自動讀取 raw 資料夾，產出結構化筆記，存入 Sumo_wiki
執行時間：每日 4:12 AM
"""

import os
import re
import shutil
import hashlib
from datetime import datetime
from pathlib import Path

RAW_DIR = Path("c:/butler_sumo/library/SumoNoteBook/raw")
PROCESSED_DIR = RAW_DIR / "processed"
WIKI_DIR = Path("c:/butler_sumo/library/SumoNoteBook/Sumo_wiki")
CONCEPTS_DIR = WIKI_DIR / "concepts"
SUMMARIES_DIR = WIKI_DIR / "summaries"
BACKLINKS_DIR = WIKI_DIR / "backlinks"


def get_file_hash(filepath):
    """取得檔案 hash 作為唯一 ID"""
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def read_file_content(filepath):
    """讀取檔案內容"""
    ext = filepath.suffix.lower()
    if ext in [".md", ".txt", ".py", ".js", ".csv", ".json", ".yaml", ".yml"]:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return f"[二進制檔案: {filepath.name}]"


def extract_concepts(content):
    """簡單的概念擷取（關鍵詞）"""
    import re
    # 移除程式碼區塊
    content_clean = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content_clean = re.sub(r'`[^`]+`', '', content_clean)
    
    # 移除路徑和特殊字元
    content_clean = re.sub(r'[a-zA-Z]:\\[^\s]+', '', content_clean)
    
    words = content_clean.split()
    # 取長度 > 3 的中英文混合單字，排除數字和路徑
    concepts = []
    for w in words:
        w = w.strip(".,!?()[]{}:;\"'-_/\\#")
        if len(w) > 3 and not w.startswith('venv') and not w.startswith('c:') and not w.isdigit():
            concepts.append(w)
    
    # 只取有實際意義的概念（至少包含一個字母）
    concepts = [c for c in concepts if any(ch.isalpha() for ch in c)]
    return list(set(concepts))[:20]  # 取最多20個


def create_summary(raw_filename, content):
    """為單一檔案建立摘要"""
    file_id = get_file_hash(Path(RAW_DIR / raw_filename))
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    summary_content = f"""# 摘要：{raw_filename}

## 基本資訊
- **原始檔案**：{raw_filename}
- **檔案 ID**：{file_id}
- **建立時間**：{now}
- **類型**：{Path(raw_filename).suffix}

## 內容預覽

{content[:500]}{"..." if len(content) > 500 else ""}

## 概念關鍵詞

<!-- AUTO_CONCEPTS -->

## 反向連結

> 此摘要由 [每日整理腳本](../scripts/daily_organizer.py) 自動產生
"""
    return summary_content, file_id


def create_concept_note(concept, related_files):
    """為概念建立筆記"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    content = f"""# 概念：{concept}

## 相關檔案
{"".join([f"- [[{f}]]" for f in related_files])}

## 建立時間：{now}
"""
    return content


def update_backlinks(file_id, raw_filename, concepts):
    """更新反向連結"""
    backlinks_file = BACKLINKS_DIR / f"{file_id}.md"
    content = f"""# 反向連結：{raw_filename}

## 檔案 ID：{file_id}

## 概念關聯
{"".join([f"- #{c}" for c in concepts])}

## 原始位置
[[../raw/{raw_filename}]]
"""
    with open(backlinks_file, "w", encoding="utf-8") as f:
        f.write(content)


def update_index(new_files, new_summaries):
    """更新總目錄"""
    index_file = WIKI_DIR / "index.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    new_entries = "\n".join([f"- [[summaries/{s}]] - {f}" for s, f in zip(new_summaries, new_files)])
    
    with open(index_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 更新最近更新
    content = content.replace("<!-- AUTO_UPDATE -->", f"- {now}: {', '.join([Path(f).stem for f in new_files])}\n<!-- AUTO_UPDATE -->")
    
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(content)


def organize():
    """主整理流程"""
    print(f"[{datetime.now()}] 蘇茉圖書館 每日整理開始")
    
    # 確保目錄存在
    for d in [PROCESSED_DIR, CONCEPTS_DIR, SUMMARIES_DIR, BACKLINKS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    
    # 找出新的 raw 檔案
    raw_files = list(RAW_DIR.glob("*"))
    raw_files = [f for f in raw_files if f.is_file() and f.suffix not in [".py"]]
    
    if not raw_files:
        print("沒有新檔案需要整理")
        return
    
    print(f"找到 {len(raw_files)} 個新檔案")
    new_summaries = []
    
    for raw_file in raw_files:
        print(f"處理: {raw_file.name}")
        content = read_file_content(raw_file)
        summary, file_id = create_summary(raw_file.name, content)
        
        # 存摘要
        summary_file = SUMMARIES_DIR / f"{file_id}.md"
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(summary)
        new_summaries.append(f"{file_id}.md")
        
        # 擷取概念並建立概念筆記
        concepts = extract_concepts(content)
        
        # 更新反向連結
        update_backlinks(file_id, raw_file.name, concepts)
        
        # 概念筆記
        for concept in concepts:
            # 安全的檔案名（只允許字母數字中文）
            safe_name = re.sub(r'[^\w\u4e00-\u9fff]', '_', concept)[:50]
            concept_file = CONCEPTS_DIR / f"{safe_name}.md"
            existing = ""
            if concept_file.exists():
                with open(concept_file, "r", encoding="utf-8") as f:
                    existing = f.read()
            
            if raw_file.name not in existing:
                with open(concept_file, "a", encoding="utf-8") as f:
                    f.write(f"\n- [[{raw_file.name}]]")
        
        # 移動到 processed
        dest = PROCESSED_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{raw_file.name}"
        shutil.move(str(raw_file), str(dest))
        print(f"  → 已移至 processed: {dest.name}")
    
    # 更新 index
    update_index([r.name for r in raw_files], new_summaries)
    
    print(f"[{datetime.now()}] 整理完成！處理了 {len(raw_files)} 個檔案")


if __name__ == "__main__":
    organize()
