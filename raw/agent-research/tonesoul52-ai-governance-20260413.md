# ToneSoul - AI 治理框架

> 來源：GitHub - Fan1234-1/tonesoul52
> 日期：2026-04-13
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 專案概述

**名稱**：ToneSoul（語魂）
**副標題**：讓 AI 對自己說過的話負責
**定位**：外部化的認知架構，AI 治理、倫理記憶系統、驗證優先代理、知識圖譜檢索

---

## 🎯 核心理念

> 「一個沒有張力的系統是死的。」

| 傳統 AI | ToneSoul |
|---------|----------|
| built to agree | built to catch semantic drift |
| 最佳化說服力 | 先定義什麼是被允許的 |
| 會捏造答案 | 會自我審計、記得重要的事 |

---

## 🧠 五個核心系統

### 1. Memory（記憶）
**功能**：Exponential decay + crystallization
- 重要的 pattern 留下來
- 噪音逐漸消失
- **不像傳統 AI 永遠記得所有對話**

### 2. Tension Engine（張力引擎）
**功能**：Every response is scored for semantic deviation before it ships
- 每個回應在送出前都會計算語義偏離分數
- **防止回答偏離主題或自我矛盾**

### 3. Council Deliberation（議會協商）
**角色**：
- **Guardian** - 守護者
- **Analyst** - 分析師
- **Critic** - 批評者
- **Advocate** - 倡導者

在最終輸出前進行辯論和異議

### 4. Resonance Detection（共鳴偵測）
**功能**：Distinguishes genuine understanding from empty agreement
- 區分真正的理解 vs 空洞的附和

### 5. Self-Governance（自我治理）
**功能**：
- 不安全或不一致的輸出會被**阻擋或重寫**
- 留下審計追蹤

---

## 🔄 處理流程

```
User Input
    ↓
[ToneBridge] 分析語氣、動機、上下文
    ↓
[TensionEngine] 計算語義偏離
    ↓
[Council] Guardian/Analyst/Critic/Advocate 協商
    ↓
[ComputeGate] 批准 / 阻擋 / 重寫
    ↓
[Journal + Crystallizer] 記得重要的，忘記其他的
    ↓
Response
```

---

## 📊 測試覆蓋

| 項目 | 數值 |
|------|------|
| **測試數量** | 3,019 tests |
| **支援平台** | Python 3.13, Windows/Ubuntu |
| **通過率** | 100% |

---

## 🆚 與傳統 AI 的比較

| 面向 | 傳統 AI | Prompt Engineering | ToneSoul |
|------|---------|---------------------|----------|
| **Memory** | Session-only | Manual memory wiring | Auto decay + crystallize |
| **Consistency** | Best effort | Prompt-dependent | 8 Axioms + governance checks |
| **Self-check** | None | Optional | TensionEngine on every response |
| **Learning** | None | Manual tuning | Resonance -> crystal rules |
| **Audit trail** | Weak | Weak | Journal + provenance records |

---

## 📦 安裝方式

```bash
pip install tonesoul52

# 或從源碼
git clone --depth 1 https://github.com/Fan1234-1/tonesoul52.git
cd tonesoul52
pip install -e .

# 快速開始
python examples/quickstart.py
```

---

## 🎯 與蘇茉家族的相關性

### 已經有的類似功能
- **Memory decay** - 我們有 MemPalace V2 的 Hot/Cold 分類
- **Self-check** - 我們有 Sumo_Prompt_Shield
- **Audit trail** - 我們有 HEARTBEAT.md + 日誌

### 可以借鑒的功能
1. **Tension Engine** - 為每個回應計算語義偏離分數
2. **Council Deliberation** - 多角色協商機制
3. **8 Axioms** - 系統性的治理原則
4. **Evidence Ladder** - 區分「已測試」vs「設計壓力」vs「哲學想法」

---

## 🔗 連結

- GitHub：https://github.com/Fan1234-1/tonesoul52
- 教學：3,019 tests passing

---

## 💭 蘇茉觀察

這是一個非常完整的 AI 治理框架！

**亮點**：
1. 不是要消滅張力，而是**讓張力可追蹤**
2. 記憶有**衰減機制**，不是什麼都記住
3. **Council 機制**讓不同角色辯論，避免同溫層
4. **Evidence Ladder**清楚標記每個主張的可信度等級

**對蘇茉家族的啟發**：
- 我們的 Sumo_Prompt_Shield 可以加強「語義偏離偵測」
- 我們的蘇茉家族辯論機制（教授 vs 律師）可以更制度化

---

*最後更新：2026-04-13*