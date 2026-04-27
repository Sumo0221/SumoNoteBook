# Gemma 4 + OpenClaw 三步驟本地部署

## 基本資訊

| 項目 | 內容 |
|------|------|
| **標題** | 三步驟在本機跑 Gemma 4 + OpenClaw，五分鐘搞定 |
| **來源** | AIOnDaily Facebook 粉絲專頁 |
| **時間** | 12 小時前（2026-04-09）|
| **連結** | https://www.facebook.com/share/17ZHNnv2Kf/ |

---

## 這是什麼？

一篇關於如何在本地端快速部署 **Gemma 4 + OpenClaw** 的教學貼文。

---

## 三步驟部署流程

### Step 1：安裝 Ollama

前往 `ollama.com/download` 下載安裝，支援：
- Mac
- Windows
- Linux

---

### Step 2：下載 Gemma 4 26B A4B 模型

```bash
ollama pull gemma4:26b-a4b
```

**推薦原因**：能力強 + 速度快，是本地跑 Agent 任務的最佳甜蜜點。

> 不過官方提到這步可跳過，Step 3 會自動處理（所以其實兩步驟就能搞定了）

---

### Step 3：一行指令啟動 OpenClaw + Gemma 4

```bash
ollama launch openclaw --model gemma4:26b-a4b
```

這行指令會：
1. 自動安裝 OpenClaw
2. 以 Gemma 4 作為後端直接啟動

就這樣，完成！

---

## 相關討論

| 問題 | 回覆 |
|------|------|
| 支援哪些系統？ | Mac 以及 Linux，不過都支援的（原文：Mac以及Linux，不過都支援的）|

---

## 與蘇茉家族的關係

| 項目 | 說明 |
|------|------|
| **蘇茉家族** | 已在使用 OpenClaw |
| **可能的整合** | 蘇茉可以考慮用 Gemma 4 作為本地模型 |
| **參考價值** | 本地部署 AI 模型的方法 |

---

## 標籤

#知識儲備 #Gemma4 #OpenClaw #本地AI #Ollama #AIOnDaily

---

*記錄者：總管蘇茉*
*時間：2026-04-09 09:56*
