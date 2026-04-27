# 蘇茉家族記憶工程指南

**建立日期**：2026-03-31  
**靈感來源**：多 Agent 系統記憶工程文章  
**目的**：避免多 Agent 系統「一起失憶」

---

## 為什麼記憶工程比模型更重要？

多 Agent 系統最容易被低估的不是模型，而是**記憶**。

如果沒有記憶工程，agent 很快就會從「看起來有分工」變成「一起失憶」。

---

## 八層記憶系統

### 第一層：群組隔離

**原則**：每個群組的 Agent 只讀自己那條線的記憶，不隨便碰別的群組資料。

好處：
- 避免工作線互相污染
- A 群的資料不會跑到 B 群
- Agent 不會混線

**蘇茉家族應用**：
```
張家財金群組 (-5053318694) → 財金蘇茉
我們這一家 (-5200937586) → 管家蘇茉
風水輪流轉 (-5220828504) → 術士蘇茉
...
```

---

### 第二層：規則層（AGENTS.md）

每個 Agent 都有自己的 **AGENTS.md**，內容包括：
- 它是誰
- 做什麼、不做什麼
- 服務哪個群組
- 遇到什麼情況要回報總管
- 能不能跨線、能不能直接找其他 Agent

**蘇茉家族應用**：
- `workspace/AGENTS.md` — 總管蘇茉規則
- `workspace_professor/AGENTS.md` — 教授蘇茉規則
- `workspace_finance/AGENTS.md` — 財金蘇茉規則
- ...

---

### 第三層：長期記憶索引（MEMORY.md）

MEMORY.md **不是倉庫，而是索引**。

它的作用是告訴 Agent：
- 哪些事情值得長期記
- 重點是什麼
- 真正內容在哪裡

**結構**：
```markdown
# 蘇茉長期記憶

## 重點領域
- 張家成員資料 → memory/family_members.md
- 股票系統 → memory/trading_system.md
- 法律研究 → memory/law_study_car_accident.md

## 最近重點
- [2026-03-30] lossless-claw 升級為增強版

## 重要規則
- API Keys 絕對不能外流
- 只有老爺可以執行愛可樂 FB
```

---

### 第四層：真正的內容（memory/ 子目錄）

真正的內容應該拆到 `memory/` 子目錄裡：

```
memory/
├── YYYY-MM-DD.md          # 每日日誌
├── family_members.md      # 張家成員資料
├── law_study/            # 法律研究（按主題）
│   ├── car_accident.md
│   ├── contracts.md
│   └── ...
├── corrections/          # 錯誤與修正
│   └── 2026-03-errors.md
├── self_improving/       # 自我改進
│   └── lessons_learned.md
├── projects/            # 專案
│   ├── trading_system/
│   └── sumo_family/
└── decisions/           # 重要決策
    └── 2026-03-decisions.md
```

好處：
- 記憶不會單一檔案一路膨脹
- 可以按需載入，不用每次都塞全部歷史

---

### 第五層：記憶提煉

**不是每一句聊天都值得留**。

真正應該沉澱下來的只有：
- ✅ 明確結論
- ✅ 重要數字
- ✅ 固定規則、流程變更
- ✅ 踩過的坑

**提煉方式**：
```markdown
# 記憶提煉格式

## 結論
[明確的結論或決定]

## 數據
[重要的數字或統計]

## 規則
[新的規則或流程]

## 教訓
[犯過的錯誤及如何避免]
```

---

### 第六層：錯誤與教訓（corrections / self-improving）

這類內容**不要混在一般 memory**，而是額外放進：
- `memory/corrections/` — 犯過的錯誤
- `memory/self_improving/` — 自我改進

**目的不是留存歷史，而是避免重犯**。

如果錯誤沒有沉澱成規則，Agent 很可能下次換個 Session 又再犯。

---

### 第七層：總管提煉

手下 Agent 各自記自己的細節，但**總管還需要一份高層組織記憶**。

總管記的是：
- 誰負責什麼
- 最近哪條工作線有新規則
- 哪個 Agent 最近踩過什麼坑
- 哪些教訓應該升級成軍團級規則

```markdown
# 組織記憶（總管專用）

## 分工表
- 財金蘇茉：股票、總經分析
- 律師蘇茉：法律諮詢
- 教授蘇茉：技術研究

## 最近動態
- [2026-03-30] 完成五大系統整合
- [2026-03-31] 研究吳恩達 Agentic AI 課程

## 待關注問題
- 教授蘇茉 sessions_spawn 有配對問題
- 每日總經晨報有超時問題
```

---

### 第八層：備份

記憶系統一旦開始有用，**就不能只存在當前上下文**。

**備份項目**：
- `AGENTS.md` — 工作規則
- `SOUL.md` — 靈魂設定
- `USER.md` — 用戶資料
- `MEMORY.md` — 長期記憶索引
- `memory/` — 所有子目錄
- 相關 scripts
- 必要 config

**備份工具**：`C:\butler_sumo\Tools\sumou_backup.py`

---

## 蘇茉家族當前記憶結構

```
C:\Users\rayray\.openclaw\workspace\
├── AGENTS.md           ✅ 工作規則
├── SOUL.md            ✅ 靈魂設定
├── USER.md            ✅ 用戶資料
├── MEMORY.md          ✅ 長期記憶索引
├── TOOLS.md           ✅ 工具配置
├── HEARTBEAT.md      ✅ 心跳配置
└── memory/
    ├── YYYY-MM-DD.md  ✅ 每日日誌
    ├── professor_research/  ✅ 研究筆記
    ├── law_study_notes.md   ✅ 法律筆記
    ├── development_log.md    ✅ 開發日誌
    └── ...
```

---

## 總結

| 層次 | 檔案/目錄 | 作用 |
|------|-----------|------|
| 1 | 群組隔離 | 各 Agent 只讀自己群組資料 |
| 2 | AGENTS.md | 工作規則、邊界定義 |
| 3 | MEMORY.md | 索引，不是倉庫 |
| 4 | memory/ 子目錄 | 真正內容，按需載入 |
| 5 | 記憶提煉 | 只留結論、數據、規則、教訓 |
| 6 | corrections/ | 錯誤沉澱，避免重犯 |
| 7 | 總管組織記憶 | 高層視角，組織邏輯 |
| 8 | 備份 | 全域 workspace 備份 |

---

## 核心原則

> **聊天只是入口，真正讓系統不失憶的，是背後這整套：群組隔離、分層記錄、持續提煉、錯誤沉澱與全域備份。**

---

*蘇茉家族記憶工程持續更新中...*
