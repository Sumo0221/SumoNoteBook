# MemPalace 記憶宮殿優化方案

> 將 MemPalace 概念應用於 SumoNoteBook 的實作指南
> 版本：1.0 | 建立日期：2026-04-07

---

## 1. 結構差異分析

### 1.1 MemPalace 結構

```
Wing（人物/專案）
├── Room（主題：auth, billing, deploy）
│   ├── Closet（壓縮摘要）
│   └── Drawer（原始檔案）
├── Hall（同 wing 內房間連接）
└── Tunnel（跨 wing 連接）
```

### 1.2 現有 SumoNoteBook 結構

```
Sumo_wiki/
├── concepts/        # 概念頁
├── summaries/       # 摘要頁
├── agents/          # Agent 技術
├── prompts/         # Prompt 設計
├── workflows/       # 工作流程
├── research/        # 研究報告
├── backlinks/       # 反向連結
├── index.md         # Wiki 目錄
└── log.md          # 活動日誌
```

### 1.3 關鍵差異

| 面向 | MemPalace | SumoNoteBook |
|------|-----------|--------------|
| 組織邏輯 | 人物/專案驅動 | 功能分類驅動 |
| 知識層次 | Closet + Drawer 分離 | 僅有 summaries |
| 連接方式 | Hall + Tunnel | backlinks |

---

## 2. Closet + Drawer 實作方式

### 2.1 現況分析

目前的 `summaries/` 相當於 Closet（壓縮摘要），但缺乏明確的 Drawer（原始檔案）概念。

### 2.2 實作建議

在每個概念筆記中明確標註來源：

```markdown
# 概念：系統架構

## 定義
系統架構是軟體系統的整體結構設計...

## Closet（壓縮摘要）
- 來源：[[../summaries/a1b2fbec]]
- 摘要：系統架構的核心原則與實踐

## Drawer（原始檔案）
- 原始檔案：
  - [[../../raw/architectural_patterns.md]]
  - [[../../raw/microservices_guide.pdf]]

## 相關概念
- [[微服務]] - 系統架構的一種形式
- [[負載平衡]] - 系統架構的組成部分

## 建立時間：2026-04-07
```

### 2.3 自動萃取腳本

建議在 INGEST 流程中加入 Drawer 自動萃取：

```python
# 伪代码
def extract_closet_drawer(source_file, summary):
    closet = generate_summary(source_file, max_tokens=500)
    drawer = {
        "original_path": source_file,
        "file_type": detect_file_type(source_file),
        "word_count": count_words(source_file)
    }
    return closet, drawer
```

---

## 3. 目錄優化建議（記憶宮殿化）

### 3.1 新目錄結構

```
SumoNoteBook/
├── wings/                          # 記憶宮殿最高層級
│   ├── sumo_family/               # 蘇茉家族 Wing
│   │   ├── architecture/          # Room: 架構
│   │   │   ├── closet/            # 壓縮摘要
│   │   │   └── drawer/            # 原始檔案
│   │   ├── agents/                # Room: Agent 技術
│   │   ├── prompts/               # Room: Prompt 設計
│   │   └── workflows/             # Room: 工作流程
│   ├── openclow/                  # OpenClaw Wing
│   │   ├── gateway/
│   │   ├── node/
│   │   └── skills/
│   └── projects/                  # 專案 Wing
│       ├── sumo_voice/
│       └── notebook_rag/
├── shared/                        # 跨 Wing 共享
│   ├── concepts/                 # 全域概念
│   ├── summaries/                # 全域摘要
│   └── backlinks/                # 反向連結
├── raw/                          # 原始資料（Layer 1）
├── Sumo_wiki/                    # 結構化知識（Layer 2）
└── SCHEMA.md                     # 結構定義（Layer 3）
```

### 3.2 Wing 定義規則

| Wing | 定義 | 範例 |
|------|------|------|
| 人物 | 以人為中心的知識集合 | sumo_family, butler |
| 專案 | 以專案為單位的知識集合 | sumo_voice, notebook_rag |
| 技術領域 | 特定技術領域的知識集合 | openclaw, ai_agents |

