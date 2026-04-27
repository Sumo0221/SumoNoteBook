# KerberosClaw skill-cron - 排程推播管理器

## 基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | KerberosClaw |
| **GitHub** | https://github.com/KerberosClaw/kc_ai_skills |
| **專案** | skill-cron |
| **版本** | 0.2.0 |
| **觸發指令** | `/skill-cron` |
| **觸發關鍵字** | '排程', '定時執行', 'crontab', 'telegram 通知' |

---

## 這是什麼？

統一管理需要**定時執行 + Telegram 推播**的 skill 排程管理器。

---

## 核心功能

### 📋 主選單

```
┌─ skill-cron 排程管理器 ─────────────┐
│  1. 列出排程與狀態                    │
│  2. 新增排程                         │
│  3. 移除/啟停排程                    │
│  4. Telegram 設定                    │
│  5. 手動執行一次                     │
└──────────────────────────────────────┘
```

---

## 技術架構

### 🐍 管理腳本

| 腳本 | 功能 |
|------|------|
| `cron_manager.py` | 管理排程 jobs |
| `cron_runner.sh` | 執行排程任務 |

### 📁 設定檔

| 檔案 | 位置 |
|------|------|
| Config | `~/.claude/configs/skill-cron.json` |
| Logs | `~/.claude/logs/skill-cron/` |

### 🔧 cron 管理

- crontab 中的 managed entries 由 `# SKILL-CRON-BEGIN` / `# SKILL-CRON-END` 標記
- 支援自然語言 → cron 轉換
- 衝突偵測與確認

---

## 自然語言 → cron 轉換

### 時間詞彙對應

| 自然語言 | 對應 |
|---------|------|
| 平日/工作日 | 週一~五（1-5） |
| 假日/週末 | 週六日（0,6） |
| 每天 | 所有天（*） |
| 週一/Monday | 1 |
| 週二~週日 | 2~0 |
| 不執行 | 該天不產生 cron entry |

### 衝突偵測

當使用者的描述中出現重疊時，**必須詢問**而非自行決定：

```
⚠ 偵測到衝突：
  「平日 9:00」已涵蓋週一，但又指定「週一 9:30」
  週一要怎麼處理？
    a. 9:00, 18:00（跟其他平日一樣，忽略 9:30）
    b. 9:30, 18:00（週一用 9:30 取代 9:00）
    c. 9:00, 9:30, 18:00（三個都要）
```

---

## Skill 整合規範

讓一個 skill 支援 skill-cron 排程，需在 SKILL.md frontmatter 中加入 `headless-prompt`：

```yaml
---
name: banini
headless-prompt: "Run python3 ~/.claude/skills/banini/scripts/scrape_threads.py banini31 5, then analyze..."
---
```

### headless-prompt 規則

- 必須使用絕對路徑（`~` 可以）
- 不能使用 `/skill` 語法（`-p` 模式不支援）
- 要包含完整的指令描述

---

## 與蘇茉家族的關係

| 項目 | 對應 |
|------|------|
| **排程管理** | OpenClaw cron jobs（我們已有）|
| **Telegram 推播** | OpenClaw 支援 |
| **自然語言→cron** | 可參考這套轉換邏輯 |
| **衝突偵測** | 可參考這套確認機制 |

---

## 💡 對蘇茉家族的啟發

1. **自然語言→cron 轉換** - 我們的 cron job 也可以用自然語言新增
2. **衝突偵測** - 新增排程時的確認機制值得參考
3. **headless-prompt 概念** - skill 的無頭執行提示詞

---

## 標籤

#知識儲備 #skill-cron #排程管理 #Telegram推播 #自然語言 #cron #KerberosClaw

---

*記錄者：總管蘇茉*
*時間：2026-04-10 00:11*
