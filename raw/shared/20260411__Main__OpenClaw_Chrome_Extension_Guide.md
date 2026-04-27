# OpenClaw Chrome Extension 使用與問題排查

## 概述

讓蘇茉可以控制老爺現有的 Chrome 分頁，而不是開啟獨立的瀏覽器。

- **官網**：https://docs.openclaw.ai/tools/chrome-extension
- **Extension 名稱**：OpenClaw Browser Relay
- **Extension 版本**：0.1.0（原版）

---

## 架構

### 三個組成部分

| 元件 | 說明 |
|------|------|
| Browser control service | Gateway 或 node 上的 API |
| Local relay server | 本地 CDP 中繼 (`http://127.0.0.1:18792`) |
| Chrome MV3 extension | 使用 chrome.debugger 附加到分頁 |

### 運作流程

```
Chrome Extension ←→ Local Relay (18792) ←→ Gateway (18789)
```

1. Extension 附加到 Chrome 分頁
2. Extension 透過 local relay server 與 Gateway 溝通
3. Gateway 將指令傳給蘇茉處理

---

## 安裝步驟

### 1. 安裝擴充功能

```bash
openclaw browser extension install
```

### 2. 取得安裝路徑

```bash
openclaw browser extension path
```

輸出：`C:\Users\rayray\.openclaw\browser\chrome-extension`

### 3. Chrome 載入

1. 開啟 Chrome → `chrome://extensions`
2. 啟用右上角「開發者模式」
3. 點擊「載入未封裝」
4. 選擇：`C:\Users\rayray\.openclaw\browser\chrome-extension`
5. 點擊「釘選」圖示

### 4. 設定

| 設定項目 | 值 |
|----------|-----|
| **Port** | `18792` |
| **Gateway Token** | `77509115af9b3802ffced9f57e55e72fe6fd1fdf70f69a7b` |

---

## 使用方式

### 圖示狀態

| 圖示 | 狀態 | 說明 |
|------|------|------|
| `ON` | 已連線 | 可以控制分頁 |
| `!` | 錯誤 | 無法連接到 local relay |
| `...` | 連線中 | 稍等片刻 |

### 基本操作

```python
# 開啟分頁
browser(action="tabs", profile="chrome")

# 截圖
browser(action="snapshot", profile="chrome")

# 導航
browser(action="navigate", profile="chrome", targetUrl="https://...")
```

---

## 問題排查

### 常見錯誤

#### 1. 圖示顯示 `!`（驚嘆號）

**原因**：無法連接到本地中繼伺服器

**解決步驟**：

1. 檢查 Gateway 是否正在運行
   ```bash
   openclaw gateway status
   ```

2. 檢查 Port 18792 是否在監聽
   ```powershell
   Test-NetConnection -ComputerName 127.0.0.1 -Port 18792
   ```

3. 檢查 Extension 設定
   - Port 應該是 `18792`
   - Token 應該與 Gateway 設定一致

4. 重新載入 Extension
   - `chrome://extensions` → 找到 OpenClaw Browser Relay → 點擊「重新載入」

#### 2. 圖示顯示 `...`（三點）

**原因**：連線中或等待中

**解決步驟**：
- 等待幾秒
- 如果持續超過 30 秒，嘗試重新點擊圖示

#### 3. Gateway 版本與 Extension 不匹配

**錯誤訊息**：
```
invalid connect params: at root: unexpected property 'nonce'
at /client/id: must be equal to constant
```

**原因**：Extension 送的連線參數（含 `nonce`）新版 Gateway 不認得

**解決方案**：
1. 確保 Gateway 和 Extension 版本匹配
2. 或使用內建的 OpenClaw 瀏覽器（profile: openclaw）代替

---

## Extension 與內建瀏覽器的選擇

| 功能 | Chrome Extension | 內建瀏覽器 |
|------|------------------|------------|
| 控制老爺的 Chrome | ✅ 可以 | ❌ 不行 |
| 需要登入的網站 | ✅ 可以 | ❌ 不行 |
| 穩定性 | ⚠️ 版本匹配問題 | ✅ 穩定 |
| 設定複雜度 | ⚠️ 需要設定 | ✅ 簡單 |

**建議**：如果需要控制已登入的 Chrome 分頁，使用 Extension；否則使用內建瀏覽器。

---

## 安全注意事項

1. **模型可以點擊/輸入/導航分頁** - 可以訪問該分頁登入的帳號狀態
2. **建議使用專用的 Chrome profile** - 不要用日常瀏覽的
3. **Gateway 和 node host 放在同一個 tailnet** - 確保安全

---

## 版本歷史

| 日期 | 版本 | 備註 |
|------|------|------|
| 2026-03-08 | 0.1.0 | 初次安裝 |
| 2026-04-02 | 0.1.0 | 備份更新 |

---

*最後更新：2026-04-11*
*記錄者：總管蘇茉（TotalControlSuMo）*