### 3.3 Room 定義規則

每個 Wing 下的 Room 代表主題細分：
- 數量建議：3-7 個 Room
- 命名：使用中文或英文底線連接
- 最小化：至少 1 個 Room

### 3.4 Hall（翼內連接）

同 Wing 內 Room 之間的連接：

```markdown
## Hall 連接
- [[../architecture/closet/系統設計]] → [[../agents/closet/多代理]]
- [[../prompts/closet/ Chain of Thought]] → [[../workflows/closet/自動化流程]]
```

### 3.5 Tunnel（跨翼連接）

不同 Wing 之間的連接：

```markdown
## Tunnel 連接
- [[../../openclaw/gateway/closet/API設計]] → [[../architecture/closet/RESTful]]
- [[../../projects/sumo_voice/closet/語音處理]] → [[../agents/closet/語音識別]]
```

---

## 4. 檢索優化：目標 34% 提升

### 4.1 分層檢索策略

```
┌─────────────────────────────────────────────┐
│  Query → Closet（壓縮摘要）                  │
│  └─→ 如果需要完整內容 → Drawer（原始檔案）   │
└─────────────────────────────────────────────┘
```

**原理**：
- Closet 體積小，檢索速度快
- 先在 Closet 找到候選結果，再依需求擴展到 Drawer

### 4.2 實作機制

#### 4.2.1 雙索引策略

```python
# 伪代码
class DualIndex:
    def __init__(self):
        self.closet_index = VectorIndex()  # 壓縮摘要索引
        self.drawer_index = FileIndex()     # 原始檔案索引
    
    def search(self, query, need_full=False):
        # Step 1: 先搜尋 Closet
        closet_results = self.closet_index.search(query)
        
        # Step 2: 如需完整內容，從 Drawer 擴展
        if need_full:
            drawer_results = self.drawer_index.search(query)
            return closet_results + drawer_results
        
        return closet_results
```

#### 4.2.2 Wing/Room 語義編碼

為每個 Wing 和 Room 建立 bi-encoder 編碼：

```python
# 伪代码
def encode_hierarchy(wing, room):
    prompt = f"Wing: {wing}, Room: {room}"
    return bi_encoder.encode(prompt)
```

### 4.3 預期效果

| 優化策略 | 預期提升 |
|----------|----------|
| Closet/Drawer 分離 | +15% |
| Wing/Room 語義結構 | +12% |
| 雙索引檢索 | +7% |
| **總計** | **+34%** |

---

## 5. 遷移路徑

### Phase 1: 概念驗證（1-2 週）
- [ ] 建立示範 Wing（sumo_family）
- [ ] 建立 2-3 個示範 Room
- [ ] 實作 Closet/Drawer 標註格式
- [ ] 測試檢索效果

### Phase 2: 結構調整（2-3 週）
- [ ] 建立 wings/ 目錄
- [ ] 搬遷現有概念到對應 Wing/Room
- [ ] 建立 Hall/Tunnel 連接
- [ ] 更新 SCHEMA.md

### Phase 3: 檢索優化（2-4 週）
- [ ] 實作雙索引檢索
- [ ] 建立 Wing/Room bi-encoder
- [ ] 效能測試與調優
- [ ] 上線監控

---

## 6. 總結

### 6.1 核心建議

1. **Closet + Drawer 分離**：在概念筆記中明確標註來源，区分壓縮摘要與原始檔案
2. **Wing/Room 層級**：將現有功能分類改為人物/專案驅動的記憶宮殿結構
3. **Hall + Tunnel 連接**：建立翼內與跨翼的知識連接網路
4. **雙索引檢索**：先搜尋 Closet，需要時擴展到 Drawer

### 6.2 預期效益

- 檢索速度提升
- 知識組織更直觀
- 學習曲線降低
- 跨領域連接更強

---

*本方案由高工蘇茉制定，2026-04-07*
*版本：1.0*
