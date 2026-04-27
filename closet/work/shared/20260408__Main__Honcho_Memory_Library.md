# Honcho - Stateful Agents 記憶庫

## 基本資訊

| 項目 | 內容 |
|------|------|
| **名稱** | Honcho |
| **GitHub** | https://github.com/plastic-labs/honcho |
| **網站** | https://app.honcho.dev |
| **用途** | 為 AI Agent 建立和維護狀態的記憶庫 |
| **特點** | 持續學習系統，理解隨時間變化的實體 |
| **支援** | Python SDK、TypeScript SDK |

---

## 這是什麼？

Honcho 是一個開源的記憶庫，用於構建有狀態的 AI Agent。

> 使用任何模型、框架或架構。它使 Agent 能夠建立和維護關於任何實體的狀態——用戶、Agent、群組、想法等等。

---

## 核心功能

| 功能 | 說明 |
|------|------|
| **持續學習** | 理解實體隨時間的變化 |
| **多模型支援** | 任何模型、框架或架構 |
| **工作流程設定** | 輕鬆設定應用程式工作流程 |
| **互動歷史** | 保存互動歷史 |
| **推理利用** | 利用 Agent 的推理來 informs 行為 |
| **搜尋** | 搜尋相似的訊息 |
| **表達** | 取得 session-scoped 的 peer 表示 |

---

## 安裝方式

```bash
# Python
pip install honcho-ai
uv add honcho-ai
poetry add honcho-ai
```

---

## 基本使用範例

```python
from honcho import Honcho

# 1. 初始化 Honcho client
honcho = Honcho(workspace_id="my-app-testing")

# 2. 初始化 peers
alice = honcho.peer("alice")
tutor = honcho.peer("tutor")

# 3. 建立 session 並添加訊息
session = honcho.session("session-1")
session.add_messages([
    alice.message("Hey there — can you help me with my math homework?"),
    tutor.message("Absolutely. Send me your first problem!"),
])

# 4. 利用推理來 informs agent 行為
response = alice.chat("What learning styles does the user respond to best?")
```

---

## 架構

| 元件 | 說明 |
|------|------|
| **FastAPI Server** | 儲存應用程式狀態 |
| **Python SDK** | Pypi: honcho-ai |
| **TypeScript SDK** | NPM: @honcho-ai/sdk |
| **PostgreSQL + pgvector** | 資料庫 |
| **Deriver Worker** | 生成錳述、摘要、peer cards、管理 dreaming 任務 |

---

## 與蘇茉家族的關係

| Honcho 功能 | 蘇茉家族現有 |
|-------------|--------------|
| 記憶系統 | ✅ 有（MemPalace, SumoNoteBook, Memory Dream）|
| 持續學習 | ⚠️ 部分（Memory Dream 正在實作）|
| 多模型支援 | ✅ 有 |

---

## 標籤

#知識儲備 #Honcho #AI記憶 #StatefulAgents #PlasticLabs

---

*記錄者：總管蘇茉*
*時間：2026-04-08 23:04*
