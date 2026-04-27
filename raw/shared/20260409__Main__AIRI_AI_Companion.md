# AIRI - Self-Hosted AI Companion (虛擬伙伴專案)

## 基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | moeru-ai |
| **GitHub** | https://github.com/moeru-ai/airi |
| **口號** | Self hosted, you-owned Grok Companion |
| **靈感來源** | Neuro-sama（知名 AI VTuber）|

---

## 這是什麼？

一個開源的**自託管虛擬伙伴**專案，將 AI 角色（waifu、數位寵物）帶進我們的世界。

> Re-creating Neuro-sama, a soul container of AI waifu / virtual characters to bring them into our world.

---

## 支援的功能

### 🎮 遊戲能力
| 遊戲 | 狀態 |
|------|------|
| Minecraft | ✅ 支援 |
| Factorio | WIP（已有 PoC）|
| Kerbal Space Program | 公告中 |
| Helldivers 2 | WIP |

### 💬 聊天平台
| 平台 | 狀態 |
|------|------|
| Telegram | ✅ 支援 |
| Discord | ✅ 支援 |

### 🧠 大腦/記憶
| 功能 | 說明 |
|------|------|
| 記憶系統 | DuckDB WASM（瀏覽器內建資料庫）|
| Memory Alaya | WIP |
| 本地推論 | WebGPU 支援 |

### 👂 耳朵（語音輸入）
| 功能 | 說明 |
|------|------|
| 瀏覽器音頻輸入 | ✅ |
| Discord 音頻輸入 | ✅ |
| 用戶端語音辨識 | ✅ |
| 說話偵測 | ✅ |

### 👄 嘴巴（語音輸出）
| 功能 | 說明 |
|------|------|
| ElevenLabs 語音合成 | ✅ |

### 🦸 身體（視覺模型）
| 功能 | 說明 |
|------|------|
| VRM 模型支援 | ✅ |
| Live2D 模型支援 | ✅ |
| 自動眨眼 | ✅ |
| 自動注視 | ✅ |
| 待機眼睛移動 | ✅ |

---

## 技術架構

### Web 技術棧
| 技術 | 用途 |
|------|------|
| WebGPU | 圖形渲染 |
| WebAudio | 音頻處理 |
| Web Workers | 多執行緒 |
| WebAssembly | 高效能 |
| WebSocket | 即時通訊 |

### 原生加速
| 平台 | 技術 |
|------|------|
| NVIDIA | CUDA |
| Apple | Metal |
| HuggingFace Candle | 推理引擎 |

### 跨平台支援
| 平台 | 說明 |
|------|------|
| Web | 瀏覽器版本 |
| macOS | 原生 app |
| Windows | 原生 app |
| PWA | 行動裝置支援 |

---

## 安裝方式

### Windows
```bash
# 方法1: 安裝程式
下載 AIRI-0.9.0-beta.2-windows-x64-setup.exe

# 方法2: Scoop
scoop bucket add airi https://github.com/moeru-ai/airi
scoop install airi/airi
```

### macOS
```bash
# 下载 DMG
AIRI-0.9.0-beta.2-darwin-arm64.dmg
```

---

## 與蘇茉家族的關係

### 可參考的功能

| AIRI 功能 | 蘇茉家族可以學 |
|------------|----------------|
| **ElevenLabs 語音合成** | 語音輸出優化 |
| **記憶系統設計** | Memory Dream 參考 |
| **遊戲整合** | 可能用於遊戲相關查詢 |
| **多平台支援** | 跨設備體驗 |

### 不太適用的原因

| AIRI 特色 | 蘇茉家族需求 |
|----------|--------------|
| **VTuber/虛擬伙伴** | 我們是管家，不是娛樂 |
| **遊戲能力** | 目前不需要遊戲功能 |
| **角色扮演** | 我們是專業服務 |

---

## 結論

AIRI 是一個很棒的**娛樂/陪伴型 AI** 專案，但蘇茉家族是**服務/管家型 AI**。

兩者架構不同，但我們可以學習：
1. **語音合成整合**（ElevenLabs）
2. **記憶系統設計**（DuckDB WASM）
3. **多平台支援架構**

---

## 標籤

#知識儲備 #AIRI #AICompanion #VirtualWaifu #Neuro-sama #VTuber #Minecraft #ElevenLabs #WebGPU

---

*記錄者：總管蘇茉*
*時間：2026-04-09 14:00*
