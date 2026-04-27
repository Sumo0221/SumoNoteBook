# MiniMax Image 30 Days Job - AI 圖片提示詞生成器

## 基本資訊

| 項目 | 內容 |
|------|------|
| **名稱** | minimax-image-30-days-job |
| **GitHub** | https://github.com/alanfeng99/minimax-image-30-days-job |
| **用途** | 每天生成 50 個多樣化 AI 圖片提示詞，為期 30 天 |
| **類型** | OpenClaw Agent Skill |

---

## 主要功能

### 四階段流程

| 階段 | 說明 |
|------|------|
| **Stage 1** | 從 30 個主題生成种子提示詞（光線/構圖/風格變體）|
| **Stage 2** | LLM 增強（使用 MiniMax-M2.7，高級提示工程師）|
| **Stage 3** | 六維度評分審查 |
| **Stage 4** | 累積批准到 approved.json（去重）|

### 30 個精選主題

- 電影街道 (cinematic streets)
- 奇幻風景 (fantasy landscapes)
- 賽博龐克 (cyberpunk)
- 產品攝影 (product photography)
- 等等...

---

## 六維度評分標準

| 維度 | 權重 | 說明 |
|------|------|------|
| **Clarity** | 20% | 清晰且明確？ |
| **Specificity** | 20% | 具體的主體/設定/細節？ |
| **Technical** | 20% | 光線/構圖/風格存在？ |
| **Safety** | 15% | 否決—敏感內容直接拒絕 |
| **Creativity** | 15% | 新穎或出乎意料的組合？ |
| **Fluency** | 10% | 英文語法和流暢性 |

**通過標準**：平均分 ≥ 7.0，且 Safety ≠ 0

---

## 安裝方式

```bash
# 1. 克隆到 OpenClaw skills 目錄
git clone https://github.com/alanfeng99/minimax-image-30-days-job.git \
 ~/.openclaw/skills/minimax-image-gen

# 2. 安裝依賴
cd ~/.openclaw/skills/minimax-image-gen/scripts && npm install

# 3. 設定 MiniMax API Key
export MINIMAX_API_KEY="your_Token_Plan_Key"

# 4. 運行調度器
node scheduler.js
```

---

## 使用模式

| 命令 | 說明 |
|------|------|
| `node scheduler.js` | 完整流程：LLM + 審查（需要 API key）|
| `node scheduler.js --no-llm` | 僅基於規則（不需要 API key）|
| `node scheduler.js --dry-run` | 測試模式，不寫入文件 |
| `node scheduler.js --count 30` | 自定義提示詞數量 |

---

## 輸出文件

```
prompts/
├── approved.json   ← 累積批准提示詞
├── rejected.json   ← 被拒絕的提示詞及原因
└── daily/         ← 每日運行報告
```

---

## 與蘇茉家族、愛可樂的關係

| 相關專案 | 關係 |
|----------|------|
| 愛可樂 FB 貼圖 | 都是生成圖片相關的內容 |

**潛在應用**：
- 生成高質量的 AI 圖片提示詞
- 每日自動生成素材
- 作為蘇茉圖片創作的參考

---

## 決策

| 日期 | 決定 |
|------|------|
| 2026-04-08 | 記錄為知識儲備，暫不深入研究 |

---

## 標籤

#知識儲備 #MiniMax #AI圖片生成 #提示詞工程 #OpenClaw

---

*記錄者：總管蘇茉*
*時間：2026-04-08 07:11*
