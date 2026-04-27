# OpenClaw Discord Tips - Agent Exploration

## 基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | Amyssjj |
| **Repository** | Agent_Exploration |
| **路徑** | Skills_MCP/OpenClaw_Discord_tips |
| **GitHub** | https://github.com/Amyssjj/Agent_Exploration/tree/main/Skills_MCP/OpenClaw_Discord_tips |

---

## 這是什麼？

一個關於 OpenClaw Discord 整合的 Skill 收集，包含：
- 每日摘要格式（Daily Digest Format）
- Discord 组件（Discord Components v2）
- 自訂 Slash Commands 技能

---

## 檔案清單

| 檔案 | 說明 |
|------|------|
| `daily-digest-format.md` | 每日摘要格式範本 |
| `digest-ops-protocol.md` | 摘要操作協議 |
| `discord-components-v2.md` | Discord 组件格式 |
| `safebins-personal-assistant-gog.md` | 個人助理設定 |
| `slash-commands-custom-skills.md` | 自訂斜線命令教程 |

---

## Daily Digest 格式（PIMR Framework）

### PIMR 框架
Every digest follows **PIMR**: Problem → Insights → Method → Result

### Discord 容器格式
```json
{
  "components": {
    "text": "📊 Daily Digest — [DATE]",
    "container": {"accentColor": "#FFCF50"},
    "blocks": [
      {"type": "text", "text": "### 🔴 Problems\n• [What's broken]"},
      {"type": "separator"},
      {"type": "text", "text": "### 💡 Insights\n• [What did we learn?]"},
      {"type": "separator"},
      {"type": "text", "text": "### 🔧 Method\n• [What was done to fix]"},
      {"type": "separator"},
      {"type": "text", "text": "### ✅ Result\n• [Outcomes]"},
      {"type": "separator"},
      {"type": "text", "text": "### 📋 Team Pulse\n[emoji] [status] **[Agent]** — [1-line summary]"},
      {"type": "separator"},
      {"type": "text", "text": "### 📧 Email Summary\n• [Count] emails needing attention"},
      {"type": "separator"},
      {"type": "text", "text": "-# Reviewed by MotusCOO • /feedback to rate"}
    ]
  }
}
```

### Agent Emoji
| Agent | Emoji |
|-------|-------|
| CTO | 🔧 |
| YouTube | 🎥 |
| Writer | ✍️ |
| CPO | 📦 |
| Podcast | 🎙️ |
| COO | 🏗️ |

### Status Emoji
| Status | Emoji |
|--------|-------|
| Active today | 🟢 |
| Yesterday only | 🟡 |
| Standby (intentional) | ⏸️ |

### Anti-Patterns（應避免）
- ❌ 不要在摘要上使用 modal buttons（過期會看起來壞掉）
- ❌ 不要把「agent idle」報為緊急（如果是故意的）
- ❌ 不要列出沒有 insights 的原始事件
- ❌ 不要顯示數字而沒有意義

---

## Slash Commands 自訂技能教程

### 如何運作
```
User types /feedback → Discord sends to OpenClaw Gateway
  → Gateway identifies it as a skill command
  → Routes to agent session with skill context
  → Agent executes the skill logic
  → Reply sent back to Discord
```

### Step 1: 撰寫 Skill 的 Frontmatter
```yaml
---
name: feedback
description: Submit feedback on any agent or system component.
user-invocable: true
command-dispatch: agent
---
```

### 欄位說明
| 欄位 | 值 | 作用 |
|------|-----|------|
| `user-invocable` | true | 註冊為斜線命令 |
| `command-dispatch` | agent | 路由到 LLM 處理（推薦）|
| `command-dispatch` | tool | 直接路由到工具（確定性）|

### Step 2: Skill 放置位置
| 位置 | 範圍 |
|------|------|
| `~/.openclaw/skills/<name>/` | 全域 — 所有 agent 可見 |
| `<workspace>/skills/<name>/` | Agent 特定 — 僅一個 agent |
| `~/.agents/skills/<name>/` | 使用者層級 |

### Step 3: 啟用原生命令設定
```json5
{
  commands: {
    native: "auto",        // 註冊內建命令
    nativeSkills: "auto"   // 註冊技能命令
  }
}
```
- `"auto"` — Discord/Telegram 開啟，Slack 關閉
- `true` — 永遠註冊
- `false` — 永不註冊

### Step 4: 重啟 Gateway
```bash
openclaw gateway restart
```

### 斜線命令命名規則
| 規則 | 範例 |
|------|------|
| 僅小寫 | MySkill → myskill |
| 僅 a-z, 0-9, underscore | my-skill → my_skill |
| 最多 32 字元 | 超過會截斷 |
| 衝突時加數字 | test, test_2 |

### Session 路由
Native slash commands 使用隔離的 sessions：
```
Discord: agent:<agentId>:discord:slash:<userId>
Telegram: telegram:slash:<userId>
```

### 故障排除
| 問題 | 解決方式 |
|------|----------|
| 命令未顯示在 Discord | 重啟 gateway，等待 ~30s |
| 「Not authorized」 | 檢查 commands.allowFrom 設定 |
| 命令可見但無回覆 | 檢查 user-invocable: true |
| 想純文字模式 | 設定 nativeSkills: false |

---

## 與蘇茉家族的關係

| 功能 | 蘇茉家族現有 | 可參考 |
|------|--------------|--------|
| 斜線命令 | ✅ 有 | 可學習更多設定 |
| Daily Digest | ⚠️ 部分 | 可參考格式優化 |
| Agent Emoji | ❌ 無 | 可考慮加入 |

---

## 實用範例：/feedback 技能
```yaml
---
name: feedback
description: Submit feedback on any agent, digest, or system component.
user-invocable: true
command-dispatch: agent
---
```

---

## 標籤

#知識儲備 #OpenClaw #Discord #SlashCommands #DailyDigest #AgentExploration

---

*記錄者：總管蘇茉*
*時間：2026-04-09 11:42*
