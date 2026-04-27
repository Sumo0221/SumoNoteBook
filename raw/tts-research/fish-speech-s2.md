# TTS 研究報告：Fish Speech S2

## 基本資訊

| 項目 | 內容 |
|------|------|
| **名稱** | Fish Audio S2 / Fish Speech S2 |
| **機構** | Fish Audio |
| **GitHub** | https://github.com/fishaudio/fish-speech |
| **模型** | S2-Pro (4B 參數) |
| **論文** | arXiv:2603.08823 |

## 核心功能

| 功能 | 說明 |
|------|------|
| **情緒標籤** | 15,000+ 種（[whisper], [angry], [laughing] 等）|
| **聲音克隆** | 10-30 秒參考音頻 |
| **多語言** | 80+ 種語言（含中文）|
| **多說話人** | 支援對話生成 |
| **即時生成** | H200 GPU: RTF 0.195, TTFA ~100ms |

## 安裝需求

| 安裝方式 | 需求 |
|----------|------|
| **GPU 版本** | 24GB VRAM |
| **CPU 版本** | ✅ 可以安裝！ |

### CPU 安裝命令

```bash
# CPU 安裝
pip install -e .[cpu]

# 或 Docker CPU
BACKEND=cpu docker compose --profile webui up
```

## 效能評測

| 測試 | 分數 |
|------|------|
| 中文 WER | 0.54%（最佳）|
| 英文 WER | 0.99%（最佳）|
| Audio Turing Test | 0.515（超越 Seed-TTS 24%）|
| 情緒控制品質 | 4.51/5.0 |

## 情緒標籤範例

```
[whisper] - 輕聲細語
[angry] - 憤怒
[laughing] - 笑聲
[excited] - 興奮
[sad] - 悲傷
[pause] - 停頓
[emphasis] - 強調
...共 15,000+ 種！
```

## 與其他 TTS 比較

| 系統 | GPU 需求 | 情緒控制 | 語言支援 |
|------|----------|----------|----------|
| **Fish Speech S2** | ✅ CPU 可運行 | ✅ 15,000+ | 80+ |
| IndexTTS-2 | ❌ 需要 GPU | ✅ | 中英文 |
| MegaTTS3 | ❌ 需要 GPU | ❌ | 中英文 |
| Edge TTS | ✅ 不需要 | ❌ | 多語 |

## 安裝狀態

- [ ] 待安裝

## 備註

- 2026-04-12 研究
- 老爺選擇先試用此系統
