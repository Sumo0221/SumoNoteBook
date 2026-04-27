# 蘇茉如何連接 Facebook 發文 - 經驗分享

整理者：小茉莉（偶像蘇茉）
整理時間：2026-04-07
來源：偶像蘇茉在「愛可樂粉絲團」群組與老爺的對話

---

## 🎯 目標

讓其他蘇茉了解如何透過 Playwright 控制 Chrome，自動發文到 Facebook 粉絲團。

---

## 📚 小茉莉使用 SumoNoteBook 的經驗

### 如何搜尋知識

使用 `query_notebook.mjs` 腳本：
```bash
cd C:\butler_sumo\library\SumoNoteBook\scripts
node query_notebook.mjs "關鍵字"
```

### 範例
```bash
# 搜尋「知識蒸餾」
node query_notebook.mjs "知識蒸餾"

# 搜尋更精準的內容
node query_notebook.mjs "youtube 知識蒸餾"
```

### 常見問題
- 如果出現 `Table 'sumo_notebook' not found`，需要重新執行攝取：`node ingest_notebook.mjs --rebuild`
- 編碼問題可能導致 `[內容已損壞]`，需要修復原始 Markdown 檔案

---

## 🌐 如何連接 Facebook（完整流程）

### Step 1：檢查 Chrome 是否已開啟遙控調試

```powershell
try {
    $r = Invoke-WebRequest -Uri "http://127.0.0.1:9222/json/version" -TimeoutSec 5 -ErrorAction Stop
    "Chrome is running with remote debugging"
} catch { 
    "Chrome not ready"
}
```

### Step 2：關閉所有 Chrome 程序

```powershell
Get-Process -Name chrome -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2
```

### Step 3：用正確參數啟動 Chrome

```powershell
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$profilePath = "C:\butler_sumo\Tools\AICola\chrome_debug_profile\Default"
Start-Process -FilePath $chromePath -ArgumentList "--remote-debugging-port=9222 --user-data-dir=`"$profilePath`""
```

### ⚠️ 重要：路徑必須包含 `\Default`

```
錯誤 ❌ - 會跳 profile picker
--user-data-dir="C:\butler_sumo\Tools\AICola\chrome_debug_profile"

正確 ✅ - 直接指定 Default profile
--user-data-dir="C:\butler_sumo\Tools\AICola\chrome_debug_profile\Default"
```

### Step 4：等待 Chrome 完全啟動

```powershell
Start-Sleep -Seconds 15
```

### Step 5：執行 AICola 發文腳本

```powershell
Set-Location C:\butler_sumo\Tools\AICola
python aicola_auto_post.py --once
```

### 循環發文（適用於多次）

```powershell
python aicola_auto_post.py --loop 5  # 發5次，間隔3分鐘
```

---

## 🔧 Chrome 遙控調試相關檔案路徑

| 項目 | 路徑 |
|------|------|
| Chrome 捷徑 | `C:\butler_sumo\Tools\AICola\Chrome_Remote_Debug.lnk` |
| Chrome 設定檔 | `C:\butler_sumo\Tools\AICola\chrome_debug_profile\Default` |
| AICola 發文腳本 | `C:\butler_sumo\Tools\AICola\aicola_auto_post.py` |
| 發文圖片目錄 | `C:\butler_sumo\Tools\AICola\pic\` |
| Chrome 問題排查筆記 | `C:\butler_sumo\memory\chrome-debugging-notes.md` |

---

## ❌ 常見錯誤與解法

### 錯誤 1：停在 `chrome://profile-picker/`
- **原因**：設定檔路徑只到 parent folder
- **解法**：指定到 `\Default` 子資料夾

### 錯誤 2：`Page.goto: Target page, context or browser has been closed`
- **原因**：Chrome 还没完全啟動或 profile 被鎖定
- **解法**：增加等待時間，或先關閉所有 Chrome 程序再重試

### 錯誤 3：`Cannot connect to Chrome at 9222`
- **原因**：Chrome 沒有開啟遙控調試端口
- **解法**：使用正確的命令列參數啟動 Chrome

---

## 💡 小茉莉的心得

1. **路徑很重要** - 設定檔路徑一定要包含 `\Default`，否則會跳 profile picker
2. **等待時間要足夠** - 至少 15 秒讓 Chrome 完全啟動
3. **先關閉乾淨** - 重啟 Chrome 前要先殺掉所有程序，避免端口被佔用
4. **SumoNoteBook 是好幫手** - 遇到問題可以先搜看看有沒有相關筆記

---

## 📝 相關筆記

- Chrome 問題排查：`C:\butler_sumo\memory\chrome-debugging-notes.md`
- SumoNoteBook RAG System：`C:\butler_sumo\library\SumoNoteBook\scripts\README.md`
