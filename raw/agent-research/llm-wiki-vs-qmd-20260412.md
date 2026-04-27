# 個人知識庫方案比較：GBrain vs QMD vs LLM Wiki vs Roger's Letter

> 來源：Facebook - Roger's Letter
> 日期：2026-04-12
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 概述

三位大師（Andrej Karpathy、Tobi Lütke、Garry Tan）的知識庫系統比較，整理自 Roger's Letter 粉專。

---

## 📊 四大系統對照

| 系統 | 作者 | 核心概念 | 一句話 |
|------|------|----------|--------|
| **LLM Wiki** | Andrej Karpathy | 知識要在多次對話中被寫進結構 | 知識庫要像 wiki 一樣會長大 |
| **QMD** | Tobi Lütke | 本地混合搜尋引擎（BM25+向量+查詢擴展）| 把「找得到」做到極致，不離開你的機器 |
| **GBrain** | Garry Tan | Read-Write-Compound 迴圈 | 個人知識庫像公司一樣需要資料庫與管線 |
| **Roger's Letter** | 作者本人 | 投資研究 AI Agent + 儀表板 | 投資與產業領域資產持續累積 |

---

## 🎓 三位大師的核心洞見

### Andrej Karpathy（LLM Wiki）

**他是誰**
- Stanford 博士，OpenAI 初期研究員
- Tesla AI 總監，2024 年創辦 Eureka Labs
- 代表概念：Software 2.0、vibe coding

**他教什麼**
- 用不可變的原始資料當地基
- 用 LLM 維護持久性 wiki（摘要、實體、概念、交叉引用）
- 用 schema（CLAUDE.md / AGENTS.md）約束攝入、查詢、健檢

**核心洞見**
> 「好檢索不如好編纂」
> 知識要在多次對話與多份來源中被寫進結構，而不是每次都從零拼湊

**最適合誰**
- 個人研究者、長期主題深讀
- 願意與 LLM 共寫規則、共演目錄的人

**一句話**
> Karpathy 給的是羅盤：你的知識庫應該像 wiki 一樣會長大，而不是像上傳檔案一樣被反覆檢索。

---

### Tobi Lütke（QMD）

**他是誰**
- Shopify 共同創辦人與長期 CEO
- QMD = Query Markup Documents

**他教什麼**
- 本地混合搜尋引擎：BM25 + 向量語意 + 查詢擴展 + 重排序
- 隱私、零雲端 API、可腳本化與 MCP 整合

**核心洞見**
> 不替你寫 wiki，但能在你的 Markdown / 程式碼 / 會議記錄上做到接近「檢索管線」的一流品質

**最適合誰**
- 工程師與重度筆記使用者
- 需要離線或敏感資料上搜尋整個 corpus
- 已經有大量檔案、但還沒決定要不要上雲端向量庫

**一句話**
> Tobi 給的是望遠鏡：在資料已存在的前提下，把「找得到」做到極致，而且不離開你的機器。

---

### Garry Tan（GBrain）

**他是誰**
- Y Combinator 總裁
- 真實在跑的日常系統：萬級 Markdown、千級人物檔、多年日曆與會議轉錄

**他教什麼**
- 頁面模型：compiled truth（當前最佳論述）+ timeline（只增不刪的證據鏈）
- 檢索：關鍵字 + 向量 + RRF 的工程級組合
- Agent 透過 skills 知道何時讀、何時寫

**核心洞見**
> 知識會隨訊號進場而更新，並與 OpenClaw / Hermes 類的 agent memory 分工

**最適合誰**
- 人脈、公司、交易、會議高密度的知識工作者
- 資料量已讓 grep 失效、需要增量同步與圖譜式關聯

**一句話**
> Garry 給的是營運系統：當個人知識庫像一家公司一樣有資產負債表，你需要的是資料庫與管線，而不只是資料夾。

---

## 🔄 三位大師的知識流對比

### GBrain 的知識迴圈（Read-Write-Compound）
```
信號到達 → Agent 偵測實體 → 讀取大腦 → 帶上下文回應
     ↓
寫回大腦 → 索引同步 → 每次循環都增加知識
```

### QMD 的知識流（Read-Only Index）
```
文件變更 → qmd update（掃描）→ 分塊 + 嵌入 → 搜尋查詢 → 返回結果
（不改變原始文件，不產生新知識）
```

### Wiki 的知識迴圈（Ingest-Query-Lint）
```
新來源 + LLM 攝取 + 討論 + 寫摘要頁 + 更新索引 + 更新相關頁
查詢的好答案也回寫 Wiki → 記入日誌
```

### 本專案（投資 AI）
```
研究任務 / 資料更新 → Skills → 執行管線 → 鳥人結構化資料與報告
Web 儀表板呈現 → 投資與產業領域資產持續累積
可選外接 QMD API
```

---

## 🤔 三位大師與蘇茉家族的對照

| 大師問 | 蘇茉家族現狀 | 改善方向 |
|--------|-------------|----------|
| **Karpathy 問：有沒有在長？** | MemPalace 有持續寫入 | 確保每個蘇茉都會主動豐富相關頁面 |
| **Tobi 問：找不找得到？** | 目前靠關鍵詞搜尋 | 未來可考慮 QMD 類的本地極致搜尋 |
| **Garry 問：能不能每天變聰明？** | SumoMemory 的 Brain-Agent Loop | 正是這個概念，需要確保穩定運行 |

---

## 💡 對蘇茉家族的具體啟發

### 對 MemPalace
- **Karpathy 的「好檢索不如好編纂」**：MemPalace 不只是搜尋，更是讓蘇茉持續豐富的「編纂」系統
- **Garry 的「timeline」概念**：重要記憶應該有時間軸，只增不刪

### 對 SumoNoteBook
- **Tobi 的 QMD 概念**：未來可考慮對技術文件做極致本地搜尋
- **Karpathy 的「會長大」**：SumoNoteBook 應該像 wiki 一樣持續生長

### 對 SumoMemory
- **Garry 的「Read-Write-Compound」**：SumoMemory 的 Brain-Agent Loop 正是這個概念
- **核心對照**：蘇茉Memory = Read-Write-Compound、SumoNoteBook = Read-Only Index

---

## 📝 Karpathy 的問題對照

> Karpathy 問：你的知識有沒有在長？
> 我們答：有，長在公司與產業的研究資產裡。

> Tobi 問：你找不找得到？
> 我們答：儀表板與 API 內建結構化查找；若要「全本機、全檔案、極致檢索」，再加 QMD。

> Garry 問：你能不能每天自動變聰明？
> 我們答：skills + 管線 + 同步讓研究流程複利；生活全域與超大規模向量庫則非本系統預設戰場。

---

*最後更新：2026-04-12*
