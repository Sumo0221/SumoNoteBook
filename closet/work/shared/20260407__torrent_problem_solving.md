# /torrent 自動化流程問題與解決記錄

## 日期
2026-04-03

## 背景
老爺反映 /torrent 之前可以全自動化搜尋+下載，但後來失效了。

---

## 問題分析

### 1. Cloudflare 保護
- **問題**：BT4G、1337x、The Pirate Bay 都有 Cloudflare 保護
- **影響**：Python requests 無法直接存取，會被擋在 Cloudflare 頁面

### 2. 瀏覽器工具不穩定
- **問題**：OpenClaw Browser Tool 常常超時
- **影響**：無法穩定地自動化操作網頁

### 3. Magnet URL 格式問題
- **問題**：BT4G 的 Magnet 連結有兩種格式：
  1. **代理格式**（BT4G 內部格式）：`bt4gprx.com/magnet/xxx` - 這不是真正的 BTIH hash
  2. **真正 Magnet**：`magnet:?xt=urn:btih:xxxxxxxx` - 真正的 hash
- **影響**：直接複製代理格式的 URL 加入 qBittorrent 無法下載

---

## 解決方案

### 1. 使用瀏覽器截圖確認頁面
- 透過截圖確認老爺是否已經在 BT4G 頁面
- 可以看到搜尋結果和相關資訊

### 2. 手動識別真正的 Magnet URL
- 從截圖中找到真正的 Magnet URL
- 格式如：`magnet:?xt=urn:btih:7d3c67cffec4790d8a26c1b3a84fd7c2d9c7f9b5`
- **關鍵**：必須提取 `btih:` 後面的 40 字符十六進制 hash

### 3. qBittorrent API 直接加入
- 使用 `add_to_qbittorrent.py` 自動附加 17 個公開 Trackers
- 然後直接加入 qBittorrent

---

## 自動化流程（目前可行版本）

```
1. 老爺在瀏覽器打開 https://bt4gprx.com
2. 搜尋關鍵字（如 ROYD181）
3. 蘇茉截圖確認頁面
4. 蘇茉嘗試用 evaluate 抓 Magnet URL
5. 如果超時，手動從截圖識別
6. 組裝完整 Magnet URL
7. 呼叫 add_to_qbittorrent.py 加入 qBittorrent
```

---

## 技術細節

### BT4G Magnet URL 格式
```
代理格式：https://bt4gprx.com/magnet/h5BE5xx7iscoRI5yZlBI8SqCPXLDq1IL
真正格式：magnet:?xt=urn:btih:7d3c67cffec4790d8a26c1b3a84fd7c2d9c7f9b5&dn=xxx
```

### add_to_qbittorrent.py 功能
- 自動登入 qBittorrent WebUI（Port 8080）
- 自動附加 17 個公開 Trackers
- 支援 Magnet URL 直接加入

---

## 教訓

1. **不要依賴代理格式的 URL** - 必須轉換成真正的 BTIH hash
2. **瀏覽器工具有穩定性問題** - 需要準備截圖識別作為備援
3. **qBittorrent API 是可靠的** - 只要拿到正確的 Magnet URL 就能成功

---

## 未來優化方向

1. 研究如何穩定地從 BT4G 提取真正的 Magnet URL
2. 考慮使用其他沒有 Cloudflare 保護的 torrent 網站
3. 自動化截圖分析，直接識別 Magnet URL
