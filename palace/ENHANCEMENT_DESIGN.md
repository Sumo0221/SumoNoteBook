# SumoNoteBook 強化計劃 - 記憶宮殿化方案

> 設計者：高工蘇茉  
> 日期：2026-04-09  
> 版本：1.0

---

## 📋 現狀分析

### 現有結構
```
SumoNoteBook/
├── raw/                    # 原始資料（老爺放置）
│   ├── processed/         # 已處理檔案
│   └── shared/           # 共享資料
├── wiki/                  # 目前未使用
├── Sumo_wiki/            # 結構化知識庫（主要使用）
│   ├── concepts/         # 概念原子筆記
│   ├── summaries/       # 檔案摘要
│   ├── backlinks/       # 反向連結
│   ├── qa/              # 問答記錄
│   ├── research/        # 研究資料
│   ├── shared/          # 共享知識
│   ├── workflows/       # 工作流
│   └── prompts/         # 提示詞
├── scripts/              # Python 腳本
└── mempalace.yaml       # MemPalace 房間設定
```

### 現有問題
1. **無空間邏輯** - 只有資料夾，沒有「位置」概念
2. **檢索單一** - 只有關鍵詞搜尋，缺乏語義理解
3. **Closet/Drawer 混合** - 資料存放沒有明確分類

---

## 🏛️ 記憶宮殿化方案

### 核心概念：Location = Memory

**Loci（記憶位置）**：
- 每個位置（Location）代表一個知識領域
- 每個位置可容納多個概念（Items）
- 位置之間可建立連結（Navigation）

### 設計架構

```
┌─────────────────────────────────────────────────────────┐
│                    SUMONOTEBOOK                          │
│                   記憶宮殿總覽                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   CLOSET    │    │   DRAWER    │    │   PALACE    │ │
│  │   (衣櫃)    │    │   (抽屜)    │    │   (宮殿)    │ │
│  │             │    │             │    │             │ │
│  │  長期知識   │    │  臨時工作   │    │  主動召回   │ │
│  │  分類儲存   │    │  階段任務   │    │  空間導覽   │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🗄️ Closet（衣櫃）- 長期知識儲存

### 設計原則
- **分類存放** - 類似衣櫃分區：正裝、休閒、運動
- **標籤化** - 每個知識 item 有多個標籤
- **長期維護** - 不輕易刪除，只標記過時

### Closet 結構

```
closet/
├── formal/           # 正式知識（蘇茉家族官方資訊）
│   ├── agents/      # 各蘇茉設定
│   ├── skills/      # 技能定義
│   └── workflows/  # 工作流程
├── casual/          # 休閒知識（生活、興趣）
│   ├── life/        # 生活記錄
│   ├── hobby/       # 興趣愛好
│   └── travel/      # 旅行記錄
├── work/            # 工作相關
│   ├── projects/    # 專案記錄
│   ├── tech/        # 技術筆記
│   └── meetings/   # 會議記錄
└── archive/         # 歸檔（過時但不刪除）
    └── 2026_01/    # 按月份歸檔
```

### Closet Metadata Schema

```yaml
closet_item:
  id: "uuid"
  name: "知識名稱"
  category: "formal|casual|work|archive"
  tags: ["標籤1", "標籤2"]
  location: "closet/formal/agents/"
  created: "2026-04-09"
  updated: "2026-04-09"
  status: "active|archived|deprecated"
  links: ["相關知識ID"]
