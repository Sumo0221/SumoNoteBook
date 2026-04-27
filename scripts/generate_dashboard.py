"""
SumoNoteBook Dashboard Generator
產生 Wiki 知識儀表板

用法:
    python generate_dashboard.py [--output Sumo_wiki/dashboard.html]
"""

import os
from pathlib import Path
from datetime import datetime
from collections import Counter

# ============================================================================
# 設定
# ============================================================================

WIKI_DIR = Path("c:/butler_sumo/library/SumoNoteBook/Sumo_wiki")
CONCEPTS_DIR = WIKI_DIR / "concepts"
SUMMARIES_DIR = WIKI_DIR / "summaries"
QA_DIR = WIKI_DIR / "qa"
OUTPUT_FILE = WIKI_DIR / "dashboard.html"

# ============================================================================
# 工具函數
# ============================================================================

def get_all_markdown_files(directory: Path) -> list:
    """取得目錄下所有 .md 檔案"""
    if not directory.exists():
        return []
    return list(directory.glob("*.md"))

def count_words_in_file(filepath: Path) -> int:
    """計算檔案的字數"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.read())
    except:
        return 0

def extract_links(content: str) -> list:
    """提取 wiki 連結 [[...]]"""
    import re
    return re.findall(r'\[\[([^\]]+)\]\]', content)

def get_file_content(filepath: Path) -> str:
    """安全讀取檔案內容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

def get_all_tags() -> Counter:
    """統計所有標籤"""
    tags = Counter()
    for directory in [CONCEPTS_DIR, SUMMARIES_DIR, QA_DIR]:
        for f in get_all_markdown_files(directory):
            content = get_file_content(f)
            import re
            tag_matches = re.findall(r'#[\w-]+', content)
            tags.update(tag_matches)
    return tags

def get_most_linked_pages(limit: int = 10) -> list:
    """找出最常被連結的頁面"""
    link_counts = Counter()
    
    for directory in [CONCEPTS_DIR, SUMMARIES_DIR, QA_DIR]:
        for f in get_all_markdown_files(directory):
            content = get_file_content(f)
            links = extract_links(content)
            for link in links:
                link_counts[link] += 1
    
    return link_counts.most_common(limit)

def get_recent_files(limit: int = 10) -> list:
    """取得最近更新的檔案"""
    files_with_time = []
    
    for directory in [CONCEPTS_DIR, SUMMARIES_DIR, QA_DIR]:
        for f in get_all_markdown_files(directory):
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                files_with_time.append((f.name, mtime, f.parent.name))
            except:
                pass
    
    # 排序並返回最近的
    files_with_time.sort(key=lambda x: x[1], reverse=True)
    return files_with_time[:limit]

def get_concept_distribution() -> Counter:
    """統計每個目錄的檔案數量"""
    dist = Counter()
    dist['concepts'] = len(get_all_markdown_files(CONCEPTS_DIR))
    dist['summaries'] = len(get_all_markdown_files(SUMMARIES_DIR))
    dist['qa'] = len(get_all_markdown_files(QA_DIR))
    dist['wiki'] = dist['concepts'] + dist['summaries'] + dist['qa']
    return dist

# ============================================================================
# HTML 產生器
# ============================================================================

