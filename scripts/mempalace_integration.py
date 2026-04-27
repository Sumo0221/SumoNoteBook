"""
MemPalace 與 SumoNoteBook 整合模組

功能：
- 讓 MemPalace 可以存取 SumoNoteBook 知識庫
- 提供統一 API 查詢介面

使用方法：
    from mempalace_integration import MemPalaceClient, SumoNoteBookClient
    
    # 建立客戶端
    client = MemPalaceClient(workspace="engineer")
    
    # 查詢 SumoNoteBook
    results = client.query_notebook("python 程式設計")
    print(results)
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pathlib import Path

# 設定路徑
SCRIPT_DIR = Path(__file__).parent
SUMO_NOTEBOOK_DIR = SCRIPT_DIR.parent
QUERY_INTERFACE = SUMO_NOTEBOOK_DIR / "scripts" / "query_interface.py"


class SumoNoteBookClient:
    """SumoNoteBook 客戶端"""
    
    def __init__(self, vault_path: Optional[str] = None):
        """
        初始化客戶端
        
        Args:
            vault_path: Vault 路徑，預設為 SumoNoteBook 目錄
        """
        self.vault_path = Path(vault_path) if vault_path else SUMO_NOTEBOOK_DIR
    
    def query(self, keyword: str, count: int = 10) -> str:
        """
        關鍵詞搜尋
        
        Args:
            keyword: 搜尋關鍵詞
            count: 回傳結果數量
            
        Returns:
            搜尋結果
        """
        if not QUERY_INTERFACE.exists():
            return f"Error: query_interface.py not found at {QUERY_INTERFACE}"
        
        # 使用 subprocess 執行查詢
        import subprocess
        cmd = [
            "python",
            str(QUERY_INTERFACE),
            keyword
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(SUMO_NOTEBOOK_DIR)
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Error: {str(e)}"
    
    def dataview(self, query: str) -> str:
        """
        Dataview 風格查詢
        
        Args:
            query: Dataview 語法查詢
            
        Returns:
            查詢結果
        """
        return self.query(f"DATAVIEW {query}")
    
    def list_notes(self, folder: str = "summaries", limit: int = 10) -> str:
        """
        列出筆記
        
        Args:
            folder: 資料夾名稱
            limit: 結果數量限制
            
        Returns:
           筆記列表
        """
        return self.query(f"LIST FROM {folder} LIMIT {limit}")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        取得 Vault 統計資訊
        
        Returns:
            統計資訊字典
        """
        # 計算基礎統計
        stats = {
            "vault_path": str(self.vault_path),
            "rooms": [],
            "total_notes": 0,
        }
        
        # 讀取 mempalace.yaml 取得房間列表
        config_path = self.vault_path / "mempalace.yaml"
        if config_path.exists():
            import yaml
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                stats["rooms"] = [r.get("name", "unknown") for r in config.get("rooms", [])]
            except Exception:
                pass
        
        # 計算總筆記數
        for room in stats["rooms"]:
            room_path = self.vault_path / room
            if room_path.exists():
                stats["total_notes"] += len(list(room_path.glob("*.md")))
        
        return stats
    
    def search_concepts(self, concept: str) -> List[Dict[str, str]]:
        """
        搜尋關聯概念
        
        Args:
            concept: 概念名稱
            
        Returns:
            相關檔案列表
        """
        results = []
        concepts_path = self.vault_path / "concepts"
        
        if not concepts_path.exists():
            return results
        
        # 搜尋包含該概念的筆記
        for md_file in concepts_path.glob("*.md"):
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                if concept.lower() in content.lower():
                    results.append({
                        "file": md_file.name,
                        "path": str(md_file),
                    })
            except Exception:
                continue
        
        return results


class MemPalaceClient:
    """MemPalace 客戶端 - 整合 SumoNoteBook"""
    
    def __init__(self, workspace: str = "engineer"):
        """
        初始化客戶端
        
        Args:
            workspace: workspace 名稱
        """
        # 找 workspace 的 mempalace 目錄
        openclaw_dir = Path(os.path.expanduser("~/.openclaw"))
        self.mempalace_dir = openclaw_dir / f"workspace_{workspace}" / "mempalace"
        
        if not self.mempalace_dir.exists():
            raise ValueError(f"MemPalace not found for workspace: {workspace}")
        
        # 建立 SumoNoteBook 客戶端
        self.notebook = SumoNoteBookClient()
        
    def get_rooms(self) -> List[str]:
        """
        取得所有房間
        
        Returns:
            房間名稱列表
        """
        config_path = self.mempalace_dir / "mempalace.yaml"
        if not config_path.exists():
            return []
        
        import yaml
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            return [r.get("name", "unknown") for r in config.get("rooms", [])]
        except Exception:
            return []
    
    def query_notebook(self, keyword: str) -> str:
        """
        查詢 SumoNoteBook 知識庫
        
        Args:
            keyword: 搜尋關鍵詞
            
        Returns:
            搜尋結果
        """
        return self.notebook.query(keyword)
    
    def search_in_room(self, room: str, query: str) -> str:
        """
        在特定房間搜尋
        
        Args:
            room: 房間名稱
            query: 查詢語法
            
        Returns:
            搜尋結果
        """
        return self.notebook.dataview(f"{query} FROM {room}")
    
    def get_notebook_stats(self) -> Dict[str, Any]:
        """
        取得 SumoNoteBook 統計
        
        Returns:
            統計資訊
        """
        return self.notebook.get_stats()


def get_client(workspace: str = "engineer") -> MemPalaceClient:
    """
    建立 MemPalace 客戶端的工廠函數
    
    Args:
        workspace: workspace 名稱
        
    Returns:
        MemPalaceClient 實例
    """
    return MemPalaceClient(workspace=workspace)


if __name__ == "__main__":
    # 測試範例
    print("=== MemPalace + SumoNoteBook 整合測試 ===\n")
    
    try:
        # 建立客戶端
        client = get_client("engineer")
        
        # 顯示房間
        rooms = client.get_rooms()
        print(f"📁 MemPalace Rooms: {', '.join(rooms)}\n")
        
        # 顯示統計
        stats = client.get_notebook_stats()
        print(f"📊 SumoNoteBook Stats:")
        print(f"   - 路徑: {stats['vault_path']}")
        print(f"   - 房間數: {len(stats['rooms'])}")
        print(f"   - 總筆記: {stats['total_notes']}\n")
        
        # 測試搜尋
        print("🔍 搜尋 'python':")
        result = client.query_notebook("python")
        print(result[:500] if len(result) > 500 else result)
        
    except Exception as e:
        print(f"Error: {e}")