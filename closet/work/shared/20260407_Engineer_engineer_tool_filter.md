# 工具過濾機制

## 📋 文件資訊
- **版本：** 1.0
- **建立日期：** 2026-04-03
- **目的：** 建立 Sub-agent 安全工具清單，限制危險操作

---

## 🎯 目的

限制 Sub-agent 可使用的工具範圍，增強系統安全性，防止誤操作導致系統損害或資料外洩。

---

## 🔐 工具分類

### 分類說明

| 分類 | 說明 | 風險等級 |
|------|------|---------|
| 🔵 **SAFE** | 安全工具，Sub-agent 可自由使用 | 低 |
| 🟡 **LIMITED** | 有限制地使用，需確認參數 | 中 |
| 🔴 **DANGEROUS** | 危險工具，僅主代理可使用 | 高 |
| 🚫 **BLOCKED** | 完全禁止，無法使用 | 極高 |

---

## 📋 工具白名單

### 🔵 SAFE - Sub-agent 可自由使用

| 工具名稱 | 說明 | 限制 |
|---------|------|------|
| `read` | 讀取檔案內容 | 僅限工作區目錄 |
| `write` | 寫入檔案 | 僅限工作區目錄，禁止覆蓋系統檔案 |
| `edit` | 編輯檔案 | 僅限工作區目錄 |
| `exec` | 執行命令 | 僅限安全命令清單（見附錄） |
| `web_fetch` | 取得網頁內容 | 僅 GET 請求 |
| `search` | 網路搜尋 | 僅 SearXNG |
| `search_news` | 新聞搜尋 | - |
| `quick_answer` | 快速問答 | - |
| `image` | 圖片分析 | - |
| `pdf` | PDF 分析 | - |
| `tts` | 文字轉語音 | - |

### 🟡 LIMITED - 需額外驗證

| 工具名稱 | 說明 | 驗證要求 |
|---------|------|---------|
| `process` | 管理程序 | 需確認目標程序安全性 |
| `sessions_yield` | 結束工作階段 | - |
| `message` | 發送訊息 | 需確認目標是內部成員 |
| `canvas` | 控制畫布 | 需確認非外部系統 |

### 🔴 DANGEROUS - 僅主代理可使用

| 工具名稱 | 說明 | 原因 |
|---------|------|------|
| `browser` | 控制瀏覽器 | 可執行任意 JavaScript |
| `memory_store` | 寫入長期記憶 | 可能影響系統行為 |
| `memory_update` | 更新記憶 | 可能影響系統行為 |
| `memory_forget` | 刪除記憶 | 可能導致資料丟失 |
| `mini_coding_agent` | 啟動子代理 | 避免代理風暴 |
| `sessions_spawn` | 派發子任務 | 避免過度資源消耗 |

### 🚫 BLOCKED - 完全禁止

| 工具名稱 | 說明 | 原因 |
|---------|------|------|
| `exec` + `rm` | 刪除檔案命令 | 資料無法恢復 |
| `exec` + `sudo` | 系統管理员权限 | 風險過高 |
| `exec` + `dd` | 磁碟操作 | 可能損壞系統 |
| `exec` + `mkfs` | 格式化 | 資料永久損失 |
| `exec` + `:(){ :|:& };:` | Fork 炸彈 | 系統資源耗盡 |
| `exec` + `curl` + 外部 URL | 下載執行腳本 | 可能的遠端代碼執行 |

---

## 🛡️ 安全命令白名單（exec 限制）

Sub-agent 使用 `exec` 工具時，僅允許以下命令：

### ✅ 允許的命令

```
# 檔案操作
ls, dir, pwd, cd, mkdir, rmdir, cp, copy, mv, move
cat, type, head, tail, wc, grep, find, which

# 程式執行
python, python3, node, npm, pip, git
echo, printf, date, time

# 網路工具（唯讀）
ping, nslookup, curl (僅 GET, 禁止 -o/-F/-d)
wget (僅下載, 禁止 --execute)

# 系統資訊
uname, hostname, whoami, ps, tasklist
df, du, free, top

# 文字處理
sed, awk, sort, uniq, cut, tr
```

### ❌ 禁止的命令

