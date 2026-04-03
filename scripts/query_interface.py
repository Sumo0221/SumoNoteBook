"""
蘇茉圖書館 - 查詢介面
查詢 Sumo_wiki 並回答問題，同時將問答結果回存
"""

import os
import re
from pathlib import Path
from datetime import datetime

WIKI_DIR = Path("c:/butler_sumo/library/SumoNoteBook/Sumo_wiki")
CONCEPTS_DIR = WIKI_DIR / "concepts"
SUMMARIES_DIR = WIKI_DIR / "summaries"
BACKLINKS_DIR = WIKI_DIR / "backlinks"


def search_in_file(filename, keywords):
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


def search_all(keywords):
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


def get_concept_related(concept_name):
    """取得概念相關的檔案"""
    concept_file = CONCEPTS_DIR / f"{concept_name}.md"
    if not concept_file.exists():
        return []
    
    with open(concept_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    files = []
    for line in content.split("\n"):
        if "- [[" in line:
            fname = line.split("[[")[1].split("]]")[0]
            files.append(fname)
    return files


def get_backlinks(file_id):
    """取得某檔案的反向連結"""
    backlink_file = BACKLINKS_DIR / f"{file_id}.md"
    if not backlink_file.exists():
        return []
    
    with open(backlink_file, "r", encoding="utf-8") as f:
        return f.read()


def save_qa_result(question, answer, related_files):
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
    
    qa_file = WIKI_DIR / "qa" / f"{qa_id}.md"
    qa_file.parent.mkdir(parents=True, exist_ok=True)
    with open(qa_file, "w", encoding="utf-8") as f:
        f.write(qa_content)
    
    return qa_file.name


def query(question):
    """查詢入口"""
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
        for r in results[:5]:  # 最多顯示5個
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


def generate_marp_slides(topic):
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


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        result = query(question)
        print(result["answer"])
        print(f"\n已回存至：{result['saved_as']}")
