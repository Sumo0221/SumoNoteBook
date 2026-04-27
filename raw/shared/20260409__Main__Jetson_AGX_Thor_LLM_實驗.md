# Jetson AGX Thor LLM 實驗 - harryliou

## 基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | harryliou |
| **GitHub** | https://github.com/harryliou/jetson-thor-llm-study |
| **主題** | 在 NVIDIA Jetson AGX Thor 上跑 LLM 的實驗記錄 |

---

## 機器規格

| 項目 | 規格 |
|------|------|
| **機器** | NVIDIA Jetson AGX Thor |
| **記憶體** | 128 GB unified memory（GPU + CPU 共用）|
| **GPU** | Blackwell sm_110a，20 SM，FP4 tensor cores |
| **磁碟** | 936 GB NVMe |

---

## 模型測試結果

| 模型 | 推理引擎 | 狀態 | 效能 |
|------|----------|------|------|
| Qwen3.5-122B-A10B（NVFP4）| vLLM 0.19.0 | ✅ 跑起來 | 9.7 tok/s |
| Gemma 4 26B-A4B / 31B（GGUF）| llama.cpp | ✅ 運行中 | SWA 問題 |

---

## 效能瓶頸分析

| 硬體 | SM 數量 | NVFP4 TOPS | 定位 |
|------|---------|------------|------|
| Jetson AGX Thor | 20 | — | 邊緣裝置（機器人/自駕）|
| GB10（DGX Spark）| 48 | 1000 | 桌面 AI server |
| H100 SXM | 132 | — | datacenter |

**結論**：9.7 tok/s 跑 122B 模型是**硬體天花板**，不是設定問題。

---

## sm_110a 的限制

| 問題 | 說明 |
|------|------|
| **FP4 tensor core** | Thor 的 sm_110a 有 FP4 tensor core，NVFP4 模型可執行 |
| **效能問題** | 最高效能的 MoE NVFP4 kernel 只針對 sm_100，sm_110a 全部 skip |
| **結論** | 「支援 sm_110a」≠「跑得好」——能跑起來，但不是最優路徑 |

---

## Gemma 4 SWA 問題

| 問題 | 說明 |
|------|------|
| **原因** | Gemma 4 整個家族使用 SWA（Sliding Window Attention） |
| **影響** | llama.cpp 的 KV cache 跨 request 失效 |
| **後果** | 每次請求都需完整 prefill system prompt（約 21K token 需 31 秒）|
| **結論** | 這是模型架構問題，換推理引擎也無法解決 |

---

## 需要的客製 Image

| Image | 用途 | 備註 |
|-------|------|------|
| `ghcr.io/nvidia-ai-iot/vllm:latest-jetson-thor` | vLLM 推理 | vLLM 0.19.0，CUDA 13.0，sm_110a 可用 |
| `ghcr.io/nvidia-ai-iot/llama_cpp:gemma4-jetson-thor` | llama.cpp 推理 | Gemma 4 GGUF 用 |

---

## 與蘇茉家族的關係

| 項目 | 說明 |
|------|------|
| **蘇茉家族參考** | 本地部署 LLM 的經驗和問題 |
| **FP4 推理** | 可參考 sm_110a 的效能限制 |
| **Gemma 4 SWA 問題** | 選模型時要注意 SWA 架構的影響 |

---

## 標籤

#知識儲備 #JetsonAGXThor #LLM #本地AI #NVIDIA #EdgeAI

---

*記錄者：總管蘇茉*
*時間：2026-04-09 10:27*
