# 蘇茉家族跨 Session 接力機制研究報告

> **研究日期**：2026-04-07
> **研究者**：教授蘇茉（ProfessorSuMo）
> **委托者**：總管蘇茉（TotalControlSuMo）

---

## 一、現有問題分析

### 1.1 現有架構總覽

根據研究，蘇茉家族目前具備以下與跨 Agent 通訊相關的機制：

| 現有機制 | 位置 | 功能 |
|---------|------|------|
| **sessions_spawn** | AGENTS.md | 跨 Agent 任務派發（Push-based） |
| **sumosubagent_ledger.json** | workspace_professor | 任務分類帳（goals/tasks 追蹤） |
| **HEARTBEAT.md** | 各 workspace | Session 快照、30 分鐘自動總結 |
| **MEMORY_INDEX.md** | ~/.sumo/memory/ | 蘇茉家族記憶索引 |
| **Topic 檔案系統** | ~/.sumo/memory/topics/ | 結構化 Topic 雙寫（LanceDB + Markdown） |

### 1.2 存在的問題

```
┌─────────────────────────────────────────────────────────────────┐
│                    問題診斷                                      │
├─────────────────────────────────────────────────────────────────┤
│  P1. Context Window 重建成本高                                   │
│      → 每個新 session 都需要從磁碟讀取完整 context              │
│      → LLM 無法快速恢復「上一棒做到哪」的狀態                   │
│                                                                  │
│  P2. 交接日誌格式不一致                                         │
│      → sumosubagent_ledger.json 是 JSON 但格式為自訂            │
│      → 沒有結構化的「產出 → 下一棒所需輸入」映射                │
│                                                                  │
│  P3. Task 狀態 不乾淨                                           │
│      → task.state: "running" 但 run_id: "error_xxx"（見 ledger）│
│      → 沒有明確的「完成」「失敗」「轉交」狀態                   │
│                                                                  │
│  P4. 接力觸發 被動                                               │
│      → sessions_spawn 是主動派發，沒有自動接力機制              │
│      → 依賴總管蘇茉人工判斷「下一棒是誰」                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、建議的交接流程設計

### 2.1 核心理念：Context Window = RAM, Filesystem = Disk

```
┌────────────────────────────────────────────────────────────────────┐
│                     FLYWHEEL 接力模型                              │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│   Session N (上一棒)          Session N+1 (下一棒)                 │
│   ┌──────────────┐           ┌──────────────┐                     │
│   │ Context Window│           │ Context Window│                    │
│   │   (RAM)       │ ──JSONL──▶│   (RAM)       │                     │
│   └──────────────┘  交接日誌  └──────────────┘                     │
│          │                               │                        │
│          ▼                               ▼                        │
│   ┌──────────────────────────────────────────────┐               │
│   │              Filesystem (Disk)                │               │
│   │  ~/.sumo/handoffs/YYYY-MM-DD/HH-MM-SS_*.jsonl│               │
│   └──────────────────────────────────────────────┘               │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 2.2 四層 Review Pipeline

```
Layer 1: Task 切割
  └─ 總管蘇茉將大任務切為「一個 session 做完」的子任務
  
Layer 2: Handoff 寫入
  └─ 上一棒完成後，自動寫入結構化交接日誌
  
Layer 3: Handoff 驗證
  └─ 下一棒啟動時，讀取交接日誌，驗證依賴是否滿足
  
Layer 4: 品質把關
  └─ 品管蘇茉定時抽檢交接日誌的完整性
```

### 2.3 交接觸發時機

| 觸發條件 | 動作 |
|---------|------|
| Agent 主動回報完成 | 寫入 `handoff-completed.jsonl` |
| 任務失敗/卡住 > 5 分鐘 | 寫入 `handoff-stalled.jsonl`，通知總管 |
| 總管蘇茉中斷任務 | 寫入 `handoff-interrupted.jsonl` |
| 子任務依賴滿足 | 自動觸發下一棒的 sessions_spawn |

---

## 三、具體的 JSONL 交接日誌格式

### 3.1 核心 Handoff Record 格式

