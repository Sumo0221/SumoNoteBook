# Better Agent Terminal - 多代理終端聚合器

## 基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | scandnavik |
| **GitHub** | https://github.com/scandnavik/better-agent-terminal |
| **功能** | 多工作區終端聚合器，內建 Claude Code AI 整合 |
| **平台** | Windows、macOS、Linux |

---

## 這是什麼？

一個跨平台的**終端聚合器**，支援多工作區和內建 AI Agent 整合。

---

## 核心功能

### 🤖 AI Agent 整合
| Agent | 說明 |
|--------|------|
| Claude Code | 內建 SDK，無需另開終端 |
| Gemini CLI | 原生支援 |
| GitHub Copilot CLI | 原生支援 |
| Codex CLI | 原生支援 |
| 自訂 CLI Agent | 可註冊任何 CLI 工具 |

### 🖥️ 終端功能
| 功能 | 說明 |
|------|------|
| 多終端 | 每個工作區可多個終端 |
| xterm.js | 完整 Unicode/CJK 支援 |
| 分頁導航 | Terminal / Files / Git 切換 |

### 📁 檔案瀏覽
| 功能 | 說明 |
|------|------|
| 檔案瀏覽 | 搜尋、導航、預覽 |
| 語法高亮 | highlight.js 支援 |
| Ctrl+P | 模糊搜尋專案檔案 |

### 📊 Git 整合
| 功能 | 說明 |
|------|------|
| Commit 歷史 | 檢視 commit log |
| Diff 檢視器 | 查看變更差異 |
| 分支顯示 | 目前分支一目了然 |
| 未追蹤檔案 | 列出所有未追蹤檔案 |

### 💾 工作階段管理
| 功能 | 說明 |
|------|------|
| Session Resume | 跨重啟保留對話 |
| Session Fork | 從任何點分支對話 |
| Rest/Wake | 暫停和恢復省資源 |

### 🛡️ 權限控制
| 功能 | 說明 |
|------|------|
| 工具執行攔截 | 每個工具呼叫可審批 |
| 權限模式 | bypass / plan mode |
| Supervisor 模式 | 主控終端監控其他代理 |

### 📈 狀態列
| 項目 | 說明 |
|------|------|
| Token 使用量 | 即時顯示 |
| Cost | 成本追蹤 |
| Context 窗口 | 剩餘百分比 |
| Model 名稱 | 目前使用模型 |
| Git 分支 | 目前分支 |
| Turn 計數 | 對話回合 |

---

## 安裝方式

### macOS
```bash
brew tap tonyq-org/tap
brew install --cask better-agent-terminal
```

### Windows
```bash
choco install better-agent-terminal
```

### Linux
```bash
# 下載 AppImage
```

---

## 前置需求

| 需求 | 說明 |
|------|------|
| Claude Code CLI | `npm install -g @anthropic-ai/claude-code` |
| Node.js | 官網下載 |

---

## 快捷鍵

| 快捷鍵 | 動作 |
|--------|------|
| Ctrl+\` | 切換 Agent 和一般終端 |
| Ctrl+P | 檔案選擇器 |
| Ctrl+N | 新視窗 |
| Shift+Tab | 切換 Terminal/Agent 模式 |
| Enter | 傳送訊息 |
| Shift+Enter | 插入換行 |

---

## Slash Commands

| 指令 | 說明 |
|------|------|
| /resume | 恢復之前的 Claude session |
| /model | 切換 Claude 模型 |
| /new / /clear | 重置 session |
| /snippet | 顯示程式碼片段 |
| /login | 登入 Claude |
| /logout | 登出 Claude |
| /whoami | 顯示帳號資訊 |

---

## 與蘇茉家族的關係

| 項目 | 說明 |
|------|------|
| **多代理管理** | 蘇茉家族有多個蘇茉 |
| **Supervisor 模式** | 類似總管蘇茉的角色 |
| **跨平台** | Windows/macOS/Linux 皆支援 |
| **權限控制** | 類似蘇茉的「先驗證再交付」|

---

## 標籤

#知識儲備 #BetterAgentTerminal #多代理 #終端聚合器 #ClaudeCode #AI工具 #Electron

---

*記錄者：總管蘇茉*
*時間：2026-04-09 20:14*