```
# 刪除操作
rm, del, rmdir, unlink

# 系統修改
chmod, chown, chgrp, passwd, useradd, userdel
mount, umount, fdisk, mkfs, parted

# 網路修改
iptables, ip, ifconfig, route, netstat
iptables -F, ip link set down

# 危險工具
dd, shred, wipe, wipefs
nc, netcat, ncat, socat
telnet, ftp, rsh, rlogin

# 任何涉及 root/sudo 的命令
sudo, su, doas

# 下載並執行
curl | sh, wget -O- | bash
```

---

## 🔧 工具過濾器實作

```python
import re
from typing import List, Set, Optional
from enum import Enum

class ToolCategory(Enum):
    SAFE = "safe"
    LIMITED = "limited"
    DANGEROUS = "dangerous"
    BLOCKED = "blocked"

class ToolFilter:
    """工具過濾器 - 限制 Sub-agent 可使用的工具"""
    
    def __init__(self):
        # 允許的工具清單
        self.allowed_tools: Set[str] = {
            "read", "write", "edit", "exec", "web_fetch",
            "search", "search_news", "quick_answer",
            "image", "pdf", "tts",
            "process", "sessions_yield"
        }
        
        # 危險命令黑名單
        self.dangerous_commands: Set[str] = {
            "rm", "del", "rmdir", "unlink",
            "sudo", "su", "doas",
            "dd", "shred", "wipe", "mkfs",
            "nc", "netcat", "telnet", "ftp",
            "iptables", "ip", "ifconfig",
            ":(){ :|:& };:",  # fork bomb
        }
        
        # exec 命令白名單
        self.allowed_commands: Set[str] = {
            "ls", "dir", "pwd", "cd", "mkdir", "cp", "copy", 
            "mv", "move", "cat", "type", "head", "tail",
            "wc", "grep", "find", "which", "python", "python3",
            "node", "npm", "pip", "git", "echo", "printf",
            "date", "time", "ping", "nslookup", "curl", "wget",
            "uname", "hostname", "whoami", "ps", "tasklist",
            "df", "du", "free", "sed", "awk", "sort", "uniq"
        }
        
        # DANGEROUS 和 BLOCKED 工具
        self.restricted_tools: Set[str] = {
            "browser", "memory_store", "memory_update", 
            "memory_forget", "mini_coding_agent", "sessions_spawn"
        }
    
    def is_tool_allowed(self, tool_name: str) -> bool:
        """檢查工具是否允許使用"""
        return tool_name in self.allowed_tools
    
    def is_command_safe(self, command: str) -> bool:
        """檢查命令是否安全（用於 exec 工具）"""
        command_lower = command.lower()
        
        # 檢查是否包含危險命令
        for dangerous in self.dangerous_commands:
            if dangerous in command_lower.split():
                return False
        
        # 檢查是否為管道命令組合
        if "|" in command:
            parts = command.split("|")
            for part in parts:
                cmd = part.strip().split()[0] if part.strip() else ""
                if cmd and cmd not in self.allowed_commands:
                    return False
        
        # 檢查第一個命令
        first_cmd = command_lower.split()[0] if command_lower.split() else ""
        return first_cmd in self.allowed_commands
    
    def filter_tools(self, requested_tools: List[str]) -> dict:
        """
        過濾工具清單，返回允許和拒絕的工具
        
        返回格式:
        {
            "allowed": ["read", "write", ...],
            "rejected": ["browser", ...],
            "reasons": {"browser": "危险工具，仅主代理可使用"}
        }
        """
        allowed = []
        rejected = {}
        
        for tool in requested_tools:
            if self.is_tool_allowed(tool):
                allowed.append(tool)
            else:
                rejected[tool] = "非白名單工具" if tool not in self.restricted_tools else "危險工具，僅主代理可使用"
        
        return {
            "allowed": allowed,
            "rejected": rejected
        }
```

---

## 🔍 參數驗證

除了工具過濾，還需驗證參數安全性：

