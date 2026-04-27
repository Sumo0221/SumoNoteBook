# GoLLM - 智慧本地 LLM 路由代理

## 基本資訊

| 項目 | 內容 |
|------|------|
| **名稱** | GoLLM |
| **作者** | echo-of-machines |
| **GitHub** | https://github.com/echo-of-machines/gollm |
| **用途** | 多後端本地 LLM 容器管理器 + 瀏覽器 GUI |
| **API** | OpenAI 相容 |

---

## 這是什麼？

GoLLM 是一個**智慧路由代理**，架在各應用程式和本地 LLM 推理後端之間。

**痛點**：跑多個本地 LLM 需要管理 Docker 容器、GPU 記憶體，手動停止舊模型才能啟動新模型。

**解決方案**：一個端點（localhost:30000），任何模型。GoLLM 自動處理負載、交換、生命周期。

---

## 核心功能

| 功能 | 說明 |
|------|------|
| **智慧模型路由** | 自動載入請求的模型，透明切換 |
| **多後端支援** | SGLang、vLLM、自訂 Docker 映像 |
| **RAM 感知交換** | 載入前檢查 /proc/meminfo，防止 OOM |
| **飛行請求洩洪** | 交換前等待活躍請求完成 |
| **別名解析** | 多個名稱指向同一模型 |
| **瀏覽器 GUI** | http://localhost:30000/ui/ |
| **即時終端** | WebSocket 容器日誌串流 |
| **OpenAI 相容 API** | 任何 OpenAI 用戶端庫直接使用 |
| **HuggingFace 整合** | 直接下載 gated models |

---

## 架構圖

```
Clients (curl, apps, AI agents)
         │
         ▼
GoLLM Router (:30000)
┌─────────────────────┐
│ OpenAI-compat API │ ← /v1/chat/completions, /v1/models
│ Management API │ ← /router/*
│ Browser GUI │ ← /ui/
│ WebSocket logs │ ← /ws/logs
└────────┬────────────┘
         │ Docker socket
         ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│ SGLang    │ │ vLLM       │ │ Custom     │
│ :30000    │ │ :8000      │ │ :port      │
└────────────┘ └────────────┘ └────────────┘
```

---

## 支援的後端

| 後端 | 映像 | 連接埠 | 用途 |
|------|------|--------|------|
| SGLang | lmsysorg/sglang:dev-cu13 | 30000 | 高效能推理、MoE 模型 |
| vLLM | vllm/vllm-openai:latest | 8000 | 廣泛模型支援、OpenAI 相容 |
| Custom | 使用者提供 | 8000 | 模型特定映像、實驗性建置 |

---

## API 端點

| 端點 | 方法 | 描述 |
|------|------|------|
| `/health` | GET | 路由健康檢查 |
| `/v1/chat/completions` | POST | OpenAI 相容聊天推理 |
| `/v1/completions` | POST | OpenAI 相容文字補全 |
| `/v1/models` | GET | 列出可用模型 |
| `/router/swap/{key}` | POST | 載入/切換模型 |
| `/router/models` | GET | 列出已註冊模型 |
| `/router/models/install` | POST | 安裝新模型 |
| `/router/system` | GET | 系統狀態（RAM、活躍模型）|
| `/router/hf-token` | GET/POST | 管理 HuggingFace token |
| `/ui/` | GET | 瀏覽器 GUI |

---

## 安裝方式

```bash
# 1. Clone the repo
git clone https://github.com/echo-of-machines/gollm.git
cd gollm

# 2. Configure (optional)
cp .env.example .env
# Edit .env to set your HF_TOKEN and port

# 3. Start GoLLM
docker compose up -d --build model-router

# 4. Open the GUI
xdg-open http://localhost:30000/ui/ # Linux
open http://localhost:30000/ui/ # macOS
```

---

## 需求

- Docker with Compose plugin
- NVIDIA GPU with drivers installed
- NVIDIA Container Toolkit

---

## Python 使用範例

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:30000/v1", api_key="unused")

# 列出可用模型
models = client.models.list()

# 聊天完成 — GoLLM 自動載入請求的模型
response = client.chat.completions.create(
    model="qwen3.5",
    messages=[{"role": "user", "content": "Hello"}],
)
```

---

## 與蘇茉家族的關係

| 項目 | 說明 |
|------|------|
| **蘇茉家族參考** | 本地 LLM 管理的解決方案 |
| **API 整合** | 可以整合到蘇茉的 LLM 設定 |
| **價值** | 讓本地跑多個 LLM 模型更容易 |

---

## 標籤

#知識儲備 #GoLLM #本地LLM #模型路由 #Docker #vLLM #SGLang #OpenAI

---

*記錄者：總管蘇茉*
*時間：2026-04-09 10:33*