```

---

## 🗃️ Drawer（抽屜）- 臨時工作區

### 設計原則
- **短期任務** - 類似抽屜放當前處理的文件
- **易取易放** - 快速存取，不強調分類
- **定期清理** - 任務結束後歸檔或刪除

### Drawer 結構

```
drawer/
├── inbox/           # 收件匣（新知識待處理）
├── processing/     # 處理中
│   └── current/    # 當前任務
├── drafts/         # 草稿（未完成的知識）
├── scratch/        # 速記（臨時メモ）
└── temp/           # 暫存（可定期清除）
```

### Drawer 使用規則

| 目錄 | 用途 | 清理週期 |
|------|------|----------|
| inbox | 新收到的知識 | 每日整理 |
| processing/current | 正在處理的任務 | 任務完成後移出 |
| drafts | 未完成的筆記 | 每週檢視 |
| scratch | 臨時メモ | 每日清除 |
| temp | 暫存檔案 | 每次使用前清除 |

---

## 🏛️ Palace（宮殿）- 主動召回系統

### 設計原則
- **空間導覽** - 類似記憶宮殿的「 walking through」
- **視覺化** - 每個房間代表一個知識領域
- **主動召回** - 依位置索引，而非關鍵詞

### Palace 結構（参考 MemPalace）

```yaml
palace:
  name: "SumoNoteBook Palace"
  description: "蘇茉家族知識宮殿"
  
  rooms:
    - name: " Entrance 大門"
      description: "入口大廳 - 總索引"
      items:
        - "最新知識"
        - "常用概念"
        
    - name: "Library 圖書館"
      description: "概念知識庫"
      items:
        - concepts/
        - summaries/
        
    - name: "Workshop 工坊"
      description: "工作區"
      items:
        - workflows/
        - prompts/
        
    - name: "Garden 花園"
      description: "休閒區"
      items:
        - life/
        - hobby/
```

### Palace Navigation

```python
# 範例：宮殿漫遊
def palace_walk(start_room="Entrance", max_rooms=3):
    """
    模擬在宮殿中走動，回傳沿途遇到的知識
    """
    path = []
    current = start_room
    
    for _ in range(max_rooms):
        room = get_room(current)
        items = get_items_in_room(room)
        path.append({"room": room.name, "items": items})
        
        # 隨機選擇下一個房間（基於連結）
        current = random.choice(room.connections)
    
    return path
```

---

## 🔍 雙索引檢索系統

### 設計架構

```
┌─────────────────────────────────────────────┐
│            雙索引檢索引擎                     │
├─────────────────────────────────────────────┤
│                                              │
│  ┌─────────────┐      ┌─────────────┐      │
│  │  Index A    │      │  Index B    │      │
│  │  語義向量    │  +   │  關鍵詞索引  │      │
│  │  (Semantic) │      │  (Keyword)  │      │
│  └─────────────┘      └─────────────┘      │
│         │                    │               │
│         └────────┬───────────┘               │
│                  ▼                            │
│         ┌─────────────┐                      │
│         │   Hybrid    │                      │
│         │   Ranking   │                      │
│         └─────────────┘                      │
│                  │                            │
│                  ▼                            │
│         ┌─────────────┐                      │
│         │  融合結果   │                      │
│         └─────────────┘                      │
└─────────────────────────────────────────────┘
```

### Index A: 語義向量索引（Vector Search）

**使用技術**：LanceDB（已有 memory-lancedb-pro-fork）

**向量維度**：1536（text-embedding-3-small）

**Index Schema**：
```python
{
    "id": "uuid",
    "text": "知識內容",
    "embedding": [0.1, 0.2, ...],  # 1536維
    "location": "closet/formal/agents/",
    "palace_room": "Library",
    "keywords": ["關鍵詞1", "關鍵詞2"],
    "metadata": {
        "source": "summaries/abc123.md",
        "created": "2026-04-09",
        "tags": ["蘇茉", "設定"]
    }
}
```

### Index B: 關鍵詞索引（Keyword Search）

**使用技術**：FUSE.js（模糊搜尋）或 SQLite FTS5

**Index Schema**：
```python
{
    "id": "uuid",
    "text": "知識內容（用於全文檢索）",
    "keywords": ["關鍵詞1", "關鍵詞2"],  # 提取的關鍵詞
    "ngrams": ["二元組", "三元組"],        # n-gram 索引
    "location": "closet/formal/agents/",
    "type": "concept|summary|qa"
}
```

### Hybrid Ranking Algorithm

```python
def hybrid_search(query, vector_weight=0.6, keyword_weight=0.4):
    """
    混合搜尋排名
    
    Args:
        query: 搜尋查詢
        vector_weight: 語義搜尋權重
        keyword_weight: 關鍵詞搜尋權重
    
    Returns:
        融合排序後的結果
    """
    # 1. 語義向量搜尋
    vector_results = vector_search(query, top_k=20)
    
    # 2. 關鍵詞搜尋
    keyword_results = keyword_search(query, top_k=20)
    
    # 3. 結果融合
    combined = []
    all_ids = set(v['id'] for v in vector_results) | set(k['id'] for k in keyword_results)
    
    for id in all_ids:
        v_score = vector_results.get(id, 0)
        k_score = keyword_results.get(id, 0)
        
        # 標準化並加权
        final_score = (v_score * vector_weight) + (k_score * keyword_weight)
        combined.append({"id": id, "score": final_score})
    
    # 4. 排序返回
    return sorted(combined, key=lambda x: x["score"], reverse=True)