```python
class ParameterValidator:
    """參數驗證器"""
    
    # 路徑限制：僅允許工作區目錄
    ALLOWED_PATH_PREFIXES = [
        "C:\\Users\\rayray\\.openclaw\\workspace_engineer",
        "C:\\Users\\rayray\\.openclaw\\workspace_main",
        "memory\\",
        ".\\"
    ]
    
    # URL 限制：僅允許特定網域
    ALLOWED_URL_PATTERNS = [
        r"^https?://searxng\.",  # SearXNG 搜尋
        r"^https?://(www\.)?github\.com/",  # GitHub
        r"^https?://api\.",  # API 端點
    ]
    
    def validate_path(self, path: str) -> bool:
        """驗證檔案路徑是否安全"""
        import os
        abs_path = os.path.abspath(path)
        
        for prefix in self.ALLOWED_PATH_PREFIXES:
            if abs_path.startswith(os.path.abspath(prefix)):
                return True
        return False
    
    def validate_url(self, url: str) -> bool:
        """驗證 URL 是否安全"""
        import re
        for pattern in self.ALLOWED_URL_PATTERNS:
            if re.match(pattern, url):
                return True
        return False
    
    def sanitize_command(self, command: str) -> str:
        """清理危險命令"""
        dangerous = [";", "&&", "||", "`", "$(", ">", "<", "|"]
        sanitized = command
        for d in dangerous:
            # 保留管道，但移除其他 shell 操作符
            if d != "|":
                sanitized = sanitized.replace(d, "")
        return sanitized.strip()
```

---

## 📊 風險矩陣

| 工具/命令 | 風險類型 | 影響程度 | 發生機率 | 風險等級 |
|----------|---------|---------|---------|---------|
| `rm -rf /` | 資料損失 | 嚴重 | 低 | 🟡 中 |
| `sudo rm` | 權限提升 | 嚴重 | 低 | 🟡 中 |
| 外部 curl\|sh | 遠端代碼執行 | 極嚴重 | 中 | 🔴 高 |
| Fork 炸彈 | 系統當機 | 嚴重 | 低 | 🔴 高 |
| `browser` 控制 | 任意操作 | 嚴重 | 中 | 🔴 高 |
| 寫入記憶體 | 系統行為改變 | 中 | 低 | 🟡 中 |

---

## 📝 Sub-agent 工具配置範例

```yaml
# subagent_config.yaml
tools:
  # 允許的工具
  allowed:
    - read
    - write
    - edit
    - exec
    - web_fetch
    - search
    - image
    - pdf
  
  # 需驗證的工具
  limited:
    - process
    - message
  
  # 禁止的工具
  blocked:
    - browser
    - memory_store
    - memory_update
    - memory_forget
    - mini_coding_agent
    - sessions_spawn

exec:
  # 允許的命令白名單
  allowed_commands:
    - ls, dir, pwd, cd, mkdir, cp, copy, mv, move
    - cat, type, head, tail, wc, grep, find, which
    - python, python3, node, npm, pip, git
    - echo, date, time, ps, df, du, free
  
  # 禁止的命令模式
  blocked_patterns:
    - "rm -rf"
    - "sudo*"
    - "*|sh"
    - ":(){ :|:& };:"
    - "curl*|sh"
    - "wget*-O-*|bash"

path:
  # 允許的目錄前綴
  allowed_prefixes:
    - "C:\\Users\\rayray\\.openclaw\\workspace_engineer"
    - "C:\\Users\\rayray\\.openclaw\\workspace_main"
```

---

## ✅ 預期效益

1. **防止誤操作導致系統損害**
   - 危險命令被阻擋
   - 路徑限制防止誤刪系統檔案

2. **限制 Sub-agent 權限範圍**
   - Sub-agent 僅能使用白名單工具
   - 敏感操作需主代理授權

3. **提升部署安全性**
   - 即使 Sub-agent 被攻擊，損害有限
   - 防止遠端代碼執行

4. **便於審計和監控**
   - 清楚定義允許/禁止清單
   - 異常操作可被檢測

---

## 📝 實作檢查清單

- [x] 建立工具分類（SAFE/LIMITED/DANGEROUS/BLOCKED）
- [x] 定義安全命令白名單
- [x] 實作工具過濾器
- [x] 實作參數驗證
- [x] 提供 Sub-agent 配置範例
- [x] 建立風險矩陣
- [ ] 與 OpenClaw 整合
- [ ] 建立監控日誌
