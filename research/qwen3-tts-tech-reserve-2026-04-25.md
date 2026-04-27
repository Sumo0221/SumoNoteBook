# Qwen3-TTS 技術儲備文件
Source: https://github.com/QwenLM/Qwen3-TTS
Date: 2026-04-25

## 基本資訊
- 開發者：阿里巴巴 Qwen 團隊
- 類型：開源 TTS 模型
- 模型大小：0.6B / 1.7B 兩種規格
- 語言支援：10 種語言（中文、英語、日、韓、德、法、俄、葡、西、義）

## 三大模式

### 1. Voice Design（語音設計）
- 用自然語言描述想要的聲音
- 可控制音色、情緒、語調
- 適合：想要獨特聲音但沒有參照音頻

### 2. Custom Voice（自訂音色）
- 內建 9 種預設音色
- 中文：Vivian（年輕女聲）、Serena（溫柔女聲）、Uncle_Fu（低沉男聲）、Dylan（北京腔男聲）、Eric（四川腔男聲）
- 英文：Ryan（有活力男聲）、Aiden（陽光男聲）
- 日文：Ono_Anna（可愛女聲）
- 韓文：Sohee（溫暖女聲）
- 可用 instruct 控制情緒（憤怒、快樂、悲傷等）

### 3. Voice Clone（聲音複製）
- 只要 3 秒鐘音頻即可克隆
- 支援 base64、URL、檔案路徑
- 需要提供 ref_audio 和 ref_text

## 技術亮點
- 延遲低至 97ms（端到端）
- 支援串流輸出
- 不需要 DiT 架構（非擴散架構）
- FlashAttention 2 加速

---

## 硬體需求（技術儲備重點）

### GPU VRAM 需求

| 模型 | VRAM（FP16） | VRAM（Int4量化） |
|------|-------------|----------------|
| 0.6B | ~2.5-3.2GB | ~1.5GB |
| 1.7B | ~5.2-5.8GB | ~3.1GB |

### GPU vs CPU

| 方案 | 延遲 | 適合場景 |
|------|------|----------|
| GPU RTX 4090 (24GB) | 97ms | 即時語音助理 |
| GPU RTX 3060 (12GB) | 125ms | 個人專案 |
| CPU Only (64GB RAM) | 850ms-1.6s | 離線批次處理 |

### 安裝必要條件
- Python 3.12 環境
- CUDA 12.x + PyTorch 2.0+
- GPU VRAM 建議 8GB 以上

### 安裝指令
`ash
pip install -U qwen-tts
pip install -U flash-attn --no-build-isolation
`

---

## 對蘇茉的意義
- 可考慮整合到 Sumo_Voice 系統
- 目前蘇茉用 Edge TTS，若要更高品質可考慮 Qwen3-TTS
- 需要 GPU 才能跑（建議 8GB+ VRAM）

## 待確認事項
- 老爺的 GPU 型號和 VRAM 大小
- 是否要整合進 SumoVoice
- 可否克隆老爺或夫人的聲音
