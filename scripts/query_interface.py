"""
SumoNoteBook 統一查詢介面 (RDT 升級版)
Unified Query Interface for SumoNoteBook with RDT Enhancement

作者：工程師蘇茉
日期：2026-04-22

RDT (Recursive Depth Transformer) 概念應用：
- Prelude: 初始搜尋階段，建立基礎理解
- Recurrent Block: 迭代深化，根據初步結果優化查詢
- Coda: 最終整合輸出，聚合多文件資訊

功能：
- 語義搜尋（向量搜尋）
- 關鍵詞搜尋（FTS5）
- 混合模式（兩者結合）
- RDT 迭代深化模式（新功能！）
- 自然語言介面
"""

import os
import json
import sqlite3
import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import time

# ============================================================================
# 配置
# ============================================================================
CONFIG = {
    "base_path": "C:\\butler_sumo\\library\\SumoNoteBook",
    "lance_path": "C:\\butler_sumo\\library\\SumoNoteBook\\data\\sumo_notebook.lance",
    "db_path": "C:\\butler_sumo\\library\\SumoNoteBook\\data\\index.db",
    "vector_weight": 0.6,
    "keyword_weight": 0.4,
    "top_k": 10,
    "min_query_length_for_hybrid": 10,
    # RDT 配置（新功能！）
    "rdt_max_iterations": 3,        # 最大迭代次數
    "rdt_iteration_threshold": 0.7,   # 分數閾值，低於此值開始迭代
    "rdt_context_window": 3,        # 每個文件取用的上下文窗口
    "rdt_convergence_threshold": 0.05,  # 收斂閾值
}

# ============================================================================
# 嘗試導入必要套件
# ============================================================================
try:
    import lancedb
    LANCEDB_AVAILABLE = True
except ImportError:
    LANCEDB_AVAILABLE = False
    print("LanceDB not installed")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("sentence-transformers not installed")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("numpy not installed")

try:
    import pyarrow as pa
    PYARROW_AVAILABLE = True
except ImportError:
    PYARROW_AVAILABLE = False
    print("pyarrow not installed")


# ============================================================================
# 搜尋模式枚舉
# ============================================================================
class SearchMode(Enum):
    SEMANTIC = "semantic"
    KEYWORD = "keyword"
    HYBRID = "hybrid"
    AUTO = "auto"
    RDT = "rdt"


@dataclass
class RDTIteration:
    iteration: int
    query: str
    results: List[Dict]
    avg_score: float
    context: str
    is_converged: bool = False


@dataclass
class RDTResult:
    original_query: str
    iterations: List[RDTIteration]
    final_results: List[Dict]
    total_iterations: int
    converged: bool
    processing_time: float
    reasoning_trace: List[str] = field(default_factory=list)


@dataclass
class SearchResult:
    file_path: str
    title: str
    snippet: str
    score: float
    source: str
    palace_room: str
    keywords: List[str]
    location: str


@dataclass
class SearchResponse:
    query: str
    mode: str
    results: List[SearchResult]
    total: int
    processing_time: float


# ============================================================================
# LanceDB 向量搜尋引擎
# ============================================================================
class LanceDBEngine:
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path or CONFIG["base_path"])
        self.lance_path = Path(CONFIG["lance_path"])
        self.lance_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.model = None
        self.db = None
        self.table = None
        
        self._init()
    
    def _init(self):
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
                print("Vector model loaded")
            except Exception as e:
                print(f"Vector model load failed: {e}")
        
        if LANCEDB_AVAILABLE:
            try:
                self.db = lancedb.connect(str(self.lance_path))
                table_names = self.db.list_tables() if hasattr(self.db, 'list_tables') else []
                if "documents" in table_names:
                    self.table = self.db.open_table("documents")
                    print("LanceDB table opened")
                else:
                    self._create_table()
            except Exception as e:
                print(f"LanceDB connect failed: {e}")
    
    def _create_table(self):
        try:
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
            print("New LanceDB table created")
        except Exception as e:
            print(f"Create table failed: {e}")
    
    def _get_embedding(self, text: str) -> List[float]:
        if self.model is None:
            return np.random.randn(384).tolist() if NUMPY_AVAILABLE else [0.0] * 384
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()
    
    def search(self, query: str, top_k: int = None, palace_room: str = None) -> List[Dict]:
        if self.table is None or self.model is None:
            return []
        
        top_k = top_k or CONFIG["top_k"]
        query_vector = self._get_embedding(query)
        
        try:
            where_clause = f"palace_room = '{palace_room}'" if palace_room else "TRUE"
            results = self.table.search(query_vector) \
                .where(where_clause) \
                .limit(top_k) \
                .to_list()
            
            formatted = []
            for r in results:
                formatted.append({
                    "file_path": r.get("file_path"),
                    "title": r.get("title"),
                    "snippet": r.get("content", "")[:200],
                    "score": 1.0 - (r.get("_distance", 0) or 0),
                    "source": "vector",
                    "palace_room": r.get("palace_room"),
                    "keywords": json.loads(r.get("keywords", "[]")),
                    "location": r.get("location"),
                })
            return formatted
        except Exception as e:
            print(f"Vector search error: {e}")
            return []
    
    def is_ready(self) -> bool:
        return self.model is not None and self.table is not None


