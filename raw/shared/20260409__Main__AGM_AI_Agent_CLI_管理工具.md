# AGM - AI Coding Agent CLI 中央管理工具

## 基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | superYngo |
| **GitHub** | https://github.com/superyngo/agm |
| **類型** | Rust CLI 工具 |
| **用途** | 集中管理多個 AI 程式碼 Agent CLI 工具 |

---

## 這是什麼？

一個用 Rust 寫的 CLI 工具，可以**集中管理**所有 AI 程式碼 Agent CLI 工具的設定、技能、和代理。

> Centralized management of AI coding agent CLI tools (Claude Code, Gemini CLI, Copilot CLI, Codex CLI, Pi, Crush, OpenCode, etc.)

---

## 支援的工具

| 工具 | 路徑 |
|------|------|
| Claude Code | ~/.claude |
| Codex CLI | ~/.codex |
| Copilot CLI | ~/.copilot |
| Crush | ~/.config/crush |
| Gemini CLI | ~/.gemini |
| OpenCode | ~/.config/opencode |
| Pi | ~/.pi/agent |

---

## 核心功能

### 1. Centralized Configuration（集中設定）
- 統一管理所有 AI CLI 工具的 prompts、skills、agents、configs
- 不必到處找設定檔

### 2. Symlink Management（符號連結管理）
- 自動建立和維護連結
- Unix: symlinks
- Windows: junctions + hardlinks

### 3. Skills & Agents Management（技能和代理管理）
- 從本地路徑或 git repo 安裝技能
- 支援自動更新

### 4. Interactive TUI（互動式介面）
- 用 ratatui 做的終端機 UI
- 瀏覽、搜尋、開關技能/代理

### 5. Registry-Driven（登錄驅動）
- 在 TOML 設定檔編輯就可以新增工具
- **不需要改 code！**

### 6. Status Monitoring（狀態監控）
- 一眼看出連結健康狀態
- 工具安裝狀態

---

## 安裝方式

### Linux/macOS
```bash
tar -xzf agm-*.tar.gz
chmod +x agm
mv agm ~/.local/bin/
```

### Windows
```powershell
Expand-Archive agm-windows-*.zip -DestinationPath .
Move-Item agm.exe "$env:USERPROFILE\.local\bin\"
```

### 從原始碼編譯
```bash
git clone https://github.com/superyngo/agm.git
cd agm
cargo build --release
cp target/release/agm ~/.local/bin/
```

### 一鍵安裝
```bash
curl -fsSL https://gist.githubusercontent.com/superyngo/a6b786af38b8b4c2ce15a70ae5387bd7/raw/gpinstall.sh | APP_NAME="agm" REPO="YOUR_USERNAME/agm" bash
```

---

## 常用指令

| 指令 | 說明 |
|------|------|
| `agm init` | 初始化設定和中央目錄 |
| `agm tool --status` | 顯示所有工具的連結狀態 |
| `agm tool --link` | 為所有已安裝工具建立連結 |
| `agm tool` | 開啟工具管理 TUI |
| `agm source -a <URL>` | 從 git repo 新增來源 |
| `agm source` | 開啟技能/代理管理 TUI |
| `agm source -u` | 更新所有來源 repos |

---

## 設定檔位置

```
~/.config/agm/config.toml
```

### 預設中央目錄
| 類型 | 路徑 |
|------|------|
| Prompts | ~/.local/share/agm/prompts/MASTER.md |
| Skills | ~/.local/share/agm/skills/ |
| Agents | ~/.local/share/agm/agents/ |
| Source repos | ~/.local/share/agm/source/ |

---

## 與蘇茉家族的關係

### 可參考的功能

| AGM 功能 | 蘇茉家族對應 |
|----------|--------------|
| 中央化管理 | SumoNoteBook 知識庫 |
| 符號連結管理 | 我們也有多個 workspace |
| Skills & Agents | 各蘇茉的 skill |
| Interactive TUI | 命令列介面 |
| Status Monitoring | health_check_v3.py |

### 可能可借鑒的點

1. **Registry-Driven 設計**：在 TOML 設定檔編輯就可以新增工具，不用改 code
2. **互動式 TUI**：用 ratatui 做終端機 UI，操作直覺
3. **中央化管理**：所有設定集中在一個地方

---

## 結論

 AGM 是一個**專門管理 AI Coding Agents** 的工具，蘇茉家族可以研究它的架構來優化我們的多 Agent 管理系統。特別是：
- 如何集中管理多個 Agent 的設定
- 如何用 TUI 讓操作更直覺
- Registry-Driven 的設計概念

---

## 標籤

#知識儲備 #AGM #AI Coding Agent #Rust CLI #中央化管理 #Claude Code #Codex

---

*記錄者：總管蘇茉*
*時間：2026-04-09 12:09*