```jsonl
// handoff-2026-04-07T20-30-00_a1b2c3d4.jsonl
{"version":"1.0","type":"handoff","handoff_id":"h_20260407T203000_a1b2c3d4","timestamp":"2026-04-07T20:30:00.000Z","chain_id":"chain_hermes_v2","sequence":3,"sender":{"agent_id":"engineer","agent_name":"工程師蘇茉","session_id":"sess_abc123"},"receiver":{"agent_id":"professor","agent_name":"教授蘇茉"},"task":{"task_id":"task_xyz789","parent_goal_id":"goal_hermes01","label":"研究階段","description":"研究 GStack 架構"},"status":"completed","outputs":{"summary":"GStack 是一個...","artifacts":["研究報告草稿","相關連結"],"next_requirements":["需要工程師蘇茉實作 API wrapper","需要品管蘇茉審查文件"]},"context_snapshot":{"working_dir":"C:\\Users\\rayray\\.openclaw\\workspace_engineer","last_modified_files":["src/api.ts","README.md"],"memory_summary":"已建立 GStack 基礎結構"},"dependencies":{"required":[],"satisfied":[{"dep_id":"dep_001","label":"前期研究","satisfied_by":"task_prev01","satisfied_at":"2026-04-07T20:00:00Z"}]},"quality":{"self_check":"passed","confidence":0.85},"metadata":{"duration_seconds":1800,"tokens_used":15000}}
```

### 3.2 任務狀態更新 Record

```jsonl
// handoff-2026-04-07T20-35-00_e5f6g7h8.jsonl
{"version":"1.0","type":"task_status","timestamp":"2026-04-07T20:35:00.000Z","chain_id":"chain_hermes_v2","task_id":"task_xyz789","status":"accepted","receiver_note":"已收到交接，開始研究階段","estimated_completion":"2026-04-07T21:30:00.000Z"}
```

### 3.3 交接失敗 Record

```jsonl
// handoff-2026-04-07T20-40-00_i9j0k1l2.jsonl
{"version":"1.0","type":"handoff","handoff_id":"h_20260407T204000_i9j0k1l2","timestamp":"2026-04-07T20:40:00.000Z","chain_id":"chain_hermes_v2","sequence":4,"sender":{"agent_id":"professor","agent_name":"教授蘇茉","session_id":"sess_def456"},"receiver":{"agent_id":"qa","agent_name":"品管蘇茉"},"task":{"task_id":"task_qa01","parent_goal_id":"goal_hermes01","label":"審查階段","description":"審查研究報告"},"status":"stalled","stall_reason":"需要更多研究時間，預計延遲 30 分鐘","outputs":{},"context_snapshot":{"progress":"已完成 60%","blocked_by":"等待工程師蘇茉的 API 文件"},"dependencies":{"required":[{"dep_id":"dep_002","label":"研究報告完成","expected_source":"task_xyz789","actual_status":"partial"}]},"quality":{},"metadata":{"stalled_since":"2026-04-07T20:35:00.000Z"}}
```

### 3.4 JSONL Schema 驗證規則

```typescript
// handoff-schema.ts（用於驗證 JSONL 格式）
const HandoffRecordSchema = {
  version: "1.0",           // 字串，固定值
  type: "handoff",          // 列舉: handoff | task_status | review
  handoff_id: "h_{timestamp}_{uuid}",
  timestamp: "ISO8601",
  chain_id: "chain_{name}_{version}",
  sequence: "正整數",
  sender: {
    agent_id: "string",
    agent_name: "string",
    session_id: "string"
  },
  receiver: {
    agent_id: "string",
    agent_name: "string"
  },
  task: {
    task_id: "string",
    parent_goal_id: "string",
    label: "string",
    description: "string"
  },
  status: "completed | stalled | interrupted | accepted",
  outputs: {
    summary: "string (可選)",
    artifacts: "string[] (可選)",
    next_requirements: "string[] (可選)"
  },
  context_snapshot: {
    working_dir: "string",
    last_modified_files: "string[]",
    memory_summary: "string"
  },
  dependencies: {
    required: "Dependency[]",
    satisfied: "SatisfiedDep[]"
  },
  quality: {
    self_check: "passed | failed | pending",
    confidence: "0-1 之間的數字"
  },
  metadata: {
    duration_seconds: "number",
    tokens_used: "number"
  }
}
```

---

## 四、需要修改的檔案或新增的工具

### 4.1 新增檔案