# ============================================================================
# FTS5 關鍵詞搜尋引擎
# ============================================================================
class FTS5Engine:
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path or CONFIG["base_path"])
        self.db_path = Path(CONFIG["db_path"])
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._init()
    
    def _init(self):
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS fts_index 
            USING fts5(file_path, content, keywords, location, title)
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS keyword_index (
                id TEXT PRIMARY KEY,
                file_path TEXT NOT NULL,
                content TEXT,
                keywords TEXT,
                location TEXT,
                palace_room TEXT,
                title TEXT,
                metadata TEXT
            )
        """)
        
        self.conn.commit()
    
    def search(self, query: str, top_k: int = None) -> List[Dict]:
        top_k = top_k or CONFIG["top_k"]
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                SELECT file_path, title, snippet(fts_index, 2, '[', ']', '...', 20) as snippet
                FROM fts_index
                WHERE fts_index MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (query, top_k))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "file_path": row[0],
                    "title": row[1] or Path(row[0]).stem,
                    "snippet": row[2] or "",
                    "score": 0.9,
                    "source": "keyword",
                    "palace_room": self._get_palace_room(row[0]),
                    "keywords": [],
                    "location": row[0],
                })
            return results
        except Exception as e:
            print(f"Keyword search error: {e}")
            return []
    
    def _get_palace_room(self, location: str) -> str:
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
        elif 'sumo_wiki' in location_lower:
            return 'library'
        else:
            return 'entrance'
    
    def close(self):
        self.conn.close()


# ============================================================================
# RDT 迭代深化引擎（新功能！）
# ============================================================================
class RDTEngine:
    """
    RDT 迭代深化引擎
    
    根據 Recurrent Depth Transformer 概念：
    - Prelude: 初始搜尋
    - Recurrent Block: 根據結果持續優化查詢
    - Coda: 整合所有迭代結果
    """
    
    def __init__(self, vector_engine: LanceDBEngine, keyword_engine: FTS5Engine):
        self.vector_engine = vector_engine
        self.keyword_engine = keyword_engine
        
        self.max_iterations = CONFIG["rdt_max_iterations"]
        self.iteration_threshold = CONFIG["rdt_iteration_threshold"]
        self.convergence_threshold = CONFIG["rdt_convergence_threshold"]
        self.context_window = CONFIG["rdt_context_window"]
    
    def search(self, query: str, top_k: int = None) -> RDTResult:
        start_time = time.time()
        top_k = top_k or CONFIG["top_k"]
        
        iterations = []
        reasoning_trace = []
        
        # === Stage 1: Prelude（初始搜尋）===
        reasoning_trace.append(f"[Prelude] Initial query: {query}")
        
        initial_results = self._hybrid_search(query, top_k, None)
        
        if not initial_results:
            return RDTResult(
                original_query=query,
                iterations=[],
                final_results=[],
                total_iterations=0,
                converged=False,
                processing_time=time.time() - start_time,
                reasoning_trace=reasoning_trace,
            )
        
        avg_score = sum(r["score"] for r in initial_results) / len(initial_results)
        
        iterations.append(RDTIteration(
            iteration=0,
            query=query,
            results=initial_results,
            avg_score=avg_score,
            context=self._build_context(initial_results),
            is_converged=False,
        ))
        
        reasoning_trace.append(f"[Prelude] Found {len(initial_results)} results, avg score: {avg_score:.3f}")
        
        # === Stage 2: Recurrent Block（迭代深化）===
        current_query = query
        current_results = initial_results
        prev_avg_score = avg_score
        convergence_count = 0
        
        for i in range(1, self.max_iterations):
            optimized_query = self._optimize_query(current_query, current_results)
            reasoning_trace.append(f"[Iteration {i}] Optimized query: {optimized_query}")
            
            new_results = self._hybrid_search(optimized_query, top_k, None)
            
            if not new_results:
                reasoning_trace.append(f"[Iteration {i}] No new results, stop")
                break
            
            new_avg_score = sum(r["score"] for r in new_results) / len(new_results)
            
            score_diff = abs(new_avg_score - prev_avg_score)
            is_converged = score_diff < self.convergence_threshold
            
            if is_converged:
                convergence_count += 1
                reasoning_trace.append(f"[Iteration {i}] Converged (diff: {score_diff:.4f})")
            else:
                convergence_count = 0
            
            iterations.append(RDTIteration(
                iteration=i,
                query=optimized_query,
                results=new_results,
                avg_score=new_avg_score,
                context=self._build_context(new_results),
                is_converged=is_converged,
            ))
            
            if convergence_count >= 2:
                reasoning_trace.append(f"[Coda] Converged, stop iteration")
                break
            
            current_query = optimized_query
            current_results = new_results
            prev_avg_score = new_avg_score
        
        # === Stage 3: Coda（整合結果）===
        final_results = self._merge_iterations(iterations, top_k)
        converged = iterations[-1].is_converged if iterations else False
        
        reasoning_trace.append(f"[Coda] Integration done, {len(final_results)} final results")
        
        return RDTResult(
            original_query=query,
            iterations=iterations,
            final_results=final_results,
            total_iterations=len(iterations),
            converged=converged,
            processing_time=time.time() - start_time,
            reasoning_trace=reasoning_trace,
        )
    
    def _hybrid_search(
        self,
        query: str,
        top_k: int,
        palace_room: str,
    ) -> List[Dict]:
        vector_results = self.vector_engine.search(query, top_k, palace_room)
        keyword_results = self.keyword_engine.search(query, top_k)
        
        combined = []
        seen_paths = set()
        
        for r in vector_results:
            if r["file_path"] not in seen_paths:
                seen_paths.add(r["file_path"])
                r["final_score"] = r["score"] * CONFIG["vector_weight"]
                r["source"] = "hybrid_vector"
                combined.append(r)
        
        for r in keyword_results:
            if r["file_path"] not in seen_paths:
                seen_paths.add(r["file_path"])
                r["final_score"] = r["score"] * CONFIG["keyword_weight"]
                r["source"] = "hybrid_keyword"
                combined.append(r)
        
        combined.sort(key=lambda x: x.get("final_score", 0), reverse=True)
        return combined
    
    def _optimize_query(self, original_query: str, results: List[Dict]) -> str:
        keywords = set()
        
        for r in results[:self.context_window]:
            title = r.get("title", "")
            snippet = r.get("snippet", "")
            
            words = re.findall(r"[\u4e00-\u9fffA-Za-z]{2,}", f"{title} {snippet}")
            keywords.update(words[:5])
        
        if keywords:
            top_keywords = list(keywords)[:3]
            return f"{original_query} {' '.join(top_keywords)}"
        
        return original_query
    
    def _build_context(self, results: List[Dict]) -> str:
        contexts = []
        for r in results[:self.context_window]:
            context = f"{r.get('title', '')}: {r.get('snippet', '')[:100]}"
            contexts.append(context)
        return " | ".join(contexts)
    
    def _merge_iterations(self, iterations: List[RDTIteration], top_k: int) -> List[Dict]:
        combined = {}
        
        for idx, it in enumerate(iterations):
            weight = 1.0 + (idx * 0.2)
            
            for r in it.results:
                path = r["file_path"]
                if path not in combined:
                    combined[path] = r.copy()
                    combined[path]["iteration_scores"] = []
                
                combined[path]["iteration_scores"].append(r["score"])
                combined[path]["final_score"] = (
                    combined[path].get("final_score", 0) + r["score"] * weight
                )
        
        final_list = list(combined.values())
        final_list.sort(key=lambda x: x.get("final_score", 0), reverse=True)
        
        return final_list[:top_k]


# ============================================================================
# 統一查詢介面
# ============================================================================
class UnifiedQueryInterface:
    """
    統一查詢介面
    
    支援多種搜尋模式（包括新增的 RDT 模式）：
    1. 語義搜尋 - 使用向量相似度
    2. 關鍵詞搜尋 - 使用 FTS5 全文檢索
    3. 混合搜尋 - 結合向量和關鍵詞
    4. RDT 搜尋 - 迭代深化（新功能！）
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path or CONFIG["base_path"])
        
        self.vector_engine = LanceDBEngine(str(self.base_path))
        self.keyword_engine = FTS5Engine(str(self.base_path))
        
        # RDT 引擎（新功能！）
        self.rdt_engine = RDTEngine(self.vector_engine, self.keyword_engine)
        
        self.stats = {
            "vector_available": self.vector_engine.is_ready(),
            "keyword_available": True,
            "rdt_available": True,
            "total_searches": 0,
            "rdt_searches": 0,
        }
    
    def _determine_mode(self, query: str) -> SearchMode:
        query_length = len(query.strip())
        
        if query_length < 5:
            return SearchMode.KEYWORD
        
        if query_length < CONFIG["min_query_length_for_hybrid"]:
            if any('\u4e00' <= c <= '\u9fff' for c in query):
                return SearchMode.HYBRID
            return SearchMode.KEYWORD
        
        return SearchMode.RDT
    
    def search(
        self,
        query: str,
        mode: str = "auto",
        top_k: int = None,
        palace_room: str = None,
    ) -> SearchResponse:
        start_time = time.time()
        
        top_k = top_k or CONFIG["top_k"]
        
        if mode == "auto":
            search_mode = self._determine_mode(query)
        else:
            search_mode = SearchMode(mode)
        
        results = []
        
        if search_mode == SearchMode.SEMANTIC:
            results = self.vector_engine.search(query, top_k, palace_room)
        
        elif search_mode == SearchMode.KEYWORD:
            results = self.keyword_engine.search(query, top_k)
            if palace_room:
                results = [r for r in results if r.get("palace_room") == palace_room]
        
        elif search_mode == SearchMode.HYBRID:
            vector_results = self.vector_engine.search(query, top_k, palace_room)
            keyword_results = self.keyword_engine.search(query, top_k)
            
            results = self._merge_results(vector_results, keyword_results)
        
        elif search_mode == SearchMode.RDT:
            rdt_result = self.rdt_engine.search(query, top_k)
            results = rdt_result.final_results
            self.stats["rdt_searches"] += 1
        
        search_results = []
        for r in results:
            search_results.append(SearchResult(
                file_path=r.get("file_path", ""),
                title=r.get("title", ""),
                snippet=r.get("snippet", ""),
                score=r.get("score", r.get("final_score", 0.0)),
                source=r.get("source", search_mode.value),
                palace_room=r.get("palace_room", ""),
                keywords=r.get("keywords", []),
                location=r.get("location", ""),
            ))
        
        processing_time = time.time() - start_time
        self.stats["total_searches"] += 1
        
        return SearchResponse(
            query=query,
            mode=search_mode.value,
            results=search_results,
            total=len(search_results),
            processing_time=processing_time,
        )
    
    def search_rdt(
        self,
        query: str,
        top_k: int = None,
    ) -> RDTResult:
        return self.rdt_engine.search(query, top_k or CONFIG["top_k"])
    
    def _merge_results(
        self,
        vector_results: List[Dict],
        keyword_results: List[Dict],
    ) -> List[Dict]:
        combined = []
        seen_paths = set()
        
        for r in vector_results:
            if r["file_path"] not in seen_paths:
                seen_paths.add(r["file_path"])
                r["final_score"] = r["score"] * CONFIG["vector_weight"]
                r["source"] = "hybrid_vector"
                combined.append(r)
        
        for r in keyword_results:
            if r["file_path"] not in seen_paths:
                seen_paths.add(r["file_path"])
                r["final_score"] = r["score"] * CONFIG["keyword_weight"]
                r["source"] = "hybrid_keyword"
                combined.append(r)
        
        combined.sort(key=lambda x: x.get("final_score", 0), reverse=True)
        
        return combined
    
    def natural_search(self, query: str, use_rdt: bool = False) -> str:
        if use_rdt:
            rdt_result = self.rdt_engine.search(query, CONFIG["top_k"])
            
            if not rdt_result.final_results:
                return f"Sorry, no results found for: {query}"
            
            lines = [f"[Search] Query: {query} (RDT mode)"]
            lines.append(f"Found {len(rdt_result.final_results)} results ({rdt_result.processing_time:.2f}s)")
            lines.append(f"Iterations: {rdt_result.total_iterations}, Converged: {rdt_result.converged}")
            lines.append("")
            
            lines.append("Reasoning trace:")
            for trace in rdt_result.reasoning_trace[:5]:
                lines.append(f"  - {trace}")
            lines.append("")
            
            lines.append("Results:")
            for i, r in enumerate(rdt_result.final_results[:5], 1):
                lines.append(f"{i}. {r.get('title', 'Unknown')}")
                lines.append(f"   Location: {r.get('location', r.get('file_path', ''))}")
                lines.append(f"   Score: {r.get('final_score', r.get('score', 0)):.3f}")
                if r.get('snippet'):
                    lines.append(f"   Excerpt: {r.get('snippet')[:100]}...")
                lines.append("")
            
            return "\n".join(lines)
        else:
            response = self.search(query, mode="auto")
            
            if not response.results:
                return f"Sorry, no results found for: {query}"
            
            lines = [f"[Search] Query: {query} Mode: {response.mode}"]
            lines.append(f"Found {response.total} results ({response.processing_time:.2f}s)")
            lines.append("")
            
            for i, r in enumerate(response.results[:5], 1):
                lines.append(f"{i}. {r.title or Path(r.file_path).stem}")
                lines.append(f"   Location: {r.location}")
                lines.append(f"   Score: {r.score:.2f}")
                if r.snippet:
                    lines.append(f"   Excerpt: {r.snippet[:100]}...")
                lines.append("")
            
            return "\n".join(lines)
    
    def get_stats(self) -> Dict:
        return self.stats
    
    def close(self):
        if hasattr(self.keyword_engine, 'close'):
            self.keyword_engine.close()


