# MindForge — 會自己讀書的 AI 知識引擎

> 來源：Facebook - Ethan Tsui
> 日期：2026-04-15（19小時前）
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 概述

作者 Ethan Tsui 做了一個**會自己讀書的 AI 知識引擎**，核心是解決「每次看到新技術都要花大量時間閱讀、整理、判斷哪些是事實哪些是幻覺」的問題。

---

## 🎯 最重要的設計原則

> **Principle 0：「知道自己不知道」優先於「零幻覺」。**

答不出來就說答不出來，不編。每句話都掛 source citation，點得到原文。

---

## 🔑 核心：Knowledge Acquisition Loop（KAL）

### 傳統 RAG vs MindForge

| 系統 | 行為 |
|------|------|
| **傳統 RAG** | 你餵文件、它回答 |
| **MindForge** | 它自己判斷學夠了沒有 |

### KAL 流程

```
你丟 URL 或關鍵字 → 系統啟動 KAL：
  觸發 → 搜尋相關文件 → 擷取蒸餾
  → 自我反問：「我能解釋這個東西了嗎？」
  → 能 → 通知你「學完了，可以問我了」
  → 不能 → 針對答不出的問題再搜尋 → 再蒸餾 → 再反問
  → 重複直到通過或達到上限
```

---

## 🔧 技術架構

### 儲存層
- **PostgreSQL 16 + pgvector + pg_trgm**
- HNSW index（1024d, m=16, ef_construction=200）

### 向量化 + 重排序
- **BGE-M3**（1024 維，支援中英多語言）
- **BGE-Reranker-v2-m3** 做重排序
- 全部地端，零 API 成本

### 檢索管線（5-step）
1. Pack Routing
2. Hybrid Retrieval（pgvector dense + pg_trgm sparse）
3. BGE Reranker 重排序
4. Graph Expansion（Recursive CTE 2-hop）
5. Citation Assembly

### 知識組織（三層）
| 層次 | 說明 |
|------|------|
| Raw | 原文 |
| Wiki | LLM 維護 |
| Schema | 人類控制 |

---

## 🤖 模型選擇

| 系統 | 模型 | 特性 |
|------|------|------|
| **產業 KG** | Qwen 3.5 122B | Recall-first |
| **MindForge** | Gemma 4 26B | **Precision-first** |

> **為什麼選 Gemma？**
> - Precision 93.5% vs Qwen F1 79.9%
> - 「說錯比少說嚴重」是個人知識場景的核心

---

## 📊 實測案例

### Hermes Agent 例子

**Round 1**：
- 擷取 GitHub README
- 蒸餾 38 條原子主張
- 自我反問 3 題 → **0/3 通過**

**Round 2**：
- Brave Search 搜尋 5 篇相關文件
- 再次蒸餾
- 再次自問 → **3/3 通過**

---

## 🔗 靈感來源

| 來源 | 借鑑內容 |
|------|----------|
| Karpathy LLM Wiki | 三層儲存（Raw / Wiki / Schema）|
| Karpathy autoresearch | Agent loop 紀律 |
| MemPalace | 記憶宮殿組織法 |

---

## 💡 蘇茉觀察

### 與蘇茉家族的關聯

| MindForge | 蘇茉家族 |
|-----------|----------|
| KAL（自己學習判斷夠了）| SumoMemory 自動整理 |
| 三層知識組織 | MemPalace V2 |
| Precision-first（Gemma）| 我們選 MiniMax |
| 零幻覺 + citation | 批判性反思技能 |

### 可以借鏡

1. **KAL 概念**：讓 SumoMemory 也能「自己判斷學夠了」
2. **Principle 0**：承認不知道 > 幻覺
3. **Precision-first**：個人知識要精準，不要貪多

---

## 📊 互動數據

| 項目 | 數量 |
|------|------|
| 心情 | 227 |
| 留言 | 59 |
| 分享 | 84 |

---

*最後更新：2026-04-15*