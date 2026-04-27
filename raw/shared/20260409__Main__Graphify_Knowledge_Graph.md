# Graphify - AI 程式碼知識圖譜技能

## 基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | safishamsi |
| **GitHub** | https://github.com/safishamsi/graphify |
| **PyPI** | graphifyy（graphify 名字被佔用）|
| **功能** | 將程式碼、文件、PDF、圖片轉換為可查詢的知識圖譜 |
| **支援平台** | Claude Code, Codex, OpenCode, OpenClaw, Factory Droid, Trae |

---

## 這是什麼？

一個 AI 程式碼助手技能。在 Claude Code、Codex、OpenCode、OpenClaw、Factory Droid 或 Trae 中輸入 `/graphify`，它會讀取你的檔案、建立知識圖譜還給你一個你不知道存在的結構。

---

## 核心功能

### 🧠 知識圖譜建構

| 輸出檔案 | 說明 |
|----------|------|
| `graph.html` | 互動式圖譜 - 點擊節點、搜尋、按社群篩選 |
| `GRAPH_REPORT.md` | 神級節點、意外連接、建議問題 |
| `graph.json` | 持久化圖譜 - 數週後還能查詢 |
| `cache/` | SHA256 快取 - 只重新處理變更的檔案 |

### 🖼️ 多模態支援

| 類型 | 說明 |
|------|------|
| 程式碼 | Python, JS, TS, Go, Rust, Java, C, C++ 等 20+ 語言 |
| 文件 | PDF、Markdown |
| 圖片 | 截圖、圖表、白板照片 |
| 其他語言 | 支援透過 Claude Vision 擷取概念 |

### 🔧 兩階段處理

| 階段 | 說明 |
|------|------|
| **第一階段** | 確定性 AST 解析（不需要 LLM）|
| **第二階段** | LLM 子代理並行處理文件、論文、圖片 |

### 📊 圖譜分析

| 功能 | 說明 |
|------|------|
| **Leiden 社群偵測** | 根據邊密度發現社群 |
| **標記類型** | EXTRACTED / INFERRED / AMBIGUOUS |
| **語意相似邊** | 直接影響社群偵測 |

---

## 安裝方式

```bash
pip install graphifyy && graphify install
```

### 平台特定安裝

| 平台 | 命令 |
|------|------|
| Claude Code (Linux/Mac) | `graphify install` |
| Claude Code (Windows) | `graphify install` 或 `graphify install --platform windows` |
| OpenClaw | `graphify install --platform claw` |

---

## 使用方式

```bash
# 基本使用
/graphify .

# 查詢圖譜
graphify query "show the auth flow" --graph graphify-out/graph.json
graphify query "what connects DigestAuth to Response?" --graph graphify-out/graph.json
```

---

## 與 SumoNoteBook 的關係

| Graphify 功能 | SumoNoteBook 對應 |
|---------------|-------------------|
| 知識圖譜建構 | 現有架構有相似概念 |
| GRAPH_REPORT.md | 類似摘要報告 |
| 互動式 graph.html | 可參考視覺化方式 |
| 社群偵測 | 目前沒有類似功能 |
| 兩階段處理 | 可參考離線 + LLM 混合架構 |

---

## 啟發

1. **Andrej Karpathy 的 /raw 資料夾概念** - graphify 是這個問題的答案
2. **20x 節省 tokens** - 71.5x fewer tokens per query vs reading raw files
3. **Always-on hook** vs **Explicit trigger** - 兩種不同的觸發模式
4. **AMIBUOUS 標記** - 對於不確定的資訊誠實標記

---

## 標籤

#知識儲備 #Graphify #知識圖譜 #AI程式碼助手 #ClaudeCode #NetworkX #Leiden #程式碼分析

---

*記錄者：總管蘇茉*
*時間：2026-04-09 20:37*
