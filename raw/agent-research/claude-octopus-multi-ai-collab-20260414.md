# Claude Octopus 與多 AI 協作工具

> 來源：Facebook - Generative AI 技術交流中心（YuShang Lung）
> 日期：2026-04-14
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 概述

原文標題：**你手上現在訂了幾個 AI？**
作者：YuShang Lung
時間：8小時前
讚：173 | 回覆：83 | 分享：8

---

## 🎯 核心問題

> 「Claude、ChatGPT、Gemini、Copilot⋯⋯每個月加起來也不少錢，但大多時候就是各開各的，哪個順手用哪個。」

---

## 🔧 Claude Octopus 介紹

一個 GitHub 上的第三方開源 plugin，讓多個 AI model 一起協作。

### 協作模式
| AI | 負責角色 |
|----|----------|
| Claude | 指揮、協調、整合 |
| Codex | 深度實作 |
| Gemini | 看生態系、資安 |

### 核心機制
- **75% 共識門檻**：三個 model 中有一個不同意，會攔下來讓你看
- **工作流程**：Discover → Define → Develop → Deliver（每階段有 quality gate）
- **Debate 功能**：讓多個 AI 對技術決策正式辯論（如 monorepo vs microservices）

### 實務面
- 不用一次設定 8 個 provider
- 只有 Claude 也能用全部的 persona、workflow
- Codex、Gemini 走 OAuth 不需另外付費
- Qwen 每天有免費額度
- 目前 2.6k stars

---

## 🤖 OpenAI 官方 Codex Plugin

**名稱**：codex-plugin-cc

### 功能
- 在 Claude Code 裡直接委派任務給 Codex
- adversarial review
- 背景執行任務
- rescue 模式（Codex 在 Claude 卡住時主動接手）

---

## 📊 兩者比較

| 工具 | 特色 |
|------|------|
| **Codex Plugin** | 輕量、Claude + Codex 雙引擎協作 |
| **Claude Octopus** | 最多 8 個 provider、consensus gate、32 個專家人格 |

---

## 💬 網友回應精選

### Guts Yang - 三方協同作業
> 「VS code 中我下指令給 Claude code，然後叫它指揮 Codex 與 Gemini CLI，我稱為三方協同作業。
> 後來發現 Gemini 是絕對的小弟。」

### Samson Fu
> 「那不就是 MAGI 嗎？」

### Yulun Yeh
> 「OpenClaw 一天內都能 20 美元的配額燒光。感覺沒做幾件事情就燒光了。」

---

## 💡 蘇茉觀察

多 AI 協作的價值：
1. **不同角度檢查** - 減少單一模型的盲點
2. **共識機制** - 75% 門檻可以過濾明顯錯誤
3. **成本考量** - 需要評估 token 消耗是否值得

---

## 🔗 相關連結

- Claude Octopus：https://github.com/（需進一步查詢）
- Codex Plugin：codex-plugin-cc

---

*最後更新：2026-04-14*