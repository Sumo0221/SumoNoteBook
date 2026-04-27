# 🔍 Torrent Skill 問題檢討與解決報告

**日期**：2026-04-04
**問題**：bt4gprx.com Cloudflare 驗證 + Magnet Hash 提取錯誤
**耗時**：從可以變成不行，折騰了很久

---

## 📋 問題 1：Cloudflare 驗證卡住

### 症狀
- 瀏覽器操作超時（timeout）
- 嘗試 3-5 次都失敗
- 錯誤訊息：`tab not found`、`timed out`

### 原因分析
| 原因 | 說明 |
|------|------|
| Profile 錯誤 | 一直用 `target="host"` 而不是 `profile="my-daily-chrome"` |
| 無法通過 Cloudflare | openclaw 預設瀏覽器被 Cloudflare 阻擋 |
| 等待時間不夠 | 只等 20-40 秒，Cloudflare 驗證需要更久 |

### 解決方法
```
# 正確的瀏覽器操作
browser(action="navigate", profile="my-daily-chrome", url="https://bt4gprx.com/search?q=KEYWORD")
browser(action="snapshot", profile="my-daily-chrome", targetId="<targetId>")
```

### 關鍵：使用 `profile="my-daily-chrome"`
- 這個 profile 有老爺已登入的瀏覽器 session
- 可以直接通過 Cloudflare 驗證

---

## 📋 問題 2：Magnet Hash 搞錯

### 症狀
- qBittorrent 加入失敗（返回 "Fails"）
- Hash 是 32 字符的 Base32 編碼，不是真正的 40 字符十六進制

### 原因分析
| 錯誤 | 正確 |
|------|------|
| 直接用 URL Path：`/magnet/SaVQMeJ0D89m3GadFHVne6M9ZbQNEydmA` | 點進詳情頁抓 `/hash/xxxx` |
| 32 字符 Base32 | 40 字符十六進制 |
| 這不是真正的 info hash | 需要從下載連結提取 |

### 解決方法
1. **點進詳情頁**（點擊搜尋結果標題）
2. 找「Download」區塊的連結
3. URL 格式：`//downloadtorrentfile.com/hash/40字符十六進制?name=...`
4. 提取 `/hash/` 後面的 40 字符才是真正的 info hash

### 正確的 Magnet 格式
```
magnet:?xt=urn:btih:40字符十六進制&dn=標題
```

---

## 📋 問題 3：qBittorrent API 認證

### 症狀
- 登入成功但加入失敗（返回 "Fails"）

### 原因
- 需要每次重新登入取得新的 SID cookie
- 之前用舊的 SID 過期了

### 解決方法
```python
# 每個操作前都要重新登入
login_url = 'http://localhost:8080/api/v2/auth/login'
r = requests.post(login_url, data={'username': 'admin', 'password': 'adminadmin'})
sid = r.cookies.get('SID')

# 然後用新的 SID 加入 torrent
```

---

## 💡 瀏覽器操作關鍵經驗

### 1. Profile 選擇
```
❌ target="host"
✅ profile="my-daily-chrome"  # 有完整 session，可通過 Cloudflare
```

### 2. 截圖診斷
- 不要盲目等待，先截圖看狀態
- 如果是 Cloudflare 驗證頁面，表示還需要時間
- 如果是空白頁或錯誤，可能需要重試

### 3. 點擊進入詳情頁
- 搜尋結果頁只顯示 Base32 短 hash
- 需要點進去詳情頁才能拿到真正的 40 字符十六進制 hash

### 4. 頁面元素取值
- URL 在 `/url:` 欄位
- 點擊用 `ref` 參考

---

## 📝 未來避免問題的方法

### 瀏覽器操作標準流程
1. 確認使用 `profile="my-daily-chrome"`
2. 截圖確認頁面狀態
3. 如果是 Cloudflare，等待並再次截圖確認
4. 從詳情頁提取真正的 info hash
5. 每次 API 操作前重新登入

### 測試清單
- [ ] 用 profile="my-daily-chrome" 開頁面
- [ ] 截圖確認通過 Cloudflare
- [ ] 點進詳情頁確認有下載連結
- [ ] 提取 40 字符十六進制 hash
- [ ] 重新登入 qBittorrent
- [ ] 加入 torrent 並確認成功

---

## 🎯 對新任務的建議

### 瀏覽器相關任務
1. 優先使用 `profile="my-daily-chrome"` 避免 Cloudflare
2. 先截圖確認狀態再繼續
3. 重要操作（如登入、付款）要先測試
4. 記錄頁面結構和元素取值方式

### 文件記錄
- 每個 skill 都要記錄踩坑經驗
- 重要：文件位置、操作順序、URL 格式
- 更新 TOOLS.md 讓其他蘇茉也能學習

---

**記錄時間**：2026-04-04 02:17 GMT+8
**記錄者**：總管蘇茉
