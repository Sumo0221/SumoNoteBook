# openclaw-docs-skill - OpenClaw 文件技能

## 基本資訊

| 項目 | 內容 |
|------|------|
| **名稱** | openclaw-docs-skill |
| **作者** | tbdavid2019 |
| **GitHub** | https://github.com/tbdavid2019/openclaw-docs-skill |
| **用途** | 讓 AI 助手擁有 OpenClaw 疑難雜症處理能力 |
| **特點** | 自動每日更新文件 |

---

## 這是什麼？

一個全面的 Agent Skill，專為 AI  coding assistants（如 Claude with Antigravity）設計。

安裝後，AI 助手會獲得 OpenClaw 的深度知識，能幫助處理：

| 功能範圍 | 說明 |
|----------|------|
| **安裝和更新** | Install, upgrade, or migrate OpenClaw |
| **設定** | Edit openclaw.json, set up models, manage secrets |
| **頻道管理** | WhatsApp, Telegram, Discord, Slack, iMessage 等 15+ 頻道 |
| **Gateway 操作** | Start, stop, restart, health check, remote access |
| **多代理路由** | 配置多個 agent， isolated workspaces |
| **ACP Agents** | Spawn Codex, Claude Code, Gemini CLI 等 14+ harnesses |
| **瀏覽器自動化** | Multi-profile browser control, Chrome MCP |
| **Plugin 系統** | Capability model, context engine plugins, SDK |
| **自動化** | Cron jobs, standing orders, background tasks |
| **安全強化** | Audit, lock down access, incident response |
| **故障排除** | Diagnose and fix common errors |

---

## 目錄結構

```
openclaw-docs-skill/
├── SKILL.md                    # 主入口（370 行專家工作流程）
├── scripts/
│   └── sync-docs.sh            # 同步引擎 - 拉取官方最新文件
├── .github/workflows/
│   └── auto-sync.yml           # GitHub Action - 每日 04:00 UTC 自動同步
└── references/                 # 400+ Markdown 檔案（知識庫）
    ├── channels/               # 各頻道設定
    ├── tools/                  # 所有內建工具
    ├── plugins/                # Plugin 架構和 SDK
    ├── providers/              # 35+ 模型提供商
    ├── concepts/               # 核心概念
    ├── gateway/                # Gateway 設定
    ├── security/               # 安全強化
    ├── nodes/                  # 節點設定
    ├── automation/             # 自動化
    ├── install/                # 安裝指南
    ├── platforms/             # 平台指南
    └── cli/                    # CLI 參考
```

---

## 安裝方式

```bash
# Clone this repo
git clone https://github.com/tbdavid2019/openclaw-docs-skill.git

# Copy to your skills directory
cp -r openclaw-docs-skill ~/.gemini/antigravity/skills/openclaw
```

---

## 同步機制

| 方式 | 說明 |
|------|------|
| **手動同步** | `sh scripts/sync-docs.sh` |
| **自動同步** | GitHub Action 每日 04:00 UTC |

---

## 與蘇茉家族的關係

| 蘇茉家族現有 | 這個 Skill |
|--------------|-----------|
| 蘇茉文件 | 可以補充更多 OpenClaw 疑難排解知識 |
| skill-vetter | 可以用來審查這個 skill |
| docs.openclaw.ai | 是官方文件來源 |

---

## 標籤

#知識儲備 #OpenClaw #AgentSkill #文件同步 #蘇茉家族

---

*記錄者：總管蘇茉*
*時間：2026-04-08 15:34*
