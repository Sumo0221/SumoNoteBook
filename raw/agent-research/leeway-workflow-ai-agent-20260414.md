# Leeway - YAML 工作流驅動的 AI Agent 框架

> 來源：GitHub - hardness1020/Leeway
> 日期：2026-04-14
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 概述

**標題**：A workflow-driven AI agent framework that executes YAML-defined decision trees.

**核心理念**：「Human-defined workflows. AI-powered execution.」

用 YAML 定義決策樹，結合 Scheduling、Hooks、MCP 和 21 個內建工具。

---

## 🎯 Leeway vs OpenClaw vs AutoGPT

| 項目 | AutoGPT / OpenClaw | Leeway |
|------|-------------------|--------|
| **驅動方式** | LLM 決定一切 | YAML 定義圖結構，LLM 決定節點內部 |
| **流程控制** | 不可重複、不可審計 | 每個節點按相同順序執行 |
| **節點定義** | 整體一個流程 | 每個節點是完整 Agent Loop |

---

## 🔧 核心特色

### 1. 每個節點都是完整 Agent Loop
- 模型可以呼叫 read_file、grep、bash
- 迭代直到 max_turns
- 發出 workflow_signal 表示完成

### 2. 每節點獨立範圍（Per-node scoping）
- 每個節點有自己的 ToolRegistry、SkillRegistry、HookRegistry、MCP
- 從全域和節點允許清單合併
- 節點 A 可以只有 bash + glob
- 節點 B 可以只有 web_fetch + mcp_github_search

### 3. 漸進式技能載入（Progressive skill loading）
- skill(name="code-review") 返回 SKILL.md + 檔案索引
- 參考檔案只在 LLM 明確要求時才載入
- 節點只看到允許的技能和技能頂層內容

### 4. Turn 預算 + 緊急注入
- 引擎告訴 LLM 剩餘 turn 數
- 剩下 2 turn 時注入緊急提醒
- 列出要呼叫的準確信號
- 防止 LLM 無聲消耗所有 turn

### 5. 自動緊縮（Auto-compaction）
- 上下文填滿時，先清除陳舊的 tool-result bodies
- 不夠時，用 LLM 總結較早的訊息，保留最後 6 條
- 完全透明，無需手動 /compact

---

## 📊 架構圖

```
User Prompt → CLI / React TUI
    ↓
RuntimeBundle
    ↓
QueryEngine
    ↓
Anthropic / OpenAI API
    ↓
Tool Registry (21+ tools)
    ↓
Permissions + Hooks
    ↓
Files | Shell | Web | MCP | Tasks | Cron
```

---

## 📋 工作流模式

### 1. 線性（無條件轉換）
```yaml
scan:
  prompt: "Scan the project structure."
  tools: [glob, bash]
  edges:
    - target: assess
      when: { always: true }
```

### 2. 分支（基於信號的分支）
```yaml
assess:
  prompt: "Signal 'well_documented' or 'needs_investigation'."
  edges:
    - target: deep_dive
      when: { signal: needs_investigation }
    - target: summarize
      when: { signal: well_documented }
```

### 3. 循環（回到自己或更早節點）
```yaml
deep_dive:
  prompt: "Signal 'dig_deeper' to loop, 'enough' to move on."
  edges:
    - target: deep_dive
      when: { signal: dig_deeper }
    - target: summarize
      when: { signal: enough }
```

### 4. 並列（條件並發分支）
```yaml
review:
  parallel:
    branches:
      quality:
        when: { always: true }
        prompt: "Review code quality"
        tools: [grep, glob]
      security:
        when: { signal: security_risk }
        prompt: "Security audit"
        requires_approval: true
      tests:
        when: { signal: has_tests }
        prompt: "Run tests"
```

---

## 🛠️ 21+ 內建工具

| 類別 | 工具 |
|------|------|
| **File I/O** | bash, read_file, write_file, edit_file, glob, grep |
| **Web** | web_fetch, web_search |
| **互動** | ask_user_question, skill |
| **任務** | task_create, task_list, task_get, task_stop |
| **排程** | cron_create, cron_list, cron_delete, cron_toggle |
| **Agent** | agent, remote_trigger |
| **記憶** | memory_read, memory_write |
| **MCP** | mcp_<server>_<tool> (動態) |

---

## 💡 對蘇茉家族的啟發

### 1. YAML 工作流定義
- 可以用 YAML 定義蘇茉的工作流程
- 每個節點是一個完整 Agent Loop
- 工作流可重複、可審計

### 2. 節點範圍隔離
- 不同節點有不同工具權限
- 安全性更高
- 符合最小權限原則

### 3. 漸進式技能載入
- SKILL.md 主指令先載入
- 詳細參考檔案按需載入
- 大幅節省 token

### 4. 自動緊縮
- 不需要手動 /compact
- 工作流執行中自動管理上下文
- 更流暢的長任務執行

---

## 🔗 連結

- GitHub：https://github.com/hardness1020/Leeway

---

*最後更新：2026-04-14*