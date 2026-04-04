---
name: sumo-torrent (蘇茉 Torrent 技能)
version: 1.0.0
description: 搜尋 BT4G 種子並自動添加到 qBittorrent 下載。支援 OpenClaw 瀏覽器自動化與 Cloudflare 繞過。
metadata:
  openclaw:
    requires:
      env:
        - PYTHONIOENCODING
        - QBIT_USER
        - QBIT_PASS
        - QBIT_URL
      bins:
        - python
      note: "qBittorrent WebUI 必須運行在 8080 端口"
tags:
  - torrent
  - download
  - bt4g
  - qbittorrent
  - magnet
  - search
  - chinese
examples:
  - "/torrent waaa087"
  - "/torrent SONE481"
---

# Sumo Torrent Skill（蘇茉 Torrent 技能）

## 概述

這個技能讓 OpenClaw 代理可以搜尋 BT4G 上的種子，並自動將 magnet 連結添加到正在運行的 qBittorrent。它會處理 Cloudflare 驗證、正確的 magnet hash 提取，以及 tracker 充實。

## 安裝

### 1. qBittorrent 安裝與 WebUI 設定

1. 下載並安裝 [qBittorrent](https://www.qbittorrent.org/)
2. 啟用 WebUI：**工具 → 選項 → Web UI**
   - 監聽所有介面：`127.0.0.1:8080`
   - 設定您的使用者名稱和密碼（**不要使用預設值！**）
3. **保持 qBittorrent 在背景執行**

### 2. 環境變數（安全性）

使用前請設定這些環境變數：

```bash
# Linux/Mac
export QBIT_USER=your_username
export QBIT_PASS=your_password
export QBIT_URL=http://localhost:8080

# Windows (PowerShell)
$env:QBIT_USER="your_username"
$env:QBIT_PASS="your_password"
$env:QBIT_URL="http://localhost:8080"
```

**安全性提醒：** 千萬不要把密碼寫進程式碼！建議加到 `.bashrc` 或 `.env` 檔案中。

### 3. 安裝技能

將技能資料夾複製到 OpenClaw skills 目錄：
```
~/.openclaw/skills/sumo-torrent/
```

或使用 clawhub CLI：
```bash
clawhub install sumo-torrent
```

## 使用方式

### 基本搜尋

```
/torrent <關鍵字>
```

範例：
```
/torrent SONE481
/torrent MIAA230
```

### 工作原理

1. 代理使用瀏覽器自動化搜尋 BT4G（繞過 Cloudflare）
2. 過濾結果，只顯示有種子的項目（Seeders > 0）
3. 從詳情頁提取**真正的 40 字符十六進制 info hash**
4. 加入 22 個公開 trackers 到 magnet 連結
5. 直接發送到 qBittorrent WebUI API

### 重要：如何取得真正的 Info Hash

**千萬不要**直接使用 BT4G 網址中的 hash - 那是 32 字符的 Base32，qBittorrent 不認識！

**正確方法：**
1. 點擊搜尋結果的標題，進入詳情頁
2. 找到下載連結：`//downloadtorrentfile.com/hash/40字符十六進制`
3. 提取 `/hash/` 後面的 **40 字符十六進制** hash
4. 組裝 magnet：`magnet:?xt=urn:btih:{40字符hex}&dn={名稱}`

## Cloudflare 繞過

技能使用帶有現有 session cookies 的瀏覽器 profile 來繞過 Cloudflare 驗證，避免「正在檢查您的瀏覽器」迴圈。

## 故障排除

### Cloudflare 阻擋
如果 Cloudflare 阻擋請求，請確保您的瀏覽器 profile 有來自先前成功登入的有效 session cookies。

### qBittorrent 無回應
- 檢查 WebUI 是否啟用：http://localhost:8080
- 確認環境變數設定正確
- 確認 qBittorrent 正在執行

### 沒有 Seeders
如果所有搜尋結果的 Seeders 都是 0，表示這個種子已經死了，無法下載。請嘗試不同的關鍵字。

## 環境變數

| 變數 | 預設值 | 說明 |
|------|--------|------|
| `QBIT_USER` | admin | qBittorrent 使用者名稱 |
| `QBIT_PASS` | adminadmin | qBittorrent 密碼（**強烈建議更改！**）|
| `QBIT_URL` | http://localhost:8080 | qBittorrent WebUI 網址 |

## 檔案說明

| 檔案 | 用途 |
|------|------|
| `torrent_search.py` | 主要搜尋腳本 |
| `add_to_qbittorrent.py` | qBittorrent API 整合 |
| `torrent.bat` | Windows 批次包裝 |

## 安全性最佳實踐

1. **更改 qBittorrent 預設密碼** - `adminadmin` 已是眾所皆知
2. **使用環境變數** - 千萬不要把密碼寫死
3. **保持 WebUI 在本機** - 不要對外開放 8080 端口
4. **使用防火牆規則** - 只允許您自己的 IP 存取

## 貢獻

由蘇茉家族（SumoSuMo）開發。
採用 MIT License 釋出。
