# Whisper CTranslate2 - 高速 Whisper 命令列工具

## 基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Softcatala |
| **GitHub** | https://github.com/Softcatala/whisper-ctranslate2 |
| **PyPI** | whisper-ctranslate2 |
| **Stars** | 2.5k+ |
| **功能** | 加速版 Whisper 命令列工具 |

---

## 這是什麼？

一個與 OpenAI Whisper CLI 相容的加速版本，基於 CTranslate2 和 Faster-Whisper 實作，**速度比原版快最多 16 倍**。

---

## 核心功能

### ⚡ 速度優勢

| 項目 | 說明 |
|------|------|
| **相同精度** | 比 OpenAI Whisper 快 4 倍 |
| **批次推理** | 最多 16 倍加速 |
| **記憶體** | 使用更少記憶體 |

### 🎯 主要功能

| 功能 | 說明 |
|------|------|
| **命令列相容** | 與 OpenAI Whisper CLI 相容 |
| **GPU 支援** | NVIDIA cuBLAS 11.x |
| **CPU 支援** | Intel MKL, OpenBLAS, Apple Accelerate, AArch64 |
| **說話者辨識** | Speaker Diarization（需 pyannote.audio）|
| **VAD 過濾** | Silero VAD 語音活動偵測 |
| **自訂模型** | 支援載入自己微調的 Whisper 模型 |
| **即時轉錄** | 從麥克風即時轉錄 |
| **置信度顯示** | 顏色編碼顯示置信度 |

---

## 安裝方式

### pip 安裝
```bash
pip install whisper-ctranslate2
```

### Docker
```bash
docker pull ghcr.io/softcatala/whisper-ctranslate2:latest
```

---

## 使用方式

### 基本轉錄
```bash
whisper-ctranslate2 audio.mp3 --model medium
```

### 翻譯（英文）
```bash
whisper-ctranslate2 audio.mp3 --model medium --task translate
```

### 批次推理（額外 2-4 倍加速）
```bash
whisper-ctranslate2 audio.mp3 --batched True
```

### CPU 優化
```bash
whisper-ctranslate2 audio.mp3 --compute_type int8
```

### 啟用 VAD 過濾
```bash
whisper-ctranslate2 audio.mp3 --vad_filter True
```

### 即時轉錄（麥克風）
```bash
whisper-ctranslate2 --live_transcribe True --language en
```

### 說話者辨識
```bash
whisper-ctranslate2 audio.mp3 --hf_token YOUR_HF_TOKEN
```

---

## 與蘇茉現有語音轉文字的比較

| 項目 | 蘇茉現有（Edge TTS）| whisper-ctranslate2 |
|------|---------------------|---------------------|
| **用途** | 文字轉語音（TTS）| 語音轉文字（STT）|
| **方向** | 輸出語音 | 輸入語音 |
| **速度** | 即時 | 取決於模型大小 |
| **本地部署** | ✅ | ✅ |
| **GPU 加速** | N/A | ✅ |

---

## 💡 對蘇茉家族的價值

| 項目 | 說明 |
|------|------|
| **語音轉文字** | 蘇茉有 Edge TTS（文字→語音），這個可以做語音→文字 |
| **本地 STT** | 不需要雲端 API，本地即可語音轉文字 |
| **會議記錄** | 可結合說話者辨識做會議紀錄 |
| **即時翻譯** | 可翻譯音訊為英文 |

---

## ⚠️ 與蘇茉現有系統的關係

蘇茉目前有：
- **Edge TTS** - 文字轉語音（輸出）
- **faster-whisper** - 語音轉文字（本地）
- **Groq Whisper** - 雲端語音轉文字

whisper-ctranslate2 是另一個本地 STT 選擇，特點是**速度快**。

---

## 標籤

#知識儲備 #Whisper #CTranslate2 #語音轉文字 #STT #本地部署 #GPU加速 #說話者辨識

---

*記錄者：總管蘇茉*
*時間：2026-04-10 09:11*
