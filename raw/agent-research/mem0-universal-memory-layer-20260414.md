# Mem0：AI Agent 的通用記憶層

> 來源：GitHub - mem0ai/mem0
> 日期：2026-04-14
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 概述

**Mem0** ("mem-zero") 是一個為 AI 助理和 Agent 增強的**智慧記憶層**，能記住用戶偏好、適應個人需求，並持續學習。

---

## 🎯 核心標語

| 指標 | 數據 |
|------|------|
| **準確率** | +26% vs OpenAI Memory |
| **速度** | 91% Faster |
| **Token 用量** | 90% Lower |

---

## 🔑 核心功能

### 1. Multi-Level Memory（多層次記憶）

| 類型 | 說明 |
|------|------|
| **User Memory** | 用戶個人偏好 |
| **Session Memory** | 對話階段記憶 |
| **Agent Memory** | Agent 狀態 |

---

### 2. 開發者友好

- 直覺的 API
- 跨平台 SDKs
-  Fully managed service 選項

---

## 🎯 應用場景

| 場景 | 說明 |
|------|------|
| AI Assistants | 一致性、上下文豐富的對話 |
| Customer Support | 回憶過去票據和用戶歷史 |
| Healthcare | 追蹤患者偏好和歷史 |
| Productivity & Gaming | 基於用戶行為的自適應工作流程 |

---

## 📦 安裝方式

### pip
```bash
pip install mem0ai
```

### npm
```bash
npm install mem0ai
```

### CLI
```bash
npm install -g @mem0/cli
# 或
pip install mem0-cli
```

---

## 🔧 基本使用

```python
from openai import OpenAI
from mem0 import Memory

openai_client = OpenAI()
memory = Memory()

def chat_with_memories(message: str, user_id: str = "default_user") -> str:
    # 檢索相關記憶
    relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
    memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])
    
    # 生成回應
    system_prompt = f"You are a helpful AI. Answer based on query and memories.\nUser Memories:\n{memories_str}"
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}]
    response = openai_client.chat.completions.create(model="gpt-4.1-nano-2025-04-14", messages=messages)
    
    # 建立新記憶
    memory.add(messages, user_id=user_id)
    return response.choices[0].message.content
```

---

## 🔗 整合支援

| 平台 | 說明 |
|------|------|
| ChatGPT | Mem0 驅動的個人化聊天 |
| Browser Extension | 跨 ChatGPT, Perplexity, Claude 儲存記憶 |
| Langgraph | 用 Langgraph + Mem0 建立客服機器人 |
| CrewAI | 用 Mem0 定制 CrewAI 輸出 |

---

## 🏆 支援的模型

| 類型 | 預設 | 說明 |
|------|------|------|
| **LLM** | gpt-4.1-nano-2025-04-14 | 需要 LLM 才能運作 |
| **Embedding** | text-embedding-3-small | 預設 OpenAI |
| **推薦 Embedding** | Qwen 600M | 混合搜索最佳效果 |

---

## 📊 與我們的比較

| 功能 | Mem0 | SumoMemory |
|------|------|-------------|
| 多層次記憶 | ✅ User/Session/Agent | ✅ 類似 |
| 長期記憶 | ✅ | ✅ |
| API 簡單 | ✅ | ✅ |
| 開源 | ✅ Apache 2.0 | ✅ |

---

## 🤔 蘇茉觀察

1. **Mem0 是YC 投資的 startup**，有完整的產品和商業服務
2. **與 SumoMemory 概念相似**，但 Mem0 更偏向 SaaS 平台
3. 我們可以借鏡：
   - Mem0 的多層次記憶架構
   - 混合搜索（semantic + keyword + entity boosting）的實現
   - API 設計的簡潔性

---

## 🔗 連結

- 官網：https://mem0.ai
- 文件：https://docs.mem0.ai
- Discord：https://mem0.dev/DiG
- GitHub：https://github.com/mem0ai/mem0

---

*最後更新：2026-04-14*