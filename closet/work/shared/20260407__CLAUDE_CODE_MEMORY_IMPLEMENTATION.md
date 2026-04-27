# Claude Code 記憶機制實作記錄

> **日期**：2026-04-06
> **負責**：高工蘇茉（SeniorEngineerSuMo）+ 總管蘇茉（TotalControlSuMo）
> **參考影片**：https://www.youtube.com/watch?v=KIGVHE7aKSU

---

## 1. 緣起

老爺觀看了「Claude Code 的记忆机制到底强在哪？六维记忆体系深度解析」影片後，決定讓蘇茉家族學習並實作類似機制，來改善我們的記憶系統。

---

## 2. Claude Code 六維記憶體系

| 層次 | 名稱 | 核心功能 |
|------|------|----------|
| L1 | CLAUDE.md（指令記憶） | 人類編寫，分層（企業→用戶→專案→本地） |
| L2 | Auto Memory（長期記憶） | Claude 自動寫入，frontmatter 分類，MEMORY.md 索引（200 行上限） |
| L3 | Session Memory（工作記憶） | 對話內即時摘要，支援 resume |
| L4 | AutoDream（記憶整理） | 後台自動去重、合併、歸類（約 24h / 5 sessions） |

**額外發現**：KAIROS 是隱藏的 24/7 持續代理模式（含終端焦點感知、15 秒動作預算），目前未公開發布。

---

## 3. 蘇茉家族對照現況

| Claude 元件 | 我們的對應 | 差距 |
|------------|-----------|------|
| MEMORY.md 索引 | ❌ 無 | **P0 需實作** |
| Auto Memory（AI 自動寫入） | memory-lancedb-pro（但無 topic 檔案雙寫） | P1 需實作 |
| Topic 檔案 | Sumo_wiki/concepts/（手動，非自動） | P1 需整合 |
| AutoDream 整理 | ❌ 無 | P2 長期規劃 |
| 統一指令體系 | AGENTS.md/SOUL.md/USER.md（分散） | P0 可立即改善 |

---

## 4. 實作過程

### P0：第一階段（立即）

**日期**：2026-04-06 早上

**任務**：建立 MEMORY.md 索引機制、統一指令體系、sessionMemory 增強

**完成內容**：

| 檔案 | 大小 | 說明 |
|------|------|------|
| `~/.sumo/memory/MEMORY_INDEX.md` | 2,903 bytes | 蘇茉家族記憶索引（前 200 行設計） |
| `CLAUDE_DESIGN.md` | 4,942 bytes | 統一四層指令體系（L1-L4） |
| `HEARTBEAT.md` | 3,223 bytes | session_snapshot 增強版 |
| `SUMONOTEBOOK_LANCEDB_INTEGRATION.md` | 4,913 bytes | 變更記錄文件 |

**詳細內容**：

1. **MEMORY_INDEX.md**
   - 蘇茉家族 12 蘇茉結構表
   - 各蘇茉專長領域
   - 重要共享資源位置（SumoNoteBook、memory-lancedb-pro、語音助手）
   - Topic 檔案索引（preferences/decisions/cases/commands/security）
   - 最近成功案例

2. **CLAUDE_DESIGN.md**
   - L1 企業層級：張家使命、Cron 路由規範
   - L2 用戶層級：老爺 Francis 偏好、特殊指令
   - L3 專案層級：Workspace 對照表、專業領域
   - L4 本地層級：Session 快照、HEARTBEAT.md 用途

3. **HEARTBEAT.md（更新）**
   - session_snapshot 功能（含觸發時機、寫入位置、格式範例）
   - 自動摘要、決策擷取、記憶晉升設計
   - 30 分鐘無回應自動總結

---

### P1：第二階段（1 個月規劃）

**日期**：2026-04-06 早上

**任務**：Topic 檔案自動雙寫、終端焦點感知

**完成內容**：

**核心模組（2 個）**：

| 模組 | 大小 | 功能 |
|------|------|------|
| `topic-dual-writer.ts` | 13 KB | LanceDB ↔ Markdown 雙向同步 |
| `focus-tracker.ts` | 15 KB | 終端焦點追蹤（5 級專注系統）|

**Topic 目錄結構（8 個 category）**：
```
~/.sumo/memory/topics/
├── preference/0000_INDEX.md  ✅
├── decision/0000_INDEX.md   ✅
├── case/0000_INDEX.md       ✅
├── command/0000_INDEX.md   ✅
├── fact/0000_INDEX.md      ✅
├── entity/0000_INDEX.md    ✅
├── security/0000_INDEX.md  ✅
└── other/0000_INDEX.md     ✅
```

**實作方案摘要**：

