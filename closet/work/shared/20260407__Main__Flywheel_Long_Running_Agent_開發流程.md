# Flywheel - Long-running Agent 開發流程框架

> 日期：2026-04-07
> 來源：Session Handoff 文章 / GitHub: romanticamaj/flywheel
> 標籤：#long-running-agent #development流程 #Claude-Code

---

## 🎯 核心理念

**「交接零成本」** — 不是讓一個 session 撐很久，是讓**無限個 session 可以接力跑下去**。

---

## 📚 背景

Anthropic 在《Effective Harnesses for Long-running Agents》中比喻：
> Agent 跨 session 工作就像工程師輪班，交班紀錄寫得好，新人幾分鐘就能上手；沒留任何東西，就是花第一個小時重建 context

---

## 🔧 Flywheel 流程

```
Spec → 規劃 feature list → 每個 session 實作一個 feature 
    → multi-agent code review → 寫交班日誌 → 下一個 session 接手
```

### 四個環節的選擇

| 環節 | 作者的選擇 | 理由 |
|------|------------|------|
| **規劃** | JSON format | Agent 不易乱改結構 |
| **實作** | 一個 session 只做一個 feature | 做玩必須可 merge，沒有半成品 |
| **Review** | 四層 pipeline（cleanup → peer → cross-model → E2E）| 品質優先 |
| **交接** | JSONL machine-readable 日誌 | 下一個 session 讀完就能直接動工 |

### 四層 Review Pipeline
1. Cleanup（清理）
2. Peer review（同儕審查）
3. Cross-model（跨模型）
4. E2E（端到端測試）

---

## 💡 關鍵洞察

### Context Window vs Filesystem
```
Context Window = RAM（易失）
Filesystem = Disk（持久）

重要的東西寫在磁碟上，不是留在 context window
```

### 三種人的不同選擇
| 人 | 在乎 | 做法 |
|----|------|------|
| 工程師 A | 速度 | 流程越輕越好，規劃完就直接衝 |
| 工程師 B | 品質 | 四層 review 全開，寧可慢也不要漏 |
| 工程師 C | 可追溯性 | 每個 session 要有 compliance table |

---

## 🚀 應用場景

### 軟體開發
- 每個 session 完成一個 feature
- 交接時帶上 codebase 狀態

### 寫技術文件
- 每個 session 完成一個章節
- 交接時記錄大綱進度和風格決定

### 做研究報告
- 每個 session 處理一個主題
- Review 確保引用正確、論述一致

### 經營內容
- 每個 session 產出一篇貼文
- 交接時帶上品牌語氣和已發布的脈絡

---

## 💎 蘇茉的應用價值

### 對 SumoNoteBook 的啟發

1. **交接日誌格式** - 現在蘇茉的交接比較隨意，可以學這套用 JSONL
2. **專注單一任務** - 每個 session 只做一個 feature，避免半成品
3. **Review 層級** - 可以根據任務重要性選擇跑幾層 review

### 對蘇茉家族的啟發

1. **跨 session 接力** - 蘇茉家族現在的交接可以更結構化
2. **交班紀錄** - 讓下一個蘇茉能快速接手
3. **知識沉澱** - 檔案>記憶，重要決定寫到磁碟

---

## 📝 備註

GitHub repo (`romanticamaj/flywheel`) 找不到，可能需要再確認。