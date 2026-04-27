# Karpathy LLM Wiki - 個人知識庫模式

> 日期：2026-04-07
> 來源：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
> 標籤：#llm-wiki #knowledge-base #karpathy

---

## 🎯 核心理念

這是一個用 LLM 構建個人知識庫的模式。

**關鍵差異**：LLM 不是在查詢時重新發現知識，而是**增量構建和維護一個持久 wiki**。

---

## 📚 三層架構

| 層次 | 說明 | 蘇茉的對應 |
|------|------|-----------|
| **Raw sources** | 原始文檔（文章、論文、圖片）| `SumoNoteBook/raw/` |
| **Wiki** | LLM 生成的 Markdown 檔案（摘要、實體頁、概念頁）| `SumoNoteBook/wiki/` |
| **Schema** | 告訴 LLM 如何組織 wiki 的配置文件 | `AGENTS.md`, `CLAUDE.md` |

---

## 🔄 三個主要流程

### 1. Ingest（攝入）
- 把新來源丟進 raw collection
- 告訴 LLM 處理它
- LLM 會：寫摘要、更新 index、更新相關頁面、記錄矛盾、附加到 log

### 2. Query（查詢）
- 問問題，LLM 搜尋相關頁面、閱讀後綜合回答
- 好的答案可以存回 wiki 成為新頁面

### 3. Lint（檢查）
- 定期健康檢查
- 檢查：矛盾、過時內容、孤立頁面、缺失連結

---

## 📝 兩個特殊檔案

### index.md（內容導向）
- Wiki 的目錄，每頁一列 + 一行摘要 + 連結
- LLM 每次 ingest 都更新
- 回答問題時 LLM 先讀 index 找到相關頁面

### log.md（時間順序）
- 只附加的 record，記錄發生了什麼 + 何時
- 建議格式：`## [2026-04-02] ingest | Article Title`
- 可以用 unix 工具解析：`grep "^## \[" log.md | tail -5`

---

## 🔧 工具建議

| 工具 | 用途 |
|------|------|
| **qmd** | 本地搜尋引擎（BM25/vector search + LLM re-ranking）|
| **Obsidian Web Clipper** | 瀏覽器擴展，把網頁文章轉 markdown |
| **Obsidian graph view** | 可視化 wiki 的形狀 |

---

## 💡 蘇茉的對應

| Karpathy 模式 | 蘇茉現況 |
|---------------|----------|
| Raw sources | `raw/` ✅ |
| Wiki（摘要、實體頁、概念頁）| `wiki/` ✅ |
| Schema (CLAUDE.md) | `AGENTS.md` ✅ |
| index.md | 還沒有（需要建立）|
| log.md | 還沒有（需要建立）|
| qmd 搜尋 | 還沒有 |

---

## 🎯 可以改進的地方

1. **建立 index.md** - Wiki 的目錄頁
2. **建立 log.md** -  時間順序 record
3. **定期 Lint** - 健康檢查流程（還沒有）
4. **qmd 整合** - 強化搜尋能力

---

## 📝 備註

這就是 SumoNoteBook 要學習的核心概念！