# ============================================================================
# 便捷函數
# ============================================================================
_query_interface = None


def get_query_interface() -> UnifiedQueryInterface:
    global _query_interface
    if _query_interface is None:
        _query_interface = UnifiedQueryInterface()
    return _query_interface


def search(query: str, mode: str = "auto", top_k: int = 10) -> SearchResponse:
    interface = get_query_interface()
    return interface.search(query, mode=mode, top_k=top_k)


def search_rdt(query: str, top_k: int = 10) -> RDTResult:
    interface = get_query_interface()
    return interface.search_rdt(query, top_k=top_k)


def natural_search(query: str, use_rdt: bool = False) -> str:
    interface = get_query_interface()
    return interface.natural_search(query, use_rdt=use_rdt)


# ============================================================================
# 命令列介面
# ============================================================================
if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("SumoNoteBook Query Interface v2.0 (RDT Edition)")
    print("=" * 60)
    
    interface = UnifiedQueryInterface()
    
    print(f"\nEngine status:")
    print(f"  - Vector: {'ON' if interface.stats['vector_available'] else 'OFF'}")
    print(f"  - Keyword: {'ON' if interface.stats['keyword_available'] else 'OFF'}")
    print(f"  - RDT: {'ON' if interface.stats['rdt_available'] else 'OFF'}")
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        use_rdt = "--rdt" in sys.argv
        result = interface.natural_search(query, use_rdt=use_rdt)
        print(result)
    else:
        print("\nEnter search query (q to exit):")
        print("Mode: auto/semantic/keyword/hybrid/rdt")
        print("Use --rdt flag to enable RDT mode")
        
        while True:
            try:
                user_input = input("\n> ").strip()
                if user_input.lower() in ['q', 'quit', 'exit']:
                    print("Bye!")
                    break
                if not user_input:
                    continue
                
                use_rdt = "--rdt" in user_input
                if use_rdt:
                    user_input = user_input.replace("--rdt", "").strip()
                
                result = interface.natural_search(user_input, use_rdt=use_rdt)
                print(result)
                
            except KeyboardInterrupt:
                print("\nBye!")
                break
    
    interface.close()