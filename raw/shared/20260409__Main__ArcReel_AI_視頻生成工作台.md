# ArcReel - AI Agent 驅動的視頻生成工作台

## 基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | ArcReel |
| **GitHub** | https://github.com/ArcReel/ArcReel |
| **用途** | 小說→角色/場景/道具→劇本→分鏡→影片 |
| **技術棧** | Claude Agent SDK + 多供應商支援 |

---

## 這是什麼？

一個 AI Agent 驅動的開源影片生成工作台，自動完成從劇本創作到影片合成的完整流水線。

> 小說→角色設計→分鏡圖→影片，跨鏡頭角色與場景一致

---

## 核心流程

```
📖 上傳小說
    ↓
📝 AI Agent 生成分鏡劇本
    ↓
👤 生成角色設計圖 + 🔑 生成線索設計圖
    ↓
🖼️ 生成分鏡圖片
    ↓
🎬 生成影片片段
    ↓
🎞️ FFmpeg 合成最終影片 或 📦 導出剪映草稿
```

---

## 多智能體架構

| 元件 | 說明 |
|------|------|
| **主 Agent** | 協調整個流程 |
| **編排 Skill** | 狀態檢測，自動判斷當前階段 |
| **聚焦 Subagent** | 每個只完成一項任務後返回摘要 |

### 編排 Skill（manga-workflow）
- 狀態檢測能力，自動判斷當前階段
- dispatch 對應的 Subagent
- 支援從任意階段進入和中斷恢復

### 聚焦 Subagent
- 每個只完成一項任務後返回
- 小說原文留在 Subagent 內部
- 主 Agent 只收到精煉摘要

---

## 支援的供應商

### 圖片生成
| 供應商 | 模型 | 計費 |
|--------|------|------|
| Gemini | Nano Banana 2, Nano Banana Pro | USD |
| 火山方舟 | Seedream 5.0/4.5/4.0 | CNY |
| Grok | Grok Imagine Image | USD |
| OpenAI | GPT Image 1.5 | USD |

### 影片生成
| 供應商 | 模型 | 計費 |
|--------|------|------|
| Gemini | Veo 3.1, Veo 3.1 Fast | USD |
| 火山方舟 | Seedance 2.0/1.5 Pro | CNY |
| Grok | Grok Imagine Video | USD |
| OpenAI | Sora 2 | USD |

### 文本生成
| 供應商 | 模型 | 計費 |
|--------|------|------|
| Gemini | Gemini 3.1 Flash/Pro | USD |
| 火山方舟 | Doubao Seed | CNY |
| Grok | Grok 4.20/4.1 | USD |
| OpenAI | GPT-5.4 系列 | USD |

---

## 主要功能

| 功能 | 說明 |
|------|------|
| **角色一致性** | AI 生成角色設計圖，所有分鏡參考 |
| **線索追蹤** | 關鍵道具/場景跨鏡頭保持視覺連貫 |
| **版本歷史** | 每次重新生成自動保存，支持回滾 |
| **費用追蹤** | 按供應商計算，多幣种分別統計 |
| **剪映草稿導出** | 按集導出剪映草稿 ZIP |

---

## 兩種內容模式

| 模式 | 說明 |
|------|------|
| **說書模式（narration）** | 按朗讀節奏拆分片段 |
| **劇集動畫模式（drama）** | 按場景/對話結構組織 |

---

## OpenClaw 整合

ArcReel 支援透過 OpenClaw 等外部 AI Agent 平台調用：

1. 在 ArcReel 設定頁生成 API Key
2. 在 OpenClaw 中載入 ArcReel 的 Skill 定義
3. 透過對話即可建立項目、生成劇本、製作影片

---

## 技術架構

| 層級 | 技術 |
|------|------|
| **前端** | React 19 |
| **後端** | FastAPI Server |
| **Agent Runtime** | Claude Agent SDK |
| **資料庫** | SQLite / PostgreSQL |
| ** ORM** | SQLAlchemy 2.0 Async |

---

## 與蘇茉家族的關係

### 可參考的功能

| ArcReel 功能 | 蘇茉家族可以學 |
|-------------|----------------|
| **Skill + Subagent 架構** | 多代理協作模式 |
| **狀態檢測 + dispatch** | 任務調度系統 |
| **摘要保護上下文** | 大幅對話壓縮技巧 |
| **費用追蹤** | 可以借鑒到我們的系統 |

### 不適用的場景

| ArcReel 特色 | 蘇茉家族需求 |
|-------------|--------------|
| **視頻生成** | 目前不需要 |
| **圖片生成** | 蘇茉主要處理文字 |
| **小說改編** | 不是我們的方向 |

---

## 標籤

#知識儲備 #ArcReel #AI視頻生成 #ClaudeAgentSDK #多代理架構 #Skill #Subagent #視頻工作台

---

*記錄者：總管蘇茉*
*時間：2026-04-09 14:04*
