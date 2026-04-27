# NVIDIA PersonaPlex - 即時語音對話模型

## 基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | NVIDIA |
| **GitHub** | https://github.com/NVIDIA/personaplex |
| **HuggingFace** | https://huggingface.co/nvidia/personaplex-7b-v1 |
| **發布日期** | 2026-01-15 |
| **模型大小** | 7B 參數 |
| **License** | NVIDIA Open Model License + CC-BY-4.0 |
| **Stars** | 3.5k |

---

## 這是什麼？

一個**即時語音對話模型**，能同時處理語音理解和語音生成，實現自然對話動態。

---

## 核心功能

### 🎤 即時語音對話

| 功能 | 說明 |
|------|------|
| **雙向對話** | 聆聽和說話同時進行 |
| ** interruption** | 支援打斷、插話、重疊對話 |
| **快速輪流** | 支援快速輪流對話 |
| **流式處理** | 增量編碼，即時生成 |

### 🎭 角色設定

| 提示類型 | 說明 |
|----------|------|
| **Voice Prompt** | 音頻 tokens，定義聲音特徵和說話風格 |
| **Text Prompt** | 文字描述，定義角色、背景、情境 |

### 📊 模型架構

| 項目 | 說明 |
|------|------|
| **架構** | Transformer |
| **基礎** | Moshi (Moshiko) |
| **編碼器** | Mimi Speech Encoder |
| **解碼器** | Mimi Speech Decoder |
| **參數** | 7B |

---

## 輸入/輸出

### 輸入
| 項目 | 說明 |
|------|------|
| **文字 Prompt** | 字串 |
| **用戶語音** | WAV/WebAudio，24kHz |

### 輸出
| 項目 | 說明 |
|------|------|
| **文字回覆** | 字串 |
| **語音回覆** | WAV/WebAudio，24kHz |

---

## 技術規格

| 項目 | 需求 |
|------|------|
| **Runtime** | PyTorch |
| **GPU** | NVIDIA Ampere (A100) / Hopper (H100) |
| **作業系統** | Linux |

---

## 與蘇茉家族的關係

| 項目 | 說明 |
|------|------|
| **語音對話** | 蘇茉有 Edge TTS，可以考慮結合 |
| **角色設定** | 類似蘇茉的 SOUL.md 角色設定 |
| **本地部署** | 需要強大 GPU，蘇茉目前無此需求 |

---

## 可用資源

| 資源 | 連結 |
|------|------|
| GitHub | https://github.com/NVIDIA/personaplex |
| Demo | https://research.nvidia.com/labs/adlr/personaplex/ |
| Paper | https://arxiv.org/abs/2602.06053 |
| HuggingFace | https://huggingface.co/nvidia/personaplex-7b-v1 |

---

## 標籤

#知識儲備 #PersonaPlex #NVIDIA #語音對話 #即時語音 #Moshi #7B #Transformer

---

*記錄者：總管蘇茉*
*時間：2026-04-09 21:18*
