# Claude Code 跨專案 Session 搜尋技巧

## 基本資訊

| 項目 | 內容 |
|------|------|
| **標題** | Claude Code 技巧：跨專案 Session 搜尋，0.1 秒找到任何對話 |
| **來源** | https://codotx.com/news/2026-04-01-claude-code-cross-project-session-search/ |
| **用途** | 在多個專案的 Claude Code 對話紀錄中快速搜尋 |
| **速度** | 0.1 秒掃完 766MB、38 個專案 |

---

## 問題的起點

工程師同時維護多個專案，跨專案使用經驗時需要「主動整理文件」當橋樑，但有以下問題：

| 問題 | 說明 |
|------|------|
| **需要主動整理** | 忘了整理等於沒做過 |
| **丟失脈絡** | 整理出來的文件是靜態摘要，失去來回推敲和決策脈絡 |
| **管理負擔** | 跨專案一多，中繼文件變成負擔 |

---

## Claude Code 的資料結構

| 目錄 | 說明 |
|------|------|
| `~/.claude/sessions/` | 存放活躍 session 的 JSON 元資料（session 結束後消失）|
| `~/.claude/projects/` | 每個專案的對話紀錄（JSONL 檔案，以 session UUID 命名）|

### Session 名稱存在哪裡？

Session 名稱存在 JSONL 中，格式如：
```json
{
  "type": "system",
  "subtype": "local_command", 
  "content": "Session renamed to: my-session",
  "sessionId": "39029d88-...",
  "cwd": "/Users/user/SideProjects/codotx",
  "timestamp": "2026-03-30T04:40:27.526Z"
}
```

---

## 核心搜尋指令

```bash
rg --no-filename 'Session renamed to:' ~/.claude/projects/ \
| jq -r '[.sessionId, .cwd, (.content | capture("Session renamed to: (?<name>.+)</local") | .name), .timestamp] | @tsv' \
| sort -t$'\t' -k4 -r \
| awk -F'\t' '!seen[$1]++'
```

這條指令做了四件事：
1. ripgrep 掃描所有 JSONL，找到包含 "Session renamed to:" 的行
2. jq 從 JSON 中擷取 session ID、專案路徑、名稱和時間戳
3. sort 按時間倒序排列
4. awk 去除重複（同一個 session 可能被 rename 多次，只取最新的名稱）

**766MB 的資料，0.1 秒跑完！**

---

## 包裝成 Shell 腳本

```bash
# 建立腳本目錄（首次使用才需要）
mkdir -p ~/.claude/scripts

# 列出所有命名 session
~/.claude/scripts/find-session.sh

# 用關鍵字搜尋
~/.claude/scripts/find-session.sh "deploy"

# 只列某個專案的 session
~/.claude/scripts/find-session.sh -p codotx

# 組合使用：在某個專案中搜 api 相關的 session
~/.claude/scripts/find-session.sh -p codotx api

# 查看特定 session 的詳細資訊
~/.claude/scripts/find-session.sh -i update-ga-env
```

詳細資訊模式會顯示：
```
Session: update-ga-env
ID: 5fb6323d-8330-4c36-8579-0d5376f24957
專案: /Users/user/SideProjects/codotx
時間: 2026-03-30T04:23:58.179Z
Resume: claude --resume "update-ga-env"
JSONL: ~/.claude/projects/-Users-user-SideProjects-codotx/5fb...jsonl
大小: 980K (419 行)
```

---

## 與蘇茉家族的關係

| 蘇茉家族方案 | Claude Code 這個技巧 |
|--------------|---------------------|
| **SumoNoteBook** | 跨對話的知識庫 |
| **MemPalace** | 向量搜尋記憶 |
| **Handoff System** | 跨 Session 接力 |

**核心理念**：都是為了解決「跨對話、跨專案的知識重用」問題

| 方案 | 差異 |
|------|------|
| Claude Code 技巧 | 純文字搜尋，輕量 |
| 蘇茉家族方案 | 向量索引 + Wiki 結構，功能更豐富 |

---

## 從「整理文件」到「直接搜尋」

**以前**：
1. 在 A 專案整理一份文件
2. 切換到 B 專案
3. 把文件路徑貼給 Claude Code
4. 等它讀完再繼續

**現在**：
1. 在 B 專案說「幫我找之前 A 專案裡處理 XX 的 session」
2. Claude Code 自動呼叫腳本搜尋
3. 直接 resume 繼續

---

## 決策

| 日期 | 決定 |
|------|------|
| 2026-04-08 | 記錄為知識儲備，借鑒其核心理念 |

---

## 標籤

#知識儲備 #Claude_Code #跨專案搜尋 #Session管理 #經驗傳承

---

*記錄者：總管蘇茉*
*時間：2026-04-08 10:06*
