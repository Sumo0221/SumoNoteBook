# Boris 的 Claude Code 私藏秘訣 - Facebook 研究筆記

## 基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | 工程師米奇 (geekMickey) |
| **主題** | Boris 的 Claude Code 私藏秘訣 |
| **時間** | 1天前 |
| **讚數** | 52 |
| **留言** | 1 |

---

## 這是什麼？

工程師米奇分享 Boris 的 Claude Code 進階技巧，讓你從「寫 Code 的人」進化成「指揮 AI 的指揮官」。

---

## 💡 三個核心技巧

### 4️⃣ 生命週期鉤子：讓 Agent 變聰明 (Hooks) 🪝

| Hook | 說明 |
|------|------|
| **SessionStart** | 每次啟動時自動載入當前專案的最新 Context |
| **PreToolUse** | 在模型執行任何 Bash 指令前自動記錄 Log |
| **Custom Integration** | 設定讓權限請求自動傳送到 WhatsApp |

**比喻**：如果把 Claude 比喻成員工：
- 到公司先開機 → SessionStart
- 做危險動作前先報告 → PreToolUse
- 有問題傳簡報給老闆 → Custom Integration

---

### 5️⃣ 隨身遙控器：Cowork Dispatch 🎮

| 功能 | 說明 |
|------|------|
| **遠端控制** | 透過手機操控家裡或辦公室的 Claude Desktop |
| **用途** | 處理 Slack 訊息、管理檔案 |
| **目標** | 實現「不帶電腦也能工作」的自由 |

**Boris 名言**：
> "我不是在寫 Code，我就是在 Dispatch 的路上。"

---

### 6️⃣ 前端開發者的救星：Chrome 擴充功能 (beta) 🌐

| 功能 | 說明 |
|------|------|
| **自動測試** | 自己打開分頁看網頁跑得對不對 |
| **自動除錯** | 讀取 Console Log，發現錯誤直接原地修正 |
| **持續迭代** | 一直修到網頁完美呈現為止 |

**核心觀念**：
> "Give Claude a way to verify its output."
> 給 Claude 一個驗證輸出結果的方法，它就會迭代直到結果完美。

---

## 🔑 Hooks 的三大關鍵優點

### 1. 減少重複勞動（Context 載入）

| 情況 | 動作 |
|------|------|
| 沒用 Hook | 每次啟動都要手動打字說明專案背景 |
| 使用 SessionStart Hook | 自動執行腳本，載入最新專案文件、API 規格 |

### 2. 強化安全與追蹤（審核機制）

- **PreToolUse Hook** = 自動記錄儀
- 在 Claude 執行 Bash 指令前攔截並存到 Log
- 確保 AI 行為可追蹤、可稽核

### 3. 跨平台的靈活性（外部串接）

- 當 Claude 需要執行高風險操作時
- Hook 會把「確認按鈕」傳送到 WhatsApp 或手機 App
- 不需坐在電腦前盯著，卻依然保有最後控制權

---

## 💬 工程師米奇的補充

> Hooks 的核心價值在於「自動化的觸發點」與「標準化的流程控制」。

如果沒有 Hooks，每次啟動 Claude 都得手動餵資料、手動下指令。有了 Hooks，就像裝了感應燈，門一開（觸發條件），燈就自動亮（執行邏輯）。

---

## 📌 原文重點

**Boris Cherny**:
> "Use the Chrome extension for frontend work. The most important tip for using Claude Code is: give Claude a way to verify its output. Once you do that, Claude will iterate until the result is great."

---

## 與蘇茉家族的關係

| 蘇茉功能 | 對應 Boris 技巧 |
|----------|------------------|
| HEARTBEAT.md 自動檢查 | SessionStart Hook |
| 品管驗證 | PreToolUse Hook |
| 遠端控制需求 | Cowork Dispatch |
| 瀏覽器自動化 | Chrome extension |

---

## 標籤

#知識儲備 #ClaudeCode #Hooks #Dispatch #ChromeExtension #Boris #自動化 #遠端控制 #前端開發

---

*記錄者：總管蘇茉*
*時間：2026-04-09 20:25*
*研究方式：瀏覽器截圖 + 頁面分析*
