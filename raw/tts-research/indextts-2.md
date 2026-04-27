# TTS 研究報告：IndexTTS-2

## 基本資訊

| 項目 | 內容 |
|------|------|
| **名稱** | IndexTTS-2 |
| **機構** | IndexTeam（Bilibili） |
| **GitHub** | https://github.com/index-tts/index-tts |
| **HuggingFace** | https://huggingface.co/IndexTeam/IndexTTS-2 |
| **論文** | arXiv:2506.21619 |

## 核心功能

| 功能 | 說明 |
|------|------|
| **情緒表達** | Zero-Shot 情緒語音生成，完美重現音頻中的情緒 |
| **時長控制** | 首次在自回歸 TTS 中實現精確時長控制 |
| **音色+情緒解耦** | 可以獨立控制音色和情緒 |
| **文字情緒描述** | 用自然語言（如「開心」「生氣」）控制情感 |
| **多語言** | 支援中英文 |

## 技術創新

### 1. 時長控制（Duration Control）
```
輸入文字 + 指定時長（0.75x / 1.0x / 1.25x）
→ 生成符合指定時長的語音
```

### 2. 情緒解耦（Emotion Disentanglement）
- **音色 prompt**：從一個音頻提取音色
- **情緒 prompt**：從另一個音頻提取情緒
- **兩者可以獨立控制！**

### 3. 文字情緒控制（Text-based Emotion）
```
輸入：「有點快樂，哈哈」
或：「超級無敵爆炸生氣」
→ 模型生成對應情緒的語音
```

## GPU 需求

| 需求 | 說明 |
|------|------|
| **需要 GPU** | ✅ 是 |
| **CUDA 版本** | 12.8+ |

## 安裝方式

```bash
# 只支援 uv
uv sync --all-extras

# 或
pip install -U uv
uv sync --all-extras
```

## 與其他 TTS 比較

| 系統 | 情緒控制 | 時長控制 | 聲音克隆 | 需求 |
|------|----------|----------|----------|------|
| **IndexTTS-2** | ✅✅ | ✅ | ✅✅ | 需要 GPU |
| Edge TTS | ❌ | ❌ | ❌ | 不需要 |

## 備註

- 2026-04-12 研究
- 需要 GPU，目前不適合我們
