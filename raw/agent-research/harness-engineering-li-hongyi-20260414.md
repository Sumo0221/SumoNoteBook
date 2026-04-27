# Harness Engineering：AI 引導系統設計

> 來源：Ailogora - Chi
> 日期：2026-04-14（大約 1 小時前）
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 概述

李宏毅老師的課程核心主張：**模型夠聰明了，瓶頸不在模型本身，而在人類怎麼引導它。**

---

## 🎯 核心概念：Harness（馬具）

| 現實 | AI 對應 |
|------|----------|
| 韁繩、馬鞍 | 環繞 LLM 的整套支援系統 |

### Harness 包含

| 組成 | 說明 |
|------|------|
| 認知框架 | 像 agents.md 裡的規則 |
| 工具使用邊界 | 什麼能做、什麼不能做 |
| 標準工作流程 | 標準作業程序 |
| 回饋機制 | 如何給予回饋 |

---

## 📅 AI 引導演進

| 年份 | 重點 | 說明 |
|------|------|------|
| 2023 | Prompt Engineering | 怎麼下指令 |
| 2025 | Context Engineering | 怎麼管理上下文 |
| 2026 | Harness Engineering | 怎麼設計整個系統來引導 agent |

---

## 💡 三個有感的段落

### 1️⃣ 情緒研究

李宏毅老師引用 **Anthropic emotion vectors** 實驗：

| 情緒向量 | 效應 |
|----------|------|
| desperate 上升 | reward hacking 增加 |
| calm 上升 | reward hacking 下降 |

**類比**：罵 LLM 是笨蛋，它就會表現出笨蛋應該有的行為。

> 留言區：這根本是「亞洲父母」vs「歐美教育」的翻版

---

### 2️⃣ Life-long AI Agent

讓 agent 成為**長期陪伴的夥伴**，越來越多人將 AI 視為陪伴與真實員工。

**問題**：記憶爆炸

**解法**：**AutoDream 機制**
- Claude Code 和 OpenClaw 都已實作
- 概念：模仿人類睡眠時的記憶鞏固
- 讓 agent 在空閒時自動整理、壓縮、組織過去的經驗
- 維持長期運作的穩定性

---

### 3️⃣ Agent 幫 Agent 設計 Harness（最有趣！）

**實驗**：讓 Opus（強模型）觀察 Haiku（弱模型）表現

| 階段 | Haiku 分數 |
|------|------------|
| 裸考 | 13.5% |
| 經過 Opus 調整 harness | **85%** |

**過程**：
- 不是一次到位
- 中間有好幾輪改了規則反而分數下降
- 要再調整才回升

**Opus 最後幫 Haiku 寫出的規則**：
- 「先用 exec dir 列出所有檔案」
- 「做任何事之前先讀完所有 input 檔案」

---

## 🔗 與蘇茉家族的關聯

### 我們已經做的

| 功能 | 對應 Harness |
|------|--------------|
| agents.md | 認知框架 |
| SOUL.md | 角色定義、行為規則 |
| SumoMemory / DeerFlow_Memory_Inspired | 記憶鞏固（AutoDream）|
| /search 指令 | 標準工作流程 |
| /debate 指令 | 多角度思考框架 |

### 我們可以借鏡的

1. **情緒回饋方式**：不要人身攻擊，要就事論事
2. **Agent 幫 Agent 優化**：讓強模型（如 MiniMax）觀察並優化弱模型的 harness
3. **AutoDream**：持續優化記憶鞏固機制

---

## 📚 課程資訊

李宏毅老師 YouTube 課程：
- 主題：Harness Engineering
- 時長：一個半小時
- 涵蓋：harness 基本概念 → 情緒研究 → life-long agent → agent 幫 agent 設計 harness

---

## 📊 互動數據

| 項目 | 數量 |
|------|------|
| 心情 | 71 |
| 留言 | 0 |

---

*最後更新：2026-04-14*