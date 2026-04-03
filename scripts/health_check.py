"""
蘇茉圖書館 - 健康檢查腳本
掃描百科全書，找出矛盾、重複、缺漏，自動更新關聯
執行時間：每日 5:21 AM
"""

import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

WIKI_DIR = Path("c:/butler_sumo/library/SumoNoteBook/Sumo_wiki")
CONCEPTS_DIR = WIKI_DIR / "concepts"
SUMMARIES_DIR = WIKI_DIR / "summaries"
BACKLINKS_DIR = WIKI_DIR / "backlinks"


def scan_summaries():
    """掃描所有摘要"""
    summaries = {}
    for f in SUMMARIES_DIR.glob("*.md"):
        with open(f, "r", encoding="utf-8") as file:
            content = file.read()
            summaries[f.stem] = content
    return summaries


def scan_concepts():
    """掃描所有概念"""
    concepts = defaultdict(list)
    for f in CONCEPTS_DIR.glob("*.md"):
        with open(f, "r", encoding="utf-8") as file:
            content = file.read()
            # 找出所有相關檔案
            for line in content.split("\n"):
                if "- [[" in line:
                    fname = line.split("[[")[1].split("]]")[0]
                    concepts[f.stem].append(fname)
    return concepts


def find_duplicates(summaries):
    """找出重複內容"""
    content_hash = defaultdict(list)
    duplicates = []
    
    for sid, content in summaries.items():
        # 用前200字元的hash檢測相似
        key = content[:200].strip()
        content_hash[key].append(sid)
    
    for key, sids in content_hash.items():
        if len(sids) > 1:
            duplicates.append(sids)
    
    return duplicates


def find_orphans(summaries, concepts):
    """找出孤兒筆記（沒有被任何概念引用的摘要）"""
    all_refs = set()
    for refs in concepts.values():
        all_refs.update(refs)
    
    orphans = []
    for sid in summaries:
        if sid not in all_refs:
            orphans.append(sid)
    
    return orphans


def check_missing_links(summaries):
    """檢查缺失的連結"""
    issues = []
    for sid, content in summaries.items():
        # 檢查概念標記是否有對應的概念檔案
        import re
        concept_tags = re.findall(r'#(\w+)', content)
        for tag in concept_tags:
            concept_file = CONCEPTS_DIR / f"{tag}.md"
            if not concept_file.exists():
                issues.append(f"[{sid}] 概念 #{tag} 缺少對應檔案")
    return issues


def generate_report(duplicates, orphans, issues):
    """產生健康報告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = f"""# 蘇茉圖書館 健康報告

## 檢查時間：{now}

---

## 重複檢測
"""
    if duplicates:
        report += f"\n發現 {len(duplicates)} 組重複：\n"
        for dup in duplicates:
            report += f"- {'、'.join(dup)}\n"
    else:
        report += "\n沒有發現重複內容\n"

    report += "\n---\n\n## 孤兒筆記\n"
    if orphans:
        report += f"\n發現 {len(orphans)} 個孤兒筆記：\n"
        for o in orphans:
            report += f"- [[summaries/{o}]]\n"
    else:
        report += "\n所有摘要都有被引用\n"

    report += "\n---\n\n## 連結問題\n"
    if issues:
        report += f"\n發現 {len(issues)} 個問題：\n"
        for issue in issues:
            report += f"- {issue}\n"
    else:
        report += "\n所有連結都正常\n"

    report += "\n---\n\n## 統計\n"
    report += f"- 摘要總數：{len(list(SUMMARIES_DIR.glob('*.md')))}\n"
    report += f"- 概念總數：{len(list(CONCEPTS_DIR.glob('*.md')))}\n"
    report += f"- 反向連結：{len(list(BACKLINKS_DIR.glob('*.md')))}\n"

    return report


def auto_fix_concepts(summaries, concepts):
    """自動修復概念關聯"""
    fixed_count = 0
    
    for sid, content in summaries.items():
        # 從摘要內容提取概念
        import re
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


def health_check():
    """主健康檢查流程"""
    print(f"[{datetime.now()}] 蘇茉圖書館 健康檢查開始")
    
    # 掃描
    summaries = scan_summaries()
    concepts = scan_concepts()
    
    print(f"掃描完成：{len(summaries)} 摘要，{len(concepts)} 概念")
    
    # 檢測問題
    duplicates = find_duplicates(summaries)
    orphans = find_orphans(summaries, concepts)
    issues = check_missing_links(summaries)
    
    # 自動修復
    fixed = auto_fix_concepts(summaries, concepts)
    if fixed:
        print(f"自動修復了 {fixed} 個概念檔案")
    
    # 產生報告
    report = generate_report(duplicates, orphans, issues)
    report_file = WIKI_DIR / "health_report.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(report)
    print(f"[{datetime.now()}] 健康檢查完成，報告已存至 {report_file}")


if __name__ == "__main__":
    health_check()
