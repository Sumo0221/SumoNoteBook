# Harness Engineering 研究：從 MCP 到 Skills 到 CLI

> 來源：胡嘉璽 Facebook 貼文，Generative AI 技術交流中心
> 日期：2026-04-12
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 核心觀點

### 1. Context Window 是 LLM 最珍貴的資產
- 管理 Context Window 是一門大學問
- MCP 的痛點：一次就要載入整個工具的說明和內容
- Agent Skills 使用「漸進式載入」(Progressive Disclosure)

### 2. CLI 的優勢
- 使用本地 CPU，便宜又快速
- 輸出是純文字標準輸出，不會有幻覺
- LLM 獲得執行結果後，能更精準判斷下一步

### 3. 三者正確的使用原則
| 工具 | 適用情境 |
|------|----------|
| MCP Server | 著重安全及可靠性，優先使用官方版本 |
| Agent Skill | 缺乏現成工具的專屬情境，或是內部工具 |
| CLI | 底層與基本操作，如 gh, docker, ffmpeg 等 |

---

## 對蘇茉家族的啟示

### 我們領先的地方
1. Progressive Disclosure - 已有 SKILL.md 漸進式載入
2. CLI First - mempalace_hook.py 是純 CLI
3. CLAUDE.md/AGENTS.md 調校 - 已有 AGENTS.md、SOUL.md、USER.md

### 可以改進的地方
1. Skill Metadata - 應該在 SKILL.md 頂部加 metadata: 區塊
2. CLI 發現機制 - 統一注册到 CLI Registry
3. 確定性 vs 推理 - 記憶系統可標注「確定」vs「推測」

---

## 作者的核心理念 vs 蘇茉家族

| 作者 | 蘇茉家族 |
|------|----------|
| Context Window 最珍貴 | HEARTBEAT.md 控制資訊流 |
| Token Efficiency | token_optimize.py |
| CLI > MCP | 我們偏愛 CLI |
| CLAUDE.md 調校 | AGENTS.md 已經存在 |

---

## 立即可做的改進

### 1. 更新 SKILL.md 模板
加入 metadata: 區塊（描述、作者、版本）

### 2. 建立 CLI Registry
統一管理所有 CLI 工具

### 3. 區分記憶類型
標注「事實」vs「推測」

---

*最後更新：2026-04-12*