def generate_html() -> str:
    """產生 Dashboard HTML"""
    
    # 收集資料
    dist = get_concept_distribution()
    tags = get_all_tags()
    most_linked = get_most_linked_pages(10)
    recent = get_recent_files(10)
    
    # 計算總字數
    total_words = 0
    for directory in [CONCEPTS_DIR, SUMMARIES_DIR, QA_DIR]:
        for f in get_all_markdown_files(directory):
            total_words += count_words_in_file(f)
    
    # 計算平均連結數
    total_files = dist['wiki']
    avg_links = sum(count for _, count in most_linked) / max(total_files, 1)
    
    # 產生 HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SumoNoteBook Dashboard</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #e94560; margin-bottom: 30px; }}
        h2 {{ color: #0f3460; margin: 20px 0 10px; border-left: 4px solid #e94560; padding-left: 10px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }}
        .card {{ background: #16213e; border-radius: 10px; padding: 20px; }}
        .card h3 {{ color: #e94560; margin-bottom: 10px; }}
        .stat {{ font-size: 2.5em; color: #0f3460; font-weight: bold; }}
        .stat-label {{ color: #888; font-size: 0.9em; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #333; }}
        th {{ color: #e94560; }}
        tr:hover {{ background: #1f2f50; }}
        .tag {{ display: inline-block; background: #0f3460; padding: 3px 8px; border-radius: 4px; margin: 2px; font-size: 0.85em; }}
        .recent-item {{ padding: 8px; border-bottom: 1px solid #333; }}
        .recent-item:last-child {{ border-bottom: none; }}
        .date {{ color: #888; font-size: 0.8em; }}
        .category {{ color: #e94560; font-size: 0.8em; }}
        a {{ color: #4cc9f0; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 SumoNoteBook Dashboard</h1>
        <p style="color:#888; margin-bottom:30px;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="grid">
            <div class="card">
                <h3>📊 總檔案數</h3>
                <div class="stat">{dist['wiki']}</div>
                <div class="stat-label">wiki pages</div>
            </div>
            <div class="card">
                <h3>🔗 總連結數</h3>
                <div class="stat">{sum(c for _, c in most_linked)}</div>
                <div class="stat-label">cross-references</div>
            </div>
            <div class="card">
                <h3>📝 總字數</h3>
                <div class="stat">{total_words:,}</div>
                <div class="stat-label">characters</div>
            </div>
            <div class="card">
                <h3>🔀 平均連結</h3>
                <div class="stat">{avg_links:.1f}</div>
                <div class="stat-label">links per page</div>
            </div>
        </div>
        
        <h2>📁 分類分佈</h2>
        <div class="grid">
            <div class="card">
                <h3>💡 概念</h3>
                <div class="stat">{dist['concepts']}</div>
            </div>
            <div class="card">
                <h3>📝 摘要</h3>
                <div class="stat">{dist['summaries']}</div>
            </div>
            <div class="card">
                <h3>❓ 問答</h3>
                <div class="stat">{dist['qa']}</div>
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>🏆 最常連結的頁面</h2>
                <table>
                    <tr><th>頁面</th><th>引用次數</th></tr>
"""
    
    for page, count in most_linked:
        html += f"                    <tr><td><a href='#'>{page}</a></td><td>{count}</td></tr>\n"
    
    html += """                </table>
            </div>
            
            <div class="card">
                <h2>🏷️ 熱門標籤</h2>
                <div>
"""
    
    for tag, count in tags.most_common(20):
        html += f'                    <span class="tag">{tag} ({count})</span>\n'
    
    html += """                </div>
            </div>
        </div>
        
        <h2>🕐 最近更新</h2>
        <div class="card">
"""
    
    for name, mtime, category in recent:
        html += f"""            <div class="recent-item">
                <span class="category">[{category}]</span>
                <a href="#">{name}</a>
                <span class="date">{mtime.strftime('%Y-%m-%d %H:%M')}</span>
            </div>
"""
    
    html += """        </div>
        
        <h2>🔄 Ingest 流程</h2>
        <div class="card">
            <p>1. <strong>資料清理</strong> → 刪除重複、清理過時檔案</p>
            <p>2. <strong>知識萃取</strong> → 建立卡片、建立連結</p>
            <p>3. <strong>校準</strong> → 人類檢查、修正</p>
            <p>4. <strong>維護</strong> → 定期更新</p>
        </div>
        
        <footer style="margin-top:40px; padding:20px; text-align:center; color:#666;">
            <p>SumoNoteBook - 蘇茉家族的知識庫 | 基於 Karpathy LLM Wiki 概念</p>
        </footer>
    </div>
</body>
</html>"""
    
    return html

# ============================================================================
# 主程式
# ============================================================================

def main():
    print("=" * 60)
    print("[DASHBOARD] SumoNoteBook Dashboard Generator")
    print("=" * 60)
    
    # 產生 HTML
    html = generate_html()
    
    # 儲存
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Dashboard saved to: {OUTPUT_FILE}")
    print(f"[INFO] Open this file in a browser to view the dashboard")
    
    # 顯示統計
    dist = get_concept_distribution()
    print(f"\n[STATS]")
    print(f"  Wiki pages: {dist['wiki']}")
    print(f"  Concepts: {dist['concepts']}")
    print(f"  Summaries: {dist['summaries']}")
    print(f"  QA: {dist['qa']}")

if __name__ == '__main__':
    exit(main())