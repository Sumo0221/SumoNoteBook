# TTS 研究報告：MegaTTS3

## 基本資訊

| 項目 | 內容 |
|------|------|
| **名稱** | MegaTTS 3 |
| **機構** | ByteDance（抖音/TikTok 母公司）|
| **GitHub** | https://github.com/bytedance/MegaTTS3 |
| **HuggingFace** | https://huggingface.co/ByteDance/MegaTTS3 |

## 核心功能

| 功能 | 說明 |
|------|------|
| **輕量高效** | Diffusion Transformer 只有 **0.45B 參數** |
| **高品質語音克隆** | Zero-Shot 聲音克隆 |
| **口音控制** | 可調整發音標準程度 |
| **Web UI** | Gradio 介面 |
| **支援 CPU** | CPU 可運行（約 30 秒推理）|

## 安裝需求

| 項目 | 需求 |
|------|------|
| **Python** | 3.10 |
| **GPU** | 可選（GPU 較快）|
| **系統** | Linux / Windows（測試中）/ Docker |

## 問題

### Windows 安裝障礙
- 需要 **pynini** 套件
- pynini 需要 C++ 編譯器
- 需要 Visual Studio Build Tools

## 命令列用法

```bash
# 基本克隆
python tts/infer_cli.py \
  --input_wav 'prompt.wav' \
  --input_text "要說的文字" \
  --output_dir ./gen

# 口音控制
python tts/infer_cli.py \
  --input_wav 'English_prompt.wav' \
  --input_text '這是一條有口音的音頻' \
  --output_dir ./gen \
  --p_w 1.0 --t_w 3.0
```

## 與 IndexTTS-2 比較

| 功能 | **MegaTTS3** | **IndexTTS-2** |
|------|---------------|-----------------|
| 參數大小 | **0.45B（輕量）** | 未公布 |
| **情緒控制** | ❌ | ✅✅ |
| **時長控制** | ❌ | ✅ |
| **口音控制** | ✅ | ❌ |
| **聲音克隆** | ✅ | ✅ |
| **Web UI** | ✅ | ✅ |
| **多語言** | 中英文 | 中英文 |

## 備註

- 2026-04-12 研究
- Windows 安裝有障礙（需要 C++ 編譯器）
- 不建議目前安裝
