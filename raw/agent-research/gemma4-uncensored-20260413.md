# Gemma4 Uncensored 模型研究

> 來源：Facebook - 喬瑟夫（OpenClaw 中文社群）
> 日期：2026-04-13
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 原始分享

> 開源的 Gemma4 表現不俗，既然要本地就是要玩 uncensored。
> 
> 目前為止表現最亮眼的 uncensored 模型：
> `fredrezones55/Gemma-4-Uncensored-HauhauCS-Aggressive`

---

## 🎯 模型資訊

| 項目 | 內容 |
|------|------|
| **模型名稱** | Gemma-4-Uncensored-HauhauCS-Aggressive |
| **作者** | fredrezones55 |
| **平台** | Hugging Face |
| **類型** | Uncensored LLM |

---

## 💡 為什麼要玩 Uncensored？

| 優點 | 說明 |
|------|------|
| **無內容限制** | 不會因為安全過濾而拒答 |
| **本地運行** | 隱私保護，不上傳資料 |
| **自託管** | 完全控制，可自由調整 |

---

## 🔧 下載方式

```bash
# 使用 huggingface-cli
huggingface-cli download fredrezones55/Gemma-4-Uncensored-HauhauCS-Aggressive

# 或使用 Python
from huggingface_hub import snapshot_download
snapshot_download("fredrezones55/Gemma-4-Uncensored-HauhauCS-Aggressive")
```

---

## 📋 蘇茉狀態

- [x] 已下載
- [ ] 已測試

---

## 📦 下載資訊

| 項目 | 內容 |
|------|------|
| **檔案名稱** | Gemma-4-E4B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf |
| **大小** | 4.97 GB |
| **位置** | `C:\butler_sumo\models\Gemma-4-E4B-Uncensored\` |
| **下載日期** | 2026-04-13 |

---

## 🔧 使用方式（ Ollama）

```bash
# 安裝 Ollama 模型
ollama pull HauhauCS/Gemma-4-E4B-Uncensored-HauhauCS-Aggressive:Q4_K_M

# 或參考 Hugging Face 的 llama-cli 用法
llama-cli -m Gemma-4-E4B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf --jinja -c 8192 -ngl 99
```

---

## 💭 備註

這是關於「本地 AI 模型」的研究，與蘇茉家族的語音/文字處理相關。

---

*最後更新：2026-04-13*