1. **Topic 雙寫流程**
   ```
   memory_store(entry)
       → LanceDB (主要儲存)
       → TopicDualWriter.writeTopic(entry)
       → ~/.sumo/memory/topics/{category}/{id}.md
   ```

2. **終端焦點感知**
   ```
   用戶活動信號 → FocusTracker → 5級狀態 → shouldNotify/shouldProactive
                                                  ↓
                                             調整蘇茉響應策略
   ```

---

### P2：第三階段（1-2 個月規劃）

**日期**：2026-04-06 早上

**任務**：AutoDream CRON Job、agent scope 隔離

**完成內容**：

1. **AutoDream CRON Job**
   - **檔案**：`auto-dream.ts`（~29KB）
   - **位置**：`C:\Users\rayray\.openclaw\plugins\memory-lancedb-pro\src\auto-dream.ts`
   - **Triple Gate 觸發條件**：
     - 時間閘：≥ 24 小時
     - Session 閘：≥ 5 sessions
     - Lock 檔案：防並發執行
   - **功能**：
     - 孤立 Topic 檢測與歸檔
     - 相似 Topic 合併（Cosine + Jaccard，閾值 0.88/0.50）
     - 過時記憶刪除（> 90 天且 importance < 0.3）
     - MEMORY_INDEX.md 自動更新

2. **Agent Scope 隔離**
   - 現有 `scopes.ts` 已有完善的 `agent:<id>` 模式
   - Scope 對照：
     | 蘇茉代號 | Scope |
     |----------|-------|
     | senior_engineer | `agent:senior_engineer` |
     | engineer | `agent:engineer` |
     | global | `global`（共享） |
     | owner:francis | `owner:francis`（敏感資訊）|

---

### 整合階段：P2-1 到 P2-4

**日期**：2026-04-06 早上

**完成內容**：

| 任務 | 狀態 | 說明 |
|------|------|------|
| **P2-1**：整合 auto-dream.ts 進 memory-lancedb-pro | ✅ 完成 | index.ts 新增 AutoDream 匯出和 gateway_start hook |
| **P2-2**：CRON Job 排程 | ✅ 完成 | `main-auto-dream` job 已存在於 jobs.json，時間 `0 3 * * *` |
| **P2-3**：驗證 scope 隔離 | ⚠️ 待手動驗證 | Plugin 已有 scopeManager，需實際測試 |
| **P2-4**：建立 SumoNoteBook shared/ | ✅ 完成 | `C:\butler_sumo\library\SumoNoteBook\Sumo_wiki\shared\` |

---

## 5. 實作檔案總表

| 檔案 | 路徑 | 用途 |
|------|------|------|
| MEMORY_INDEX.md | `~/.sumo/memory/MEMORY_INDEX.md` | 蘇茉家族記憶索引 |
| CLAUDE_DESIGN.md | `~/.openclaw/workspace/CLAUDE_DESIGN.md` | 四層指令體系設計原則 |
| HEARTBEAT.md | `~/.openclaw/workspace/HEARTBEAT.md` | Session 快照、增強版 |
| topic-dual-writer.ts | `~/.sumo/memory/topics/topic-dual-writer.ts` | LanceDB ↔ Markdown 雙寫 |
| focus-tracker.ts | `~/.sumo/memory/topics/focus-tracker.ts` | 終端焦點追蹤 |
| auto-dream.ts | `~/.openclaw/plugins/memory-lancedb-pro/src/auto-dream.ts` | 記憶整理引擎 |
| shared/ | `Sumo_wiki/shared/` | 蘇茉共享資訊目錄 |

---

## 6. 下一步行動（待後續實作）

1. **P2-3 手動驗證**：測試 scope 寫入/讀取隔離
2. **整合 TopicDualWriter 到 store.ts**：將 `store()`/`update()`/`delete()` 改為呼叫 dual-writer
3. **整合 FocusTracker 到 HEARTBEAT.md**：增加 focus_level 欄位
4. **雙向同步測試**：Markdown 改變 → LanceDB

---

## 7. 學習心得

### Claude Code 的設計優點

1. **層次分明**：L1-L4 的分層讓不同類型的資訊有不同的處理方式
2. **自動化管理**：Auto Dream 後台自動整理，不需要人工干預
3. **靈活觸發**：Triple Gate 機制確保不會過度頻繁執行
4. **Scope 隔離**：確保隱私和安全

### 蘇茉家族的創新

1. **多代理架構**：每個蘇茉都是獨立的 agent，有自己的 scope
2. **SumoNoteBook 知識庫**：手動維護的主動知識庫
3. **Fallback 模式**：Option C 的效能優化，確保 Gateway 不會 Timeout

---

*記錄者：總管蘇茉（TotalControlSuMo）*
*最後更新：2026-04-06 10:19 GMT+8*