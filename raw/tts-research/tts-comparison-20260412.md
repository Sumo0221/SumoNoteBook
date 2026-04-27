# TTS 系統比較總表

## 研究日期
2026-04-12

---

## 系統比較

| 系統 | GPU需求 | CPU支援 | 情緒控制 | 聲音克隆 | 語言支援 | 安裝難度 |
|------|---------|---------|----------|----------|----------|----------|
| **Fish Speech S2** | ✅ 24GB | ✅ | ✅ 15k+ 標籤 | ✅ | 80+ | 中等 |
| **GPT-SoVITS** | ✅ | ✅ | ⚠️ | ✅✅ | 中英日韓粵 | 簡單(Windows套件) |
| **F5-TTS** | ✅ | ❌ | ⚠️ | ✅ | 中英 | 需GPU |
| **IndexTTS-2** | ✅ GPU | ❌ | ✅ | ✅ | 中英 | 需uv |
| **MegaTTS3** | ✅ GPU | ❌ | ❌ | ✅ | 中英 | 需C++編譯器 |
| **Edge TTS** | ❌ | ✅ | ❌ | ❌ | 多語 | 簡單 |

---

## 詳細分析

### 1. Fish Speech S2（推薦 - CPU可用）

**優點**：
- ✅ CPU 可運行
- ✅ 情緒控制最強（15,000+ 標籤）
- ✅ 80+ 語言
- ✅ 聲音克隆
- ✅ 開源免費

**缺點**：
- ❌ GPU 版本需要 24GB VRAM

**安裝**：
```bash
pip install -e .[cpu]
```

---

### 2. GPT-SoVITS

**優點**：
- ✅ Windows 一鍵安裝包
- ✅ Few-shot 訓練（1分鐘資料）
- ✅ 聲音克隆效果好

**缺點**：
- ⚠️ 情緒控制不如 Fish Speech

**安裝**：
- 下載 7z 壓縮包
- 雙擊 go-webui.bat

---

### 3. IndexTTS-2

**優點**：
- ✅ 情緒表達強
- ✅ 時長控制（獨家）
- ✅ 開源

**缺點**：
- ❌ 需要 GPU
- ❌ 只能用 uv 安裝

---

### 4. MegaTTS3

**優點**：
- ✅ 口音控制
- ✅ 輕量（0.45B 參數）

**缺點**：
- ❌ 需要 C++ 編譯器（pynini）
- ❌ Windows 安裝困難

---

### 5. Edge TTS（現有系統）

**優點**：
- ✅ 已安裝
- ✅ 速度快
- ✅ 無需 GPU

**缺點**：
- ❌ 無法情緒控制
- ❌ 無法聲音克隆
- ❌ 官方音色

---

## 建議使用情境

| 需求 | 推薦系統 |
|------|----------|
| 不需要 GPU | Fish Speech S2 或 GPT-SoVITS |
| 情緒控制 | Fish Speech S2 |
| 聲音克隆（訓練） | GPT-SoVITS |
| 速度最快 | F5-TTS（需GPU）|
| 日常使用 | Edge TTS（已安裝）|

---

## 安裝記錄

| 日期 | 系統 | 狀態 |
|------|------|------|
| 2026-04-12 | Fish Speech S2 | 待安裝 |

---

## 參考連結

- Fish Speech S2：https://github.com/fishaudio/fish-speech
- GPT-SoVITS：https://github.com/RVC-Boss/GPT-SoVITS
- IndexTTS-2：https://github.com/index-tts/index-tts
- MegaTTS3：https://github.com/bytedance/MegaTTS3
- F5-TTS：https://github.com/SWivid/F5-TTS
- Edge TTS：已安裝