```

---

## 📁 新目錄結構

```
SumoNoteBook/
├── closet/                    # 🗄️ 衣櫃（長期知識）
│   ├── formal/               # 正式知識
│   │   ├── agents/          # 蘇茉家族
│   │   ├── skills/          # 技能
│   │   └── workflows/       # 工作流
│   ├── casual/              # 休閒知識
│   ├── work/                # 工作相關
│   └── archive/             # 歸檔
│
├── drawer/                   # 🗃️ 抽屜（臨時工作）
│   ├── inbox/               # 收件匣
│   ├── processing/         # 處理中
│   ├── drafts/             # 草稿
│   ├── scratch/            # 速記
│   └── temp/               # 暫存
│
├── palace/                   # 🏛️ 宮殿（空間導覽）
│   ├── config.yaml         # 宮殿設定
│   ├── rooms/              # 房間定義
│   └── navigation.py       # 導覽腳本
│
├── raw/                     # 原始資料（保持不變）
│
├── Sumo_wiki/              # 結構化知識（保持不變）
│
└── index.db                # 雙索引資料庫
```

---

## 🚀 實作計劃

### Phase 1: Closet/Drawer 分離（第1天）
- [ ] 建立 closet/ 目錄結構
- [ ] 建立 drawer/ 目錄結構
- [ ] 遷移現有資料到 closet/
- [ ] 制定分類規則

### Phase 2: Palace 空間化（第2天）
- [ ] 建立 palace/config.yaml
- [ ] 定義房間和連結
- [ ] 實作空間導覽功能

### Phase 3: 雙索引檢索（第3天）
- [ ] 擴展 LanceDB Schema（新增 location/palace_room）
- [ ] 建立關鍵詞索引（SQLite FTS5）
- [ ] 實作混合搜尋演算法

### Phase 4: 整合測試（第4天）
- [ ] 整合進現有 scripts/
- [ ] 測試所有功能
- [ ] 更新文件

---

## 📝 技術細節

### 目錄遷移腳本

```python
# migrate_to_closet.py
import os
import shutil

MAPPING = {
    "Sumo_wiki/concepts/": "closet/formal/concepts/",
    "Sumo_wiki/summaries/": "closet/formal/summaries/",
    "Sumo_wiki/shared/": "closet/casual/shared/",
    "Sumo_wiki/workflows/": "closet/work/workflows/",
}

def migrate():
    for source, dest in MAPPING.items():
        if os.path.exists(source):
            shutil.move(source, dest)
            print(f"Moved: {source} -> {dest}")
```

### 雙索引搜尋腳本

```python
# dual_index_search.py
import lancedb
import sqlite3

class DualIndexSearch:
    def __init__(self, db_path="index.db"):
        self.lance_db = lancedb.connect("data/lance")
        self.sqlite_conn = sqlite3.connect(db_path)
        
    def search(self, query, top_k=10):
        vector_results = self.vector_search(query, top_k)
        keyword_results = self.keyword_search(query, top_k)
        return self.hybrid_ranking(vector_results, keyword_results)
```

---

## ⚠️ 注意事項

1. **現有資料不刪除** - 遷移時保留備份
2. **漸進式遷移** - 逐步轉移，不要一次大規模變動
3. **保持向後相容** - 舊的搜尋方式仍可用
4. **定期清理 drawer** - 避免臨時資料堆積

---

*高工蘇茉，2026-04-09*