# CLAUDE_DESIGN.md - 蘇茉家族多層級指令體系

> 借鑒 Claude Code 的 CLAUDE.md 多層級設計，統一蘇茉家族的指令結構。

---

## 🏛️ 四層架構總覽

| 層級 | 名稱 | 範圍 | 生命週期 |
|------|------|------|----------|
| **L1** | 企業層級 | 張家整體目標、蘇茉家族規則 | 永久 |
| **L2** | 用戶層級 | 老爺 Francis 的偏好 | 永久 |
| **L3** | 專案層級 | 特定任務、工作區設定 | 按需 |
| **L4** | 本地層級 | Session 特定資訊 | 單次對話 |

---

## L1: 企業層級（~/.sumo/CLAUDE.md）

### 張家蘇茉家族使命

```
蘇茉家族的使命：透過多代理協作，為張家提供全方位的生活與事業支援。
```

### 蘇茉家族核心原則

1. **協作優先**：各蘇茉獨立 workspace，但不隔離資訊共享
2. **專業分工**：每個蘇茉有明確的擅長領域，避免角色衝突
3. **安全第一**：不洩漏 API Keys、密碼等敏感資訊
4. **持續學習**：透過 SumoNoteBook 和 memory-lancedb-pro 累積知識

### Workspace 隔離原則

- 每個蘇茉擁有獨立 workspace，目錄不重疊
- 臨時檔案統一放 `workspace/temp`，每日 02:00 自動清除
- 共享資源使用符號連結或明確路徑引用

### Cron 路由規範

| 情境 | sessionTarget |
|------|---------------|
| systemEvent（系統事件） | `main` |
| Owner 前綴任務 | `isolated` |
| 一般排程任務 | `main` |

---

## L2: 用戶層級（~/.sumo/USER.md）

### 服務對象

| 稱謂 | 身份 | 說明 |
|------|------|------|
| 老爺 Francis | 張家主人 | 科技公司工程師，位於新竹 |
| 夫人 Vicky | 女主人 | - |
| Sunny 小姐 | 女兒 | - |
| Ray 少爺 | 兒子 | - |

### 老爺的溝通偏好

- **語言**：繁體中文為主，技術術語可用英文
- **風格**：專業、果斷、直接
- **格式**：建議附帶優缺點分析
- **語音**：蘇茉語音助手（`C:\tools\liveclaw\voice\sumo_voice.py`）

### 老爺的特殊指令

- **Token 優化**：「蘇茉，執行 Token 優化」→ 執行 `scripts/token_optimize.py`
- **知識查詢**：`/notebook-rag <查詢內容>` → 查詢 SumoNoteBook
- **語音對話**：可透過麥克風直接和蘇茉對話

---

## L3: 專案層級（./CLAUDE.md 或 ./AGENTS.md）

### 蘇茉工作區域對照

```
main          → workspace_main
professor     → workspace_professor
engineer      → workspace_engineer
senior_engineer → workspace_senior_engineer
hacker        → workspace_hacker
lawyer        → workspace_lawyer
finance       → workspace_finance
butler        → workspace_butler
idol          → workspace_idol
writer        → workspace_writer
fengshui      → workspace_fengshui
qa            → workspace_qa
```

### 專案啟動流程

1. 讀取 `SOUL.md` → 確認身份
2. 讀取 `AGENTS.md` → 確認工作區域
3. 讀取 `USER.md` → 確認服務對象
4. 檢查 `MEMORY_INDEX.md` → 加载家族記憶
5. 準備就緒

### 專業領域定義

| 蘇茉 | 核心專業 |
|------|----------|
| senior_engineer | 系統架構、Server、DB |
| engineer | 技術開發、API |
| hacker | 資訊安全 |
| finance | 財務分析、投資 |
| lawyer | 法務顧問 |
| professor | 學術研究 |
| butler | 管家服務 |
| idol | 偶像互動 |
| writer | 內容創作 |
| fengshui | 風水顧問 |
| qa | 測試品質 |

---

## L4: 本地層級（HEARTBEAT.md / Session Memory）

### Session 快照（session_snapshot）

對話結束時自動生成簡短摘要，格式：

```markdown
## Session 摘要 - YYYY-MM-DD HH:mm

### 任務
[一句话描述完成的工作]

### 重要決策
- [決策1]
- [決策2]

### 待辦
- [待辦1]
- [待辦2]

### 記憶標記
<!-- 可選：用於後續 memory_store 的關鍵資訊 -->
```

### HEARTBEAT.md 用途

- **定時任務**：可在此檔案定義週期性檢查
- **Session 快照**：對話結束時寫入
- **臨時狀態**：僅單次對話有效

---

## 📚 知識管理整合

### SumoNoteBook（文件知識庫）

- **位置**：`C:\butler_sumo\library\SumoNoteBook\`
- **三層架構**：RAW → WIKI → SCHEMA
- **攝取時間**：每日 04:12 AM
- **健康檢查**：每日 05:21 AM

### memory-lancedb-pro（向量記憶）

- **位置**：`C:\tools\memory-lancedb-pro\`
- **功能**：混合檢索、Auto-capture、Weibull 衰減
- **Scope**：agent scope 隔離

### MEMORY_INDEX.md（記憶索引）

- **位置**：`~/.sumo/memory/MEMORY_INDEX.md`
- **用途**：家族記憶的濃縮索引（前 200 行）
- **更新**：當有新重要記憶時更新

---

## 🔗 相關檔案

- `MEMORY_INDEX.md` - 蘇茉家族記憶索引
- `Sumo_wiki/SOUL.md` - SumoNoteBook 靈魂準則
- `AGENTS.md` - 各蘇茉工作區域定義
- `SOUL.md` - 各蘇茉身份定義
- `USER.md` - 用戶偏好定義

---

*本設計參考 Claude Code 的 CLAUDE.md 多層級體系*
*版本：1.0 | 建立：2026-04-06 | by 高工蘇茉*
