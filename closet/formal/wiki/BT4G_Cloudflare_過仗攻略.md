# BT4G Cloudflare 過仗攻略

## 問題描述

| 階段 | 方法 | 結果 |
|------|------|------|
| 第一次 | `torrent_search.py` | ❌ UnicodeEncodeError + Cloudflare 阻擋 |
| 第二次 | OpenClaw 預設瀏覽器 | ❌ 一直卡在 Cloudflare 驗證頁面 |
| 第三次 | 等待 5 秒後重新整理 | ✅ 成功通過 Cloudflare |

---

## 正確流程（100% 成功）

### Step 1: 用預設瀏覽器開啟 BT4G
```
browser(action="open", url="https://bt4gprx.com/search?q=關鍵字")
```

### Step 2: 等待 10 秒
```
Start-Sleep -Seconds 10
```

> 建議等 10 秒更穩妥，網路慢的時候也不會失敗。

### Step 3: 截圖確認是否通過
```
browser(action="snapshot", targetId="<targetId>", compact=true)
```

### Step 4: 如果看到驗證頁面
- **不要點擊任何按鈕**
- **等待大約 5-10 秒**
- **再次截圖確認**
- Cloudflare 會自動跳轉到搜尋結果

### Step 5: 從搜尋結果點進 Magnet 詳情頁
- 找 Seeders > 0 的項目
- 點擊標題進入詳情頁

### Step 6: 從詳情頁提取 Magnet Hash
- **注意**：URL 路徑不是真正的 hash
- 要從「Download」區域的連結提取

---

## 為什麼之前會失敗？

| 錯誤做法 | 原因 |
|----------|------|
| 用 torrent_search.py | 被 Cloudflare 直接阻擋 |
| 用 `profile="my-daily-chrome"` | 不適用，沒有老爺的 session |
| 截圖一次就放棄 | Cloudflare 驗證需要時間 |
| 點擊驗證按鈕 | 不需要，會自動通過 |

---

## 關鍵技巧

### 1. 預設瀏覽器可以直接通過
OpenClaw 預設瀏覽器**不需要**指定 profile，直接用就能通過 Cloudflare。

### 2. 等待是關鍵
Cloudflare 驗證大約需要 **5 秒**，蘇茉需要耐心等待。

### 3. 不要點擊任何按鈕
Cloudflare 會自動跳轉，不需要人工介入。

---

## 參考指令

```javascript
// 開啟搜尋頁面
browser(action="open", url="https://bt4gprx.com/search?q=PFES124")

// 等待 5 秒
Start-Sleep -Seconds 5

// 截圖確認
browser(action="snapshot", targetId="<targetId>", compact=true)

// 進入 Magnet 詳情頁
browser(action="navigate", targetId="<targetId>", url="https://bt4gprx.com/magnet/<hash>")
```

---

## 同樣的地方，摔倒一次就夠了

> 不要再摔倒第二次以上。

---

*記錄者：總管蘇茉*
*時間：2026-04-08 23:15*
*原因：老爺提醒蘇茉記錄錯誤，下次不要再犯*
