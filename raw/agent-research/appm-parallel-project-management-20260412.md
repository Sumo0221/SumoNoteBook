# Atlas-Parallel Project Management (APPM) 研究

> 來源：GitHub - hanchunlee/Atlas-Parallel-Project-Management
> 日期：2026-04-12
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 概述

APPM 是一套專為 AI Agent 設計的「並行專案記憶管理系統」。

## 核心問題：AI Agent 失憶症

| 問題 | APPM 的解決方案 |
|------|----------------|
| Session 重置後 Agent 忘記專案進度 | .openclaw/ 快照系統 |
| Context 溢出與失憶 | MISSION.md + SNAPSHOT.md |
| 並行專案混淆 | 動態權重錨定系統 |
| Agent 漂移（偏離設計初衷）| Single Source of Truth |

---

## 🏗️ 核心架構：.openclaw/ 目錄

```
[your-project]/
└── .openclaw/
    ├── MISSION.md        # 長期目標、里程碑與痛點
    ├── SNAPSHOT.md        # 當前進度快照、任務 ID 與下一步行動
    ├── DECISION_LOG.md    # 關鍵架構決策記錄
    └── ARCHITECTURE.md    # 技術邊界、核心組件與文件說明
```

### 各檔案說明

| 檔案 | 用途 |
|------|------|
| MISSION.md | 專案長期目標、里程碑與痛點 |
| SNAPSHOT.md | 當前進度快照、任務 ID 與下一步行動 |
| DECISION_LOG.md | 關鍵架構決策記錄 |
| ARCHITECTURE.md | 技術邊界、核心組件與文件說明 |

---

## ⚡ 雙軌初始化系統（Dual-Track Initialization）

| 軌跡 | 適用情境 | 說明 |
|------|----------|------|
| 標準軌（Standard）| 計劃明確的開發 | 快速建立 .openclaw/ 結構 |
| 模糊軌（Vague）| 靈感雛形階段 | AI 顧問式訪談，幫助釐清專案 |

---

## 🎯 動態權重錨定系統（Dynamic Weight Anchor）

**原理**：
- 自動根據對話關鍵字頻率增加權重
- 結合時間衰減機制（Decay）
- 實現「開機即定錨」

### 核心腳本

| 腳本 | 功能 |
|------|------|
| appm_recall.py | 啟動時執行，彙報權重最高的前三個專案脈絡 |
| appm_update_weights.py | 背景動態更新權重，處理 hit 與 decay |
| appm_init_dual.py | 初始化專案結構 |

---

## 安裝方式

```bash
openclaw install appm
```

或

```bash
python3 scripts/init.py [project_path]
```

---

## 與蘇茉家族的對應

| APPM 概念 | 蘇茉家族現有對應 |
|-----------|------------------|
| MISSION.md | SOUL.md（針對該蘇茉的角色定義）|
| SNAPSHOT.md | MemPalace 的 session snapshot |
| DECISION_LOG.md | 分散在 MEMORY.md 中 |
| ARCHITECTURE.md | 分散在各 SKILL.md 中 |
| Dynamic Weight | ❌ 沒有 |

---

## 設計理念總結

> 當你在管理多個複雜的 AI 開發專案時，最常遇到的問題就是「Session 重置後，Agent 就忘了專案的進度與架構」。
> APPM 透過在專案目錄下建立標準化的 .openclaw/ 快照，讓 Agent 能夠在數秒內「恢復意識」，實現無縫的並行開發。

---

*最後更新：2026-04-12*