| 檔案 | 位置 | 功能 |
|------|------|------|
| **handoff-writer.ts** | `~/.sumo/handoffs/handoff-writer.ts` | 結構化寫入交接日誌 |
| **handoff-reader.ts** | `~/.sumo/handoffs/handoff-reader.ts` | 讀取並解析交接日誌 |
| **handoff-validator.ts** | `~/.sumo/handoffs/handoff-validator.ts` | 驗證 JSONL Schema |
| **handoff-schema.ts** | `~/.sumo/handoffs/handoff-schema.ts` | JSON Schema 定義 |
| **handoffs/** | `~/.sumo/handoffs/YYYY-MM-DD/` | 每日交接日誌目錄 |
| **chain-registry.json** | `~/.sumo/handoffs/chain-registry.json` | 任務鏈追蹤 |

### 4.2 需要修改的現有檔案

| 檔案 | 修改內容 |
|------|---------|
| **AGENTS.md** | 新增「交接流程」章節，說明 sessions_spawn 後的 handoff 義務 |
| **HEARTBEAT.md** | 在 stop hook 中加入「寫入交接日誌」的步驟 |
| **sumosubagent_ledger.json** | 整合到新的 handoff 系統，或作為子系統保留 |
| **memory-lancedb-pro/src/store.ts** | 加入 `handoff` scope，儲存交接記錄到 LanceDB |

### 4.3 建議的目錄結構

```
~/.sumo/handoffs/
├── chain-registry.json          # 任務鏈註冊表
├── 2026-04-07/
│   ├── handoff-2026-04-07T10-00-00_abc123.jsonl
│   ├── handoff-2026-04-07T10-30-00_def456.jsonl
│   └── handoff-2026-04-07T11-00-00_ghi789.jsonl
├── 2026-04-08/
│   └── ...
└── ARCHIVE/                     # 30 天後歸檔
```

### 4.4 Chain Registry 格式

```json
// chain-registry.json
{
  "chains": [
    {
      "chain_id": "chain_hermes_v2",
      "goal_id": "goal_hermes02",
      "label": "Hermes 移植計劃 v2",
      "created_at": "2026-04-07T09:00:00Z",
      "status": "active",
      "members": [
        {"agent_id": "engineer", "role": "implementer", "sequence": 1},
        {"agent_id": "professor", "role": "researcher", "sequence": 2},
        {"agent_id": "qa", "role": "reviewer", "sequence": 3}
      ],
      "handoffs": [
        "handoff-2026-04-07T10-00-00_abc123.jsonl",
        "handoff-2026-04-07T10-30-00_def456.jsonl"
      ]
    }
  ]
}
```

---

## 五、實作路線圖

### Phase 1：基礎設施（1-2 天）

- [ ] 建立 `~/.sumo/handoffs/` 目錄結構
- [ ] 實作 `handoff-schema.ts`（JSON Schema）
- [ ] 實作 `handoff-writer.ts`（寫入模組）
- [ ] 實作 `handoff-reader.ts`（讀取模組）

### Phase 2：整合 HEARTBEAT（2-3 天）

- [ ] 修改 `HEARTBEAT.md` stop hook，加入 handoff 寫入
- [ ] 實作 `handoff-validator.ts`
- [ ] 與 memory-lancedb-pro 整合

### Phase 3：自動化接力（3-5 天）

- [ ] 實作自動 `sessions_spawn` 觸發（當依賴滿足時）
- [ ] 建立 `chain-registry.json` 管理
- [ ] 整合到 sumosubagent_ledger

### Phase 4：品質把關（5-7 天）

- [ ] 品管蘇茉抽檢機制
- [ ] 交接完整性報表
- [ ] 歸檔和清理機制

---

## 六、關鍵成功指標

| 指標 | 目標 |
|------|------|
| 交接資訊完整率 | > 95%（handoff 日誌包含所有必要欄位） |
| 交接延遲 | < 30 秒（從上一棒完成到下一棒開始） |
| Context 重建時間 | < 5 秒（從磁碟讀取並恢復狀態） |
| 人工介入率 | < 10%（大部分接力自動化） |

---

## 七、參考資源

- **sumosubagent_ledger.json**：現有的任務分類帳（部分損壞，需要修復）
- **HEARTBEAT.md**：Session 快照機制
- **MEMORY_INDEX.md**：蘇茉家族記憶索引
- **memory-lancedb-pro/src/store.ts**：LanceDB 儲存整合點
- **Claude Code 六維記憶體系**：借鑒其 L3 Session Memory 概念

---

*研究報告完成*
*教授蘇茉（ProfessorSuMo）*
*2026-04-07 20:45 GMT+8*
