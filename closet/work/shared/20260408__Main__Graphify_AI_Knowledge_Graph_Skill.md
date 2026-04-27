# Graphify - AI 知識圖譜 Skill

## 基本資訊

| 項目 | 內容 |
|------|------|
| **名稱** | Graphify |
| **PyPI 名稱** | graphifyy（臨時名稱）|
| **GitHub** | https://github.com/safishamsi/graphify |
| **用途** | 將任何資料夾（程式碼、文件、PDF、圖片）變成可查詢的知識圖譜 |

---

## 支援平台

- ✅ Claude Code
- ✅ Codex
- ✅ OpenCode
- ✅ **OpenClaw**
- ✅ Factory Droid

---

## 主要功能

### 1. 輸入類型
- 程式碼（自動 AST 解析）
- PDF 文件
- Markdown 文件
- 截圖、圖表
- 白板照片
- 甚至其他語言的圖片（使用 Claude Vision）

### 2. 兩階段處理
- **第一階段（無需 LLM）**：AST 解析程式碼結構（類別、函數、導入、調用圖）
- **第二階段（並行 LLM）**：處理文件、論文、圖片，提取概念和關係

### 3. 輸出結果
```
graphify-out/
├── graph.html      ← 互動式知識圖譜（可點擊、搜尋、篩選）
├── GRAPH_REPORT.md ← 節點報告、意外連接，建議問題
├── graph.json      ← 持久化圖譜（之後可查詢）
└── cache/          ← SHA256 緩存（增量更新）
```

### 4. 圖譜聚類
- 使用 Leiden 社區檢測演算法
- 基於圖拓撲結構（不需要 Embeddings）

### 5. 關係標註
- `EXTRACTED`：直接從源碼找到
- `INFERRED`：合理推斷（有信心度分數）
- `AMBIGUOUS`：標記待審查

---

## 安裝方式

```bash
pip install graphifyy && graphify install
```

OpenClaw 安裝：
```bash
graphify install --platform claw
```

---

## 和 MemPalace 的比較

| 功能 | Graphify | MemPalace |
|------|----------|-----------|
| **用途** | 程式碼/文件理解 | 對話記憶 |
| **輸入** | Code, PDF, Markdown, 圖片 | 對話、文件 |
| **輸出** | 互動式 HTML 圖譜 | 向量搜尋 |
| **查詢方式** | 圖譜遍歷 | 向量相似度 |
| **知識來源** | Karpathy 的 /raw 模式 | 蘇茉家族的對話 |

---

## 與 SumoNoteBook 的關係

Graphify 做的事情和 SumoNoteBook + MemPalace 有些重疊：

| 現有方案 | Graphify 的優點 |
|----------|-----------------|
| SumoNoteBook（Wiki 結構） | 自動從程式碼提取結構 |
| MemPalace（向量記憶） | 互動式可視化圖譜 |

**潛在應用**：
- 把 SumoNoteBook 的文件用 Graphify 處理，自動建立知識圖譜
- 讓 Graphify 分析蘇茉家族的程式碼，了解架構決策

---

## 決策

| 日期 | 決定 |
|------|------|
| 2026-04-08 | 暫時不安裝，持續觀望 |

---

## 標籤

#知識儲備 #Graphify #知識圖譜 #AI工具 #OpenClaw

---

*記錄者：總管蘇茉*
*時間：2026-04-08 01:20*
