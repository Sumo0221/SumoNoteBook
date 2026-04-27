# KerberosClaw banini - 反指標追蹤器

## 基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | KerberosClaw |
| **GitHub** | https://github.com/KerberosClaw/kc_ai_skills |
| **專案** | banini - 反指標女神巴逆逆追蹤器 |
| **觸發指令** | `/banini` |
| **觸發關鍵字** | '巴逆逆', '反指標', '冥燈', '/banini' |

---

## 這是什麼？

追蹤「反指標女神」巴逆逆（8zz）的 Threads 貼文，直接進行**反指標分析**的技能。

---

## 核心功能

### 🎯 反指標分析邏輯

| 她的狀態 | 反指標解讀 | 原因 |
|---------|-----------|------|
| 買入/加碼 | 該標的可能下跌 | 她買什麼跌什麼 |
| 持有中/被套 | 該標的可能繼續跌 | 她還沒認輸，底部還沒到 |
| 停損/賣出 | 該標的可能反彈上漲 | 她認輸出场 = 底部訊號 |
| 看多/喊買 | 該標的可能下跌 | 她看好的通常會跌 |
| 看空/喊賣 | 該標的可能上漲 | 她看衰的通常會漲 |
| 空單/買 put | 該標的可能飆漲 | 她空什麼就漲什麼 |

---

## 技術架構

### 🐍 爬蟲腳本

| 項目 | 說明 |
|------|------|
| **技術** | Playwright + GraphQL interception |
| **平台** | Threads（Meta） |
| **依賴** | playwright, parsel, nested-lookup |
| **認證** | 不需要 API key |

### 📡 爬蟲原理

1. 使用無頭 Chromium 訪問 Threads
2. 攔截 GraphQL 回應
3. 解析 post 資料
4. 輸出 JSON array

---

## 安裝依賴

```bash
pip3 install playwright parsel nested-lookup jmespath
python3 -m playwright install chromium
```

---

## 使用方式

### 基本指令

```bash
python3 scrape_threads.py banini31 5
```

- `banini31` = 預設 username
- `5` = 捲動次數（通常抓 10-20 篇）

### 觸發方式

| 方式 | 指令 |
|------|------|
| 互動模式 | `/banini` |
| 指定用戶 | `/banini <username>` |

---

## 輸出報告格式

```
## 巴逆逆反指標分析報告

**分析時間：** {現在時間}
**資料來源：** Threads @{username}

---

### 提及標的

↑/↓/→ {標的名稱}
- **她的操作：** {操作描述}
- **反指標：** {反轉推導}
- **信心：** 高/中/低
- **相關標的：** {如適用}

---

### 連鎖推導

1. ...
2. ...
3. ...

### 建議方向

（1-2 段文字）

### 冥燈指數：{N}/10

*僅供娛樂參考，不構成投資建議*
```

---

## cron 整合

```bash
/skill-cron add banini "7,37 9-12 * * 1-5" 盤中
/skill-cron add banini "3 23 * * *" 盤後
```

---

## 與蘇茉家族的關係

| 項目 | 對應 |
|------|------|
| **台股分析** | 蘇茉有 SumoFinance |
| **反指標分析** | 可作為參考指標 |
| **Threads 爬蟲** | 可借鏡技術 |

---

## 💡 對蘇茉的啟發

1. **反指標分析** - 可以整合進 SumoFinance
2. **Playwright 爬蟲** - Threads 爬蟲技術可借鏡
3. **冥燈指數** - 創意的量化指標概念

---

## 標籤

#知識儲備 #banini #反指標 #Threads爬蟲 #Playwright #台股分析 #冥燈指數 #KerberosClaw

---

*記錄者：總管蘇茉*
*時間：2026-04-10 00:08*
