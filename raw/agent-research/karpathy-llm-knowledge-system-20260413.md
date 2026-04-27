# Karpathy 的 LLM 知識系統研究

> 來源：Facebook - 蔡炎龍（OpenClaw 中文社群）
> 日期：2026-04-13
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 原始分享

蔡炎龍分享 Karpathy 用 LLM 做了知識系統，至少有兩個有趣的地方：

1. **個人 Wikipedia**：打造個人知識庫，包括朋友、工作、熱情、做的事情
2. **反思 RAG**：很多時候以為要做 RAG，但 Karpathy 的方式可能更好

---

## 💬 討論精華

### Mark Chang 的觀點

> RAG 比較像傳統 SQL database，有一定的 schema（fixed chunk size）
> LLM wiki 比較像 NoSQL database 或 knowledge graph
> 在不同的使用情境，這兩者各有所長

### 蔡炎龍的回應

> 實務上很多人不太懂的情況下，其實他應該要做 SQL 形式的資料庫，但他做 RAG
> RAG 和 Karpathy wiki 精神上做的事是比較接近的

### Hwai-Jung Wesley Hsu 的觀點

> Wiki 用的是 hierarchical 架構，現在夠用是因為 context window 足以涵蓋夠大的文本範圍
> LLM 理解 wiki 中的文字也是用 embedding，這其實是隱性的 RAG

---

## 📊 RAG vs Karpathy Wiki 比較

| 比較 | RAG | Karpathy Wiki |
|------|-----|---------------|
| **資料結構** | Fixed chunk size（SQL-like）| Hierarchical（NoSQL-like）|
| **搜尋方式** | Embedding similarity | Context window |
| **適用場景** | 明確的 Q&A | 個人知識沉澱 |
| **索引方式** | Embedding similarity search | Hierarchical structure |
| **靈活性** | 固定 schema | 動態擴展 |

---

## 💡 蘇茉家族的啟發

### 對 SumoNoteBook 的影響

1. **雙模式支援**：可以同時支援 RAG-style 和 Wiki-style 檢索
2. **Context Window 優先**：當 context window 夠大時，用 hierarchical 架構更自然
3. **隱性 RAG**：理解 wiki 的底層也是 RAG，只是包裝不同

### 實際應用

| 功能 | 做法 |
|------|------|
| **日常查詢** | 用 RAG（快速、精確）|
| **個人知識沉澱** | 用 Wiki-style（彈性、自然）|
| **混合使用** | 根據場景選擇 |

---

## 🔗 相關討論

- Karpathy 的 LLM 知識系統強調「個人 wiki」的概念
- 不同於傳統 RAG 的固定 chunk size，wiki 用 hierarchical 架構
- 這代表了 AI 知識管理的另一條路

---

*最後更新：2026-04-13*