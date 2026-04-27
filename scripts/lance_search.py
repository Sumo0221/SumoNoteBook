"""
SumoNoteBook LanceDB 向量搜尋系統
LanceDB Vector Search System for SumoNoteBook

作者：工程師蘇茉
日期：2026-04-09
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np
import pyarrow as pa

# 配置
CONFIG = {
    "base_path": "C:\\butler_sumo\\library\\SumoNoteBook",
    "lance_path": "C:\\butler_sumo\\library\\SumoNoteBook\\data\\sumo_notebook.lance",
    "model_name": "paraphrase-multilingual-MiniLM-L12-v2",
    "top_k": 10,
    "batch_size": 32,
}

# ==================== 嘗試導入必要套件 ====================
try:
    import lancedb
    LANCEDB_AVAILABLE = True
except ImportError:
    LANCEDB_AVAILABLE = False
    print("LanceDB 未安裝")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("sentence-transformers 未安裝")


class LanceDBVectorSearch:
    """LanceDB 向量搜尋引擎"""
    
    def __init__(self, base_path: str = None, model_name: str = None):
        self.base_path = Path(base_path or CONFIG["base_path"])
        self.lance_path = Path(CONFIG["lance_path"])
        self.lance_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.model_name = model_name or CONFIG["model_name"]
        self.model = None
        self.db = None
        self.table = None
        
        # 初始化模型
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            print(f"載入embedding模型: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
        
        # 初始化資料庫
        if LANCEDB_AVAILABLE:
            self._init_database()
    
    def _init_database(self):
        """初始化LanceDB資料庫"""
        self.db = lancedb.connect(str(self.lance_path))
        
        # 檢查表是否存在
        try:
            table_names = self.db.list_tables()
        except:
            table_names = []
        
        if "documents" in table_names:
            self.table = self.db.open_table("documents")
            print("已開啟現有LanceDB表")
            
            # 檢查是否為空
            try:
                df = self.table.to_pandas()
                if len(df) == 0:
                    print("表為空，將重建...")
                    # 刪除並重建
                    self.db.drop_table("documents")
                    schema = pa.schema([
                        ("id", pa.string()),
                        ("file_path", pa.string()),
                        ("content", pa.string()),
                        ("location", pa.string()),
                        ("palace_room", pa.string()),
                        ("title", pa.string()),
                        ("keywords", pa.string()),
                        ("vector", pa.list_(pa.float32(), 384)),
                    ])
                    self.table = self.db.create_table("documents", schema=schema)
            except:
                pass
        else:
            # 建立新表 - 使用 PyArrow schema
            schema = pa.schema([
                ("id", pa.string()),
                ("file_path", pa.string()),
                ("content", pa.string()),
                ("location", pa.string()),
                ("palace_room", pa.string()),
                ("title", pa.string()),
                ("keywords", pa.string()),
                ("vector", pa.list_(pa.float32(), 384)),
            ])
            self.table = self.db.create_table("documents", schema=schema)
            print("已建立新LanceDB表")
    
    def _get_embedding(self, text: str) -> List[float]:
        """取得文字的向量embedding"""
        if self.model is None:
            return np.random.randn(384).tolist()
        
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()
    
    def _extract_title(self, content: str, file_path: str = "") -> str:
        """從內容中提取標題"""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
            if line.startswith('## '):
                return line[3:].strip()
        
        if file_path:
            return Path(file_path).stem
        return "Untitled"
    
    def _extract_keywords(self, content: str) -> List[str]:
        """提取關鍵詞"""
        import re
        # 使用更簡單的方式，避免 Unicode 範圍問題
        words = content.split()
        chinese_words = []
        english_words = []
        
        for word in words:
            # 判斷是否為中文
            if any('\u4e00' <= c <= '\u9fff' for c in word) and len(word) >= 2:
                chinese_words.append(word)
            # 判斷是否為英文
            elif word.isalpha() and len(word) >= 3:
                english_words.append(word.lower())
        
        keywords = list(set(chinese_words[:20] + english_words[:20]))
        return keywords
    
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
    
    def index_file(self, file_path: str, force: bool = False) -> bool:
        """索引單個檔案到向量資料庫"""
        try:
            path = Path(file_path)
            if not path.exists():
                return False
            
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if len(content) < 10:
                return False
            
            file_hash = hashlib.md5(content.encode()).hexdigest()[:12]
            doc_id = f"doc_{file_hash}"
            
            # 檢查是否已存在
            if not force:
                try:
                    existing = self.table.to_pandas()
                    if doc_id in existing["id"].values:
                        return False
                except:
                    pass
            
            title = self._extract_title(content, str(path))
            keywords = self._extract_keywords(content)
            location = str(path.relative_to(self.base_path.parent))
            palace_room = self._get_palace_room(location)
            vector = self._get_embedding(content[:5120])
            
            self.table.add([
                {
                    "id": doc_id,
                    "file_path": str(path),
                    "content": content[:10000],
                    "location": location,
                    "palace_room": palace_room,
                    "title": title,
                    "keywords": json.dumps(keywords),
                    "vector": vector,
                }
            ])
            
            return True
            
        except Exception as e:
            print(f"索引錯誤: {file_path} - {e}")
            return False
    
    def index_all(self, paths: List[str] = None) -> Dict:
        """索引所有檔案"""
        if paths is None:
            paths = [
                self.base_path / "Sumo_wiki" / "concepts",
                self.base_path / "Sumo_wiki" / "summaries",
                self.base_path / "closet",
                self.base_path / "drawer",
                self.base_path / "learning",
                self.base_path / "research",
                self.base_path / "docs",
            ]
        
        stats = {"indexed": 0, "skipped": 0, "errors": 0}
        
        for base in paths:
            if not base.exists():
                print(f"路徑不存在: {base}")
                continue
            
            print(f"索引: {base}")
            
            for ext in ['.md', '.txt', '.yaml', '.json']:
                for file in base.rglob(f"*{ext}"):
                    try:
                        if self.index_file(str(file)):
                            stats["indexed"] += 1
                            if stats["indexed"] % 10 == 0:
                                print(f"  已索引 {stats['indexed']} 個檔案")
                        else:
                            stats["skipped"] += 1
                    except Exception as e:
                        stats["errors"] += 1
        
        return stats
    
    def search(self, query: str, top_k: int = None, palace_room: str = None) -> List[Dict]:
        """向量搜尋"""
        if self.table is None or self.model is None:
            print("向量搜尋未初始化")
            return []
        
        top_k = top_k or CONFIG["top_k"]
        query_vector = self._get_embedding(query)
        
        try:
            results = self.table.search(query_vector) \
                .where(f"palace_room = '{palace_room}'" if palace_room else "TRUE") \
                .limit(top_k) \
                .to_list()
            
            formatted_results = []
            for r in results:
                formatted_results.append({
                    "id": r.get("id"),
                    "file_path": r.get("file_path"),
                    "title": r.get("title"),
                    "location": r.get("location"),
                    "palace_room": r.get("palace_room"),
                    "keywords": json.loads(r.get("keywords", "[]")),
                    "snippet": r.get("content", "")[:200],
                    "score": 1.0 - (r.get("_distance", 0) or 0),
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"搜尋錯誤: {e}")
            return []
    
    def find_similar(self, file_path: str, top_k: int = 5) -> List[Dict]:
        """找相似文章"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            query_vector = self._get_embedding(content[:5120])
            
            results = self.table.search(query_vector) \
                .where(f"file_path != '{file_path}'") \
                .limit(top_k) \
                .to_list()
            
            formatted_results = []
            for r in results:
                formatted_results.append({
                    "file_path": r.get("file_path"),
                    "title": r.get("title"),
                    "palace_room": r.get("palace_room"),
                    "keywords": json.loads(r.get("keywords", "[]")),
                    "score": 1.0 - (r.get("_distance", 0) or 0),
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"相似文章搜尋錯誤: {e}")
            return []
    
    def hybrid_search(self, query: str, top_k: int = None) -> Dict:
        """混合搜尋（向量 + 關鍵詞）"""
        vector_results = self.search(query, top_k)
        keyword_matches = self._keyword_match(query)
        
        combined = []
        seen_paths = set()
        
        for r in vector_results:
            r["source"] = "vector"
            r["final_score"] = r["score"] * 0.6
            if r["file_path"] not in seen_paths:
                seen_paths.add(r["file_path"])
                combined.append(r)
        
        for r in keyword_matches:
            if r["file_path"] not in seen_paths:
                seen_paths.add(r["file_path"])
                r["source"] = "keyword"
                r["final_score"] = 0.4
                combined.append(r)
        
        combined.sort(key=lambda x: x.get("final_score", 0), reverse=True)
        
        return {
            "query": query,
            "results": combined[:top_k or CONFIG["top_k"]],
            "total": len(combined),
        }
    
    def _keyword_match(self, query: str) -> List[Dict]:
        """簡單關鍵詞匹配"""
        try:
            results = self.table.search(query).limit(CONFIG["top_k"]).to_list()
            formatted = []
            for r in results:
                formatted.append({
                    "file_path": r.get("file_path"),
                    "title": r.get("title"),
                    "palace_room": r.get("palace_room"),
                    "keywords": json.loads(r.get("keywords", "[]")),
                })
            return formatted
        except:
            return []
    
    def get_stats(self) -> Dict:
        """取得索引統計"""
        try:
            df = self.table.to_pandas()
            return {
                "total_documents": len(df),
                "by_room": df["palace_room"].value_counts().to_dict() if "palace_room" in df.columns else {},
                "lance_path": str(self.lance_path),
            }
        except Exception as e:
            return {"error": str(e)}
    
    def close(self):
        """關閉資料庫"""
        pass


def main():
    """測試主程式"""
    print("=" * 50)
    print("SumoNoteBook LanceDB 向量搜尋系統")
    print("=" * 50)
    
    if not LANCEDB_AVAILABLE or not SENTENCE_TRANSFORMERS_AVAILABLE:
        print("缺少必要套件，無法運行")
        return
    
    search = LanceDBVectorSearch()
    
    # 測試索引
    print("\n正在索引檔案...")
    stats = search.index_all()
    print(f"已索引: {stats['indexed']} 個檔案")
    
    # 取得統計
    print("\n索引統計:")
    stats_info = search.get_stats()
    print(f"  總文檔數: {stats_info.get('total_documents', 0)}")
    print(f"  按房間: {stats_info.get('by_room', {})}")
    
    # 測試搜尋
    print("\n測試向量搜尋: '蘇茉 學習'")
    results = search.search("蘇茉 學習")
    print(f"找到 {len(results)} 個結果")
    for r in results[:3]:
        print(f"  - {r.get('title', 'N/A')} (相似度: {r.get('score', 0):.2f})")
    
    print("\n測試完成")
    search.close()


if __name__ == "__main__":
    main()