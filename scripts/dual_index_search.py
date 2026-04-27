"""
SumoNoteBook 雙索引檢索系統
Dual-Index Search System for SumoNoteBook

作者：高工蘇茉
日期：2026-04-09
"""

import os
import json
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import re

# 嘗試導入 LanceDB（可選）
try:
    import lancedb
    LANCEDB_AVAILABLE = True
except ImportError:
    LANCEDB_AVAILABLE = False
    print("⚠️ LanceDB 未安裝，將使用純關鍵詞搜尋")

# ==================== 配置 ====================
CONFIG = {
    "base_path": "C:\\butler_sumo\\library\\SumoNoteBook",
    "db_path": "C:\\butler_sumo\\library\\SumoNoteBook\\data\\index.db",
    "vector_weight": 0.6,
    "keyword_weight": 0.4,
    "top_k": 10,
}


class DualIndexSearch:
    """雙索引檢索引擎"""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path or CONFIG["base_path"])
        self.db_path = Path(CONFIG["db_path"])
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._init_database()
        
    def _init_database(self):
        """初始化資料庫"""
        cursor = self.conn.cursor()
        
        # 關鍵詞索引表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS keyword_index (
                id TEXT PRIMARY KEY,
                file_path TEXT NOT NULL,
                content TEXT,
                keywords TEXT,
                ngrams TEXT,
                location TEXT,
                palace_room TEXT,
                file_type TEXT,
                created_at TEXT,
                updated_at TEXT,
                metadata TEXT
            )
        """)
        
        # FTS5 全文搜尋表
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS fts_index 
            USING fts5(file_path, content, keywords, location)
        """)
        
        # Closet/Drawer 元資料表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS item_metadata (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                tags TEXT,
                location TEXT,
                closet_type TEXT,
                status TEXT DEFAULT 'active',
                created_at TEXT,
                updated_at TEXT
            )
        """)
        
        self.conn.commit()
        
    def _extract_keywords(self, text: str) -> List[str]:
        """提取關鍵詞"""
        # 簡單的中英文分詞
        chinese = re.findall(r'[\u4e00-9fff]+', text)
        english = re.findall(r'[a-zA-Z]+', text)
        
        keywords = []
        keywords.extend([w for w in chinese if len(w) >= 2])
        keywords.extend([w.lower() for w in english if len(w) >= 3])
        
        # 去重
        return list(set(keywords))[:50]
    
    def _extract_ngrams(self, text: str, n: int = 2) -> List[str]:
        """提取 n-gram"""
        words = text.split()
        ngrams = []
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i+n])
            ngrams.append(ngram)
        return ngrams[:100]
    
    def index_file(self, file_path: str, force: bool = False) -> bool:
        """索引單個檔案"""
        try:
            path = Path(file_path)
            if not path.exists():
                return False
            
            # 計算檔案 hash
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            file_hash = hashlib.md5(content.encode()).hexdigest()[:12]
            
            # 檢查是否已索引
            cursor = self.conn.cursor()
            cursor.execute("SELECT id FROM keyword_index WHERE id = ?", (file_hash,))
            if cursor.fetchone() and not force:
                return False
            
            # 提取關鍵詞和 n-gram
            keywords = json.dumps(self._extract_keywords(content))
            ngrams = json.dumps(self._extract_ngrams(content))
            
            # 判斷位置和房間
            location = str(path.relative_to(self.base_path))
            palace_room = self._get_palace_room(location)
            
            # 插入索引
            cursor.execute("""
                INSERT OR REPLACE INTO keyword_index 
                (id, file_path, content, keywords, ngrams, location, palace_room, file_type, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                file_hash,
                str(path),
                content[:10000],  # 限制內容長度
                keywords,
                ngrams,
                location,
                palace_room,
                path.suffix,
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            # FTS 索引
            cursor.execute("""
                INSERT OR REPLACE INTO fts_index (file_path, content, keywords, location)
                VALUES (?, ?, ?, ?)
            """, (str(path), content, keywords, location))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Error indexing {file_path}: {e}")
            return False
    
    def _get_palace_room(self, location: str) -> str:
        """根據位置判斷宮殿房間"""
        location_lower = location.lower()
        
        if 'closet/formal' in location_lower:
            return 'library'
        elif 'closet/casual' in location_lower:
            return 'garden'
        elif 'closet/work' in location_lower:
            return 'workshop'
        elif 'closet/archive' in location_lower:
            return 'archive'
        elif 'drawer' in location_lower:
            return 'drawer_room'
        elif 'sumo_wiki/concepts' in location_lower or 'sumo_wiki/summaries' in location_lower:
            return 'library'
        elif 'sumo_wiki/workflows' in location_lower or 'sumo_wiki/prompts' in location_lower:
            return 'workshop'
        else:
            return 'entrance'
    
    def index_all(self, paths: List[str] = None) -> Dict:
        """索引所有檔案"""
        if paths is None:
            paths = [
                self.base_path / "Sumo_wiki" / "concepts",
                self.base_path / "Sumo_wiki" / "summaries",
                self.base_path / "closet",
                self.base_path / "drawer",
            ]
        
        stats = {"indexed": 0, "skipped": 0, "errors": 0}
        
        for base in paths:
            if not base.exists():
                continue
                
            for ext in ['.md', '.txt', '.yaml', '.json']:
                for file in base.rglob(f"*{ext}"):
                    if self.index_file(str(file)):
                        stats["indexed"] += 1
                    else:
                        stats["skipped"] += 1
        
        return stats
    
    def keyword_search(self, query: str, top_k: int = None) -> List[Dict]:
        """關鍵詞搜尋"""
        top_k = top_k or CONFIG["top_k"]
        cursor = self.conn.cursor()
        
        # FTS5 搜尋
        cursor.execute("""
            SELECT file_path, location, snippet(fts_index, 2, '【', '】', '...', 20) as snippet
            FROM fts_index
            WHERE fts_index MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (query, top_k))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "file_path": row[0],
                "location": row[1],
                "snippet": row[2],
                "score": 1.0  # FTS ranking
            })
        
        return results
    
    def location_search(self, location: str, query: str = None) -> List[Dict]:
        """位置導向搜尋"""
        cursor = self.conn.cursor()
        
        if query:
            cursor.execute("""
                SELECT file_path, content, keywords, location, palace_room
                FROM keyword_index
                WHERE location LIKE ? AND (content LIKE ? OR keywords LIKE ?)
                LIMIT ?
            """, (f"{location}%", f"%{query}%", f"%{query}%", CONFIG["top_k"]))
        else:
            cursor.execute("""
                SELECT file_path, content, keywords, location, palace_room
                FROM keyword_index
                WHERE location LIKE ?
                LIMIT ?
            """, (f"{location}%", CONFIG["top_k"]))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "file_path": row[0],
                "content_preview": row[1][:200] if row[1] else "",
                "keywords": json.loads(row[2]) if row[2] else [],
                "location": row[3],
                "palace_room": row[4],
            })
        
        return results
    
    def palace_walk(self, start_room: str = "entrance", max_rooms: int = 3) -> Dict:
        """宮殿漫遊"""
        import random
        
        room_config = {
            "entrance": {"name": "Entrance 大門", "connections": ["library", "workshop", "garden"]},
            "library": {"name": "Library 圖書館", "connections": ["entrance", "workshop", "archive"]},
            "workshop": {"name": "Workshop 工坊", "connections": ["entrance", "library", "drawer_room"]},
            "garden": {"name": "Garden 花園", "connections": ["entrance", "library"]},
            "drawer_room": {"name": "Drawer 抽屜", "connections": ["workshop"]},
            "archive": {"name": "Archive 檔案室", "connections": ["library"]},
        }
        
        path = []
        current = start_room
        
        for _ in range(max_rooms):
            if current not in room_config:
                break
                
            room_info = room_config[current]
            items = self.location_search(current)
            
            path.append({
                "room": current,
                "room_name": room_info["name"],
                "items": items[:5],  # 每個房間最多5個項目
                "connections": room_info["connections"]
            })
            
            # 隨機選擇下一個房間
            if room_info["connections"]:
                current = random.choice(room_info["connections"])
            else:
                break
        
        return {"path": path, "total_rooms": len(path)}
    
    def search(self, query: str, location: str = None, palace_room: str = None) -> Dict:
        """綜合搜尋介面"""
        results = {
            "query": query,
            "keyword_results": [],
            "location_results": [],
            "palace_results": [],
            "total": 0
        }
        
        # 關鍵詞搜尋
        if query:
            results["keyword_results"] = self.keyword_search(query)
        
        # 位置搜尋
        if location:
            results["location_results"] = self.location_search(location, query)
        
        # 宮殿房間搜尋
        if palace_room:
            results["palace_results"] = self.location_search(palace_room, query)
        
        # 合併結果
        all_ids = set()
        combined = []
        
        for r in results["keyword_results"]:
            r["source"] = "keyword"
            r["score"] = r.get("score", 1.0) * CONFIG["keyword_weight"]
            key = r.get("file_path", "")
            if key and key not in all_ids:
                all_ids.add(key)
                combined.append(r)
        
        for r in results["location_results"]:
            r["source"] = "location"
            r["score"] = 0.8
            key = r.get("file_path", "")
            if key and key not in all_ids:
                all_ids.add(key)
                combined.append(r)
        
        # 排序
        combined.sort(key=lambda x: x.get("score", 0), reverse=True)
        results["results"] = combined[:CONFIG["top_k"]]
        results["total"] = len(combined)
        
        return results
    
    def close(self):
        """關閉資料庫連接"""
        self.conn.close()


def main():
    """測試主程式"""
    print("🚀 SumoNoteBook 雙索引檢索系統")
    print("=" * 50)
    
    search = DualIndexSearch()
    
    # 測試索引
    print("\n📚 正在索引檔案...")
    stats = search.index_all()
    print(f"已索引: {stats['indexed']} 個檔案")
    
    # 測試搜尋
    print("\n🔍 測試搜尋: '蘇茉'")
    results = search.search("蘇茉")
    print(f"找到 {results['total']} 個結果")
    
    for r in results["results"][:3]:
        print(f"  - {r.get('file_path', 'N/A')}")
    
    # 測試宮殿漫遊
    print("\n🏛️ 測試宮殿漫遊...")
    walk = search.palace_walk("entrance", 3)
    print(f"漫遊路徑: {' → '.join([p['room_name'] for p in walk['path']])}")
    
    search.close()
    print("\n✅ 測試完成")


if __name__ == "__main__":
    main()