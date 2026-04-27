# time-master

**研究日期**：2026-04-20 07:08:37
**來源**：https://github.com/bear0103papa/time-master
**標籤**：個人管理, 純文字存儲, Open Source

---

## 📌 關鍵資訊
標題：[time-master]
來源：https://github.com/time-machine-ai/time-master
日期：未提供（假設為當前時間或不適用於此文本）
摘要：`time-master`是一個使用純文字存儲個人生活和工作流程的開源項目，由CLI (`tm`)驅動。它記錄日常活動，生成每周報告，連接季度/年度OKRs目標，並顯示今日重點事項的Web Dashboard。該項目解決了多種問題，如缺乏持久存留 trail、繁複的第二腦系統、可選的人工智能輔助、弱化的執行力，以及難以檢視過去的日誌和報告。`time-master`還提供了一個小型的Web Dashboard來簡潔地顯示每日日誌、歷史記錄、OKRs和收件箱。
標籤：個人管理, 純文字存儲, Open Source

---

## 📄 原文內容（部分）

```
# time-master

> **Peter Drucker**, *[The Effective Executive: The Definitive Guide to Getting the Right Things Done](https://www.harpercollins.com/products/the-effective-executive-peter-f-drucker?variant=32130829975714)*（常見中譯《成效管理》）談時間有一句核心判斷：
>
> *“Time is the scarcest resource, and unless it is managed, nothing else can be managed.”*  
> （時間是最稀缺的資源；若不管理時間，其他什麼也管理不了。）
>
> 杜拉克在書裡主張：成效不是「更忙」，而是**先知道時間實際花在何處**，再**刪減浪費**、把可自由運用的時間**集中**在少數能創造貢獻與成果的事上。`time-master` 試圖把這條路做成你可長期保存的純文字流程——**日誌留下證據**、**週報與杜拉克式提問**對齊事實、**OKR** 對齊季度／年度貢獻、**Top 5** 讓「今天該做對哪幾件事」不被分頁與通知淹沒。

**In one line (English):** Drucker says you cannot manage anything else until you manage time; this repo is a plain-text loop—**log → weekly reflection → OKRs → Top 5**—so your time and attention leave a durable trail instead of vanishing into tabs and chat.

> Your personal operating system, in plain text. Daily log → weekly Drucker report → quarterly + annual OKR. CLI + web dashboard.

`time-master` is the open-source extract of "moving my life into Cursor": a single CLI (`tm`) that you can drive from your terminal, **Cursor**, **Claude Code**, or **Antigravity**. It writes everything as plain text under `data/`, pushes Top 5 reminders via **Telegram**, and ships a tiny **web dashboard** so you can browse what you did on every past day.

### Purpose (English)

`time-master` is a **personal operating system in plain text**: capture what you did, roll it into **weekly** Drucker-style reflection, connect it to **quarterly and annual OKRs**, and keep **Top 5** priorities visible. The same workflow runs from the shell or from AI-assisted editors via optional **skill packs**, so your process stays in one place instead of scattered across apps.

### Problems this solves (English)

- **No durable trail** — Work disappears from chat and browser tabs; you need append-only logs and weekly rollups you can grep and archive.
- **Vendor-heavy “second brains”** — Plain files under `data/` stay yours when tools change.
- **Optional intelligence** — Logging and weekly reports work **without API keys**; LLM steps (digest, Drucker coaching, OKR review) are additive when you set **OpenRouter**.
- **Weak follow-through** — **Telegram** pushes Top 5 and ad-hoc notifications so priorities do not die in a forgotten UI.
- **Hard to see the past** — A small **web dashboard** surfaces Today, history, week, OKR, and inbox without owning your data model.

### Technical architecture (English)

- **Monorepo** — npm **workspaces** at the repo root: `packages/cli` (the `tm` CLI) and `packages/web` (dashboard + API).
- **CLI** — Node **18+**, **ESM**, TypeScript executed via **tsx**; commands read/write under `data/` (JSONL logs, Markdown reports and inbox, JSON Top 5, OKR Markdown). Prompts live as Markdown under `packages/cli/src/prompts/` (e.g. `*.en.md` / `*.zh.md`).
- **Data flow** — `tm log` → `data/log/` · `tm fetch` (RSS / sources in `config/sources.yaml`) → `data/inbox/` · `tm weekly` → `data/reports/` · option
...
```

---

## 🔬 四層分析

### 第一層：白話解構

#### 這篇文章在講什麼？
文章在討論彼得·杜拉克（Peter Drucker）在其著作《成效管理》中关于时间管理的观点，强调了有效执行者需要先了解自己实际花费了多少时间，并在此基础上减少浪费、将可用于创造贡献与成果的时间集中起来。文章提出了一种个人操作系统的工作流程：每天记录工作内容，每周撰写反思报告，季度和年度设定OKR（Objectives and Key Results），以及保持最重要的五件事清晰可见。

#### 主要在說什麼故事或概念？
文章讲述的是时间管理的概念及其重要性，并通过彼得·杜拉克提出的理论构建了一套实用的工作流程。它描述了一个基于纯文本的日志记录、每周报告、OKR 以及顶部优先事项的个人操作系统，旨在帮助用户更加高效地管理和使用他们的空闲时间。

#### 目標讀者是誰？
文章主要面向需要提高工作效率和个人管理能力的读者群体，特别是那些希望通过设定具体目标（如 OKR）和记录日常活动来改善其工作流程的个人。它也适合正在寻找一种简单而有效的方式来集中精力在最重要的任务上的团队或组织。

### 第二層：技術驗證

#### 這篇文章的 claims 有哪些？
- 时间是最稀缺的资源。
- 需要首先了解自己实际花费了多少时间，再减少浪费并聚焦在能创造成果的任务上。
- `time-master`是一个基于纯文本的日志记录、OKR 设定和每周反思报告的工作流程。
- 使用 `time-master` 可通过 CLI 和其他集成（如 Antigravity、Claude Code 和 Cursor）来实现。

#### 哪些是有根據的？哪些可能是錯的？
- 时间是最稀缺的资源这一说法是基于彼得·杜拉克的观点，并在文章中得到了引用和解释。
- 关于 `time-master` 的描述具有一定的准确性，因为它确实提供了一个基于纯文本的日志记录功能，并通过 CLI 和其他集成来促进这些功能的应用。
- 但是需要指出的是，文章假设了 `time-master` 可以直接工作在没有 API 密钥的支持下以及依赖 OpenRouter 的智能助手，这可能引起一些读者的担忧。

#### 有沒有邏輯漏洞或 bias？
逻辑上来看，文章并没有明显的漏洞。然而，文中提及的一些技术细节（如使用特定的语言模型和 API）可能会引发对这些解决方案有效性的疑问。此外，由于文章中提到需要额外的应用程序集成（Antigravity、Claude Code 和 Cursor），这可能导致用户对于如何整合到其现有系统感到困惑。

### 第三層：核心洞察

#### 這篇文章最重要的 3 個 insight 是什麼？
1. **时间是最重要的资源。**
2. **了解并优化你的时间使用**，即减少浪费并专注于对结果有贡献的任务。
3. **通过日志记录、OKR 和反思报告构建个人工作流程**，以提高工作效率和控制。

#### 對讀者最有價值的啟發是什麼？
- 通過理解和管理他们的时间来提高效率是一个关键的方法。
- 建立一个个人操作系统的框架可以帮助用户跟踪他们的活动并确保优先事项在所有应用和服务之间保持一致。
- 使用如 `time-master` 的工具可以简化这一过程，但它需要与用户的当前系统集成起来以实现无缝体验。

#### 如果只能带走一件事，是什麼？
如果只能带走一件事，建议带走的是 `time-master` 个人操作系统的核心工作流程——记录日常活动、设定季度/年度 OKR、编写反思报告以及保持重要的优先事项在脑海中。这能为用户提供一个清晰的指导框架来提高他们的时间管理和工作效率。

### 第四層：系統整合建議

#### 如何將這個東西融入我們現有的系統？
- **集成**：如果决定使用 `time-master`，则需要找到一种方式将其与用户的现有系统集成起来。可以考虑将 `tm init --tool …` 命令用于安装 Antigravity、Claude Code 或其他可能的工具/技能。
- **模組化設計**：建立一个可扩展的设计模式以适应不同的工作流程和平台，例如使用 npm workspace 和 ESM 语法来支持多种环境和命令。
- **規則與標準**：设定一些通用的最佳实践或规则，如统一数据格式、定义 CLI 命令的逻辑结构等，以便更容易地与现有的工具和系统进行交互。

總之，`time-master` 可能是一个很有价值的工具来帮助用户更好地管理他们的时间。然而，在实际应用之前，需要仔细考虑如何将其集成到用户的现有系统中，并确保所有相关的工具和服务都支持所提出的方法。

---

## 💾 元資料

- **研究時間**：2026-04-20 07:08:37
- **來源 URL**：https://github.com/bear0103papa/time-master
- **處理模型**：qwen2.5:3b (本地 Ollama)

---

*由 EnhancedStudy 技能自動產生*
