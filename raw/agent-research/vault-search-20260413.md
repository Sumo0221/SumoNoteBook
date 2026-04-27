# Vault Search - Obsidian 語義搜尋插件

> 來源：GitHub - notoriouslab/vault-search
> 日期：2026-04-13
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 專案概述

**名稱**：Vault Search
**功能**：Obsidian 的本地語義搜尋，使用 Ollama embeddings
**特色**：Local-first、 無 API key、無雲端、繁中友善

---

## 🎯 核心理念

> "AI helps you see. You decide what it means."

| 比較對象 | 他們的做法 | Vault Search 的做法 |
|----------|------------|---------------------|
| **Karpathy 的 LLM Wiki** | AI 完全取代你的編輯 | AI 幫你發現，不是替你思考 |
| **其他 AI 工具** | 建立 AI wiki 或自動摘要 | 幫你找回忘記的筆記 |

---

## 🔥 Hot/Cold Intelligence（與我們的 MemPalace V2 概念相同！）

| 等級 | 定義 | 說明 |
|------|------|------|
| **Hot** | 有連結或近期活動的筆記 | 活躍、已連接 |
| **Cold** | 孤兒筆記（orphan） | 被遺忘的寶藏 |

### Discover 功能
- 找出與當前筆記相關的 Cold notes
- 就是你的 **blind spots（盲點）**

---

## 🗺️ MOC Generation（Map of Content）

一鍵將搜尋或 Discover 結果匯出為 MOC note，包含：
- Wikilinks
- 預覽內容

---

## 🔒 真正本地、真正隱私

| 特性 | 說明 |
|------|------|
| **所有處理都在本機** | Embedding、索引、搜尋、Discover |
| **零數據傳出** | 不是設定，是架構 |
| **不需要 API Key** | 不需要雲端服務 |
| **8GB 筆電就能跑** | 低記憶體、低 CPU 需求 |

---

## 🇨🇳 繁中優化

| 項目 | 內容 |
|------|------|
| **Embedding 模型** | `qwen3-embedding:0.6b` |
| **優勢** | 繁體中文 + 英文語義理解 |
| **同義詞擴展** | 同一概念的不同說法也能匹配 |

---

## 📊 架構圖

```
Your Notes (.md) → Ollama Embed API → Vector Index (index.json)
     ↓
Your Query → Ollama Embed API → cosine similarity → ranked results
     ↓
Discover (no Ollama call) - 純向量比較
```

---

## ✨ 功能列表

| 功能 | 說明 |
|------|------|
| Semantic Search | 語義搜尋，不只是關鍵字 |
| Sidebar Panel | 持久化結果，含 Search + Discover 分頁 |
| Quick Modal | Cmd/Ctrl+P 快速跳轉 |
| Find Similar | 找相似筆記（零 API 呼叫）|
| Smart Indexing | 增量更新，檔案變動自動索引 |
| Hot/Cold Tiers | 視覺標記區分熱/冷筆記 |
| Active Discovery | 開啟筆記，側邊欄自動顯示相關筆記 |
| Global Discover | 找出與所有 Hot 筆記相關的 Cold 筆記 |
| MOC Generation | 匯出為 Map of Content note |
| Canvas Integration | 可拖曳結果到 Canvas 視覺化 |
| LLM Descriptions | 本地 LLM 生成 frontmatter 描述 |
| Bilingual UI | 英文 + 繁體中文 |

---

## 🔧 安裝需求

| 需求 | 說明 |
|------|------|
| Ollama | 已啟動 |
| Embedding 模型 | `ollama pull qwen3-embedding:0.6b` |
| LLM 模型（可選）| `ollama pull qwen3:1.7b` 用於描述生成 |
| Obsidian Desktop | 桌面版 |
| BRAT 插件 | 用於安裝社群插件 |

---

## 💡 與蘇茉家族的相關性

### 與 MemPalace V2 的相似之處
- **Hot/Cold Intelligence** - 我們也有！
- **Discover 概念** - 找出被遺忘的筆記
- **本地優先** - 不依賴雲端

### 可以借鑒的功能
1. **MOC Generation** - 自動生成 Map of Content
2. **LLM Descriptions** - 用 LLM 生成描述改善搜尋品質
3. **增量索引** - 高效的索引更新機制

---

## 📦 推薦模型

| 模型 | 大小 | 用途 |
|------|------|------|
| qwen3-embedding:0.6b | 639MB | Embedding，最好支援繁中 |

---

## 🔗 連結

- GitHub：https://github.com/notoriouslab/vault-search
- BRAT 插件：https://github.com/TfTHacker/obsidian42-brat

---

*最後更新：2026-04-13*