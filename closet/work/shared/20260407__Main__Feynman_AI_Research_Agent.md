# Feynman - AI 研究代理

> 日期：2026-04-07
> 來源：https://github.com/getcompanion-ai/feynman
> 標籤：#research #agent #paper-review #知識儲備

---

## 🎯 這是什麼？

Feynman 是一個**開源 AI 研究代理**，用於自動化學術研究流程。

官網：https://feynman.is
License：MIT

---

## 🔧 核心功能

| 命令 | 功能 |
|------|------|
| `/deepresearch <topic>` | 多代理研究調查 |
| `/lit <topic>` | 文獻回顧（搜論文+主要來源）|
| `/review <artifact>` | 模擬同儕審查 |
| `/audit <item>` | 論文 vs 程式碼比對審計 |
| `/replicate <paper>` | 複製實驗到本地/雲端 GPU |
| `/compare <topic>` | 來源比較矩陣 |
| `/draft <topic>` | 生成論文草稿 |
| `/autoresearch <idea>` | 自主實驗循环 |
| `/watch <topic>` | 循環研究監控 |

---

## 🧠 四個內建研究代理

| 代理 | 職責 |
|------|------|
| **Researcher** | 收集證據（論文、網站、代碼庫、文件）|
| **Reviewer** | 模擬同儕審查（帶嚴重性分級回饋）|
| **Writer** | 從研究筆記生成結構化草稿 |
| **Verifier** | 內聯引用、URL 驗證、死連結清理 |

---

## 🔗 整合能力

| 工具 | 說明 |
|------|------|
| Docker | 隔離容器執行安全實驗 |
| Modal | 無伺服器 GPU 計算 |
| RunPod | 持久 GPU pods（SSH 存取）|
| AlphaXiv | 論文搜尋、問答、代碼閱讀、註釋 |

---

## 💾 安裝方式

```bash
# macOS / Linux
curl -fsSL https://feynman.is/install | bash

# Windows (PowerShell)
irm https://feynman.is/install.ps1 | iex
```

---

## 💡 對 SumoNoteBook 的參考價值

### 可以學習的地方

1. **多代理協作模式** - Researcher/Reviewer/Writer/Verifier 分工
2. **文獻回顧自動化** - 搜尋論文、總結共識、發現開放問題
3. **引用驗證機制** - 每一個聲稱都有 URL 對應
4. **模擬同儕審查** - 自動產出審查意見和修訂計畫

### 未來可能應用

- Sunny 讀大學時做研究論文
- 蘇茉家族文獻整理
- 知識庫事實查核

---

## 📝 備註

這是**知識儲備**，不是立即要做的專案。