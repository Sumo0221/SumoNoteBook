# Study: agent-skills by Addy Osmani

## 📋 基本資訊

| 項目 | 內容 |
|------|------|
| **名稱** | agent-skills |
| **作者** | Addy Osmani (Google Chrome team) |
| **描述** | Production-grade engineering skills for AI coding agents |
| **GitHub** | https://github.com/addyosmani/agent-skills |
| **Stars** | 7 slash commands + 20 skills |
| **學習日期** | 2026-04-24 |

---

## 🎯 核心理念

> Skills encode the workflows, quality gates, and best practices that senior engineers use when building software.

一套標準化的 AI Agent 開發流程，包含 7 個命令和 20 個技能。

---

## 🔧 7 個 Slash Commands

| Command | 功能 | 核心理念 |
|---------|------|----------|
| /spec | 定義規格 | Spec before code |
| /plan | 規劃任務 | Small, atomic tasks |
| /build | 增量建構 | One slice at a time |
| /test | 測試驗證 | Tests are proof |
| /review | 審查代碼 | Improve code health |
| /code-simplify | 簡化代碼 | Clarity over cleverness |
| /ship | 發布上線 | Faster is safer |

---

## 📦 20 Skills 列表

### 構想與規格
| Skill | 功能 | 使用時機 |
|-------|------|----------|
| idea-refine | 發散/收斂思考將模糊概念轉為具體提案 | 有粗糙概念需要探索時 |
| spec-driven-development | PRD（產品需求文件）涵蓋目標、命令、結構、代碼風格、測試、邊界 | 開始新專案、功能或重大變更時 |

### 規劃與執行
| Skill | 功能 | 使用時機 |
|-------|------|----------|
| planning-and-task-breakdown | 將規格分解為小型、可驗證的任務 | 有規格需要拆解成可執行單元時 |
| incremental-implementation | 薄垂直切片 - 實作、測試、驗證、提交 | 任何涉及多檔案的變更 |

### 測試與品質
| Skill | 功能 | 使用時機 |
|-------|------|----------|
| 	est-driven-development | 紅綠重構、測試金字塔 (80/15/5)、DAMP over DRY | 實作邏輯、修復錯誤、改變行為時 |
| rowser-testing-with-devtools | Chrome DevTools MCP 即時運行數據 | 建構或除錯任何在瀏覽器中運行的東西 |

### 審查與簡化
| Skill | 功能 | 使用時機 |
|-------|------|----------|
| code-review-and-quality | 五軸審查、變更大小(~100行)、嚴重性標籤 | 合併任何變更前 |
| code-simplification | Chesterton's Fence、Rule of 500、降低複雜度 | 代碼可運作但難以閱讀或維護時 |

### 安全與效能
| Skill | 功能 | 使用時機 |
|-------|------|----------|
| security-and-hardening | OWASP Top 10 預防 auth 模式、密鑰管理、依賴審計 | 處理用戶輸入、auth、數據存儲或外部整合時 |
| performance-optimization | Measure-first 方式、Core Web Vitals 目標、分析工作流 | 有效能需求或懷疑有回歸時 |

### 維運與發布
| Skill | 功能 | 使用時機 |
|-------|------|----------|
| git-workflow-and-versioning | Trunk-based development、atomic commits、~100行變更 | 任何程式碼變更（始終）|
| ci-cd-and-automation | Shift Left、Faster is Safer、feature flags、quality gate pipelines | 設定或修改建置和部署管道 |
| deprecation-and-migration | Code-as-liability 思維、compulsory vs advisory deprecation | 移除舊系統、遷移用戶或淘汰功能時 |
| documentation-and-adrs | ADR、API 文件、內聯文檔標準 | 做出架構決策、改變 API 或發布功能時 |
| shipping-and-launch | 發布前檢查清單、feature flag 生命週期、分階段 rollout、rollback 程序 | 準備部署到生產環境時 |

### 設計與上下文
| Skill | 功能 | 使用時機 |
|-------|------|----------|
| context-engineering | 餵給 Agent 正確的資訊 - rules files、context packing、MCP 整合 | 開始 session、切換任務或輸出品質下降時 |
| source-driven-development | 將每個框架決策基於官方文檔 - verify、cite sources、flag unverified | 任何框架或函式庫需要authoritative、source-cited code時 |

### 開發支援
| Skill | 功能 | 使用時機 |
|-------|------|----------|
| debugging-and-error-recovery | 五步 triage：reproduce、localize、reduce、fix、guard | 測試失敗、建置中斷或行為異常時 |
| pi-and-interface-design | Contract-first design、Hyrum's Law、One-Version Rule | 設計 API、模組邊界或公共介面時 |
| rontend-ui-engineering | Component architecture、design systems、state management、WCAG 2.1 AA | 建構或修改使用者介面時 |

---

## 🔄 Development Lifecycle Flow

`
DEFINE → PLAN → BUILD → TEST → REVIEW → SHIP
 Idea   Spec   Code   Debug   QA     Go Live

/skills/planning-and-task-breakdown/skills/spec-driven-development/skills/incremental-implementation/skills/test-driven-development/skills/debugging-and-error-recovery/skills/code-review-and-quality/skills/shipping-and-launch
`

---

## 🎭 專業角色（Personas）

| Agent | 角色 | 觀點 |
|-------|------|------|
| code-reviewer | Senior Staff Engineer | 五軸代碼審查，"would a staff engineer approve this?" 標準 |
| 	est-engineer | QA Specialist | 測試策略、覆蓋率分析、Prove-It 模式 |
| security-auditor | Security Engineer | 漏洞檢測、威脅建模、OWASP 評估 |

---

## 📚 Quick References

| Reference | 內容 |
|-----------|------|
| 	esting-patterns.md | 測試結構、命名、mocking、React/API/E2E 範例 |
| security-checklist.md | Pre-commit checks、auth、input validation、headers、CORS、OWASP Top 10 |
| performance-checklist.md | Core Web Vitals targets、frontend/backend checklists |
| ccessibility-checklist.md | Keyboard nav、screen readers、visual design、ARIA、testing tools |

---

## 💡 Skill Anatomy（每個 Skill 的結構）

`
SKILL.md
├── Frontmatter (name, description, Use when...)
├── Overview → What this skill does
├── When to Use → Triggering conditions
├── Process → Step-by-step workflow
├── Rationalizations → 常見藉口 + 反駁
├── Red Flags → 出問題的跡象
└── Verification → 證據要求
`

---

## 💡 對蘇茉家族的價值

### 與現有 Planner 機制的整合
| agent-skills | 蘇茉家族對應 |
|--------------|-------------|
| planning-and-task-breakdown | Planner 蘇茉核心職責 |
| code-review-and-quality | 品管蘇茉（Critic）|
| security-and-hardening | 駭客蘇茉（Security）|
| 	est-driven-development | 可參考用於品管蘇茉 |

### 建議引用到 Planner
- **垂直切片原則**：不要水平建構，要垂直建構功能路徑
- **任務大小指南**：XS/S/M/L/XL，超過 L 要再分解
- **依賴圖**：識別依賴關係，底層先建

### 建議引用到品管
- **五軸審查**：可讀性、正確性、效能、安全性、可維護性
- **變更大小控制**：~100 行以內
- **Verify 非談判**：每個 skill 結尾都有驗證要求

---

## 🔗 安裝方式（適用於各種 Agent）

| Agent | 安裝方式 |
|-------|----------|
| Claude Code | /plugin marketplace add addyosmani/agent-skills |
| Cursor | Copy SKILL.md to .cursor/rules/ |
| Gemini CLI | gemini skills install https://github.com/addyosmani/agent-skills.git --path skills |
| Windsurf | Add skill contents to Windsurf rules |
| OpenCode | Uses AGENTS.md and skill tool |
| GitHub Copilot | Use agents/ as personas + .github/copilot-instructions.md |

---

## 🌟 關鍵設計原則

1. **Process, not prose** - Skills are workflows agents follow, not reference docs they read
2. **Anti-rationalization** - 每個 skill 有常見藉口表格防止 agent 跳過步驟
3. **Verification is non-negotiable** - 每個 skill 結尾都有明確的證據要求

---
*學習完成時間: 2026-04-24*
*備註：非常適合與 Planner 蘇茉和品管蘇茉的實作結合*
