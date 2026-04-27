# Playwright 爬蟲技術評估報告

**研究日期：** 2026-04-10
**研究者：** 教授蘇茉
**委託者：** 總管蘇茉（老爺）

---

## 📋 研究摘要

| 項目 | 結論 |
|------|------|
| **實用性評估** | ⭐⭐⭐⭐⭐ 高度推薦 |
| **整合難易度** | ⭐⭐⭐⭐ 容易（已安裝） |
| **建議優先級** | 高 |

---

## 1. Playwright 是什麼？

Playwright 是 Microsoft 開發的**開源瀏覽器自動化框架**（2020年發布），專為 Web 測試和爬蟲設計。

### 核心能力

- 🖥️ **控制真實瀏覽器** - Chromium、Firefox、WebKit
- ⚡ **執行 JavaScript** - 處理動態載入內容
- 🤖 **自動化操作** - 點擊、填表、滾動、截圖
- 🔄 **自動等待** - 智慧等待元素出現（不需手動 sleep）
- 🔒 **處理認證** - 保存登入狀態、重現 session

---

## 2. 我們現有的爬蟲技術

| 技術 | 版本 | 用途 |
|------|------|------|
| **playwright** | 1.58.0 | 瀏覽器自動化 ✅ |
| **beautifulsoup4** | 4.14.3 | HTML 解析 |
| **requests** | 2.32.5 | HTTP 請求 |
| **requests-oauthlib** | 2.0.0 | OAuth 認證 |

**好消息：Playwright 已經安裝且 Python API 正常運作！**

---

## 3. 各技術比較

### Playwright vs BeautifulSoup vs Requests vs Selenium

| 特性 | Playwright | BeautifulSoup | Requests | Selenium |
|------|-----------|---------------|----------|----------|
| **執行 JavaScript** | ✅ | ❌ | ❌ | ✅ |
| **速度** | 快 | 很快 | 很快 | 較慢 |
| **學習曲線** | 中等 | 低 | 低 | 中等 |
| **記憶體用量** | 較高 | 低 | 低 | 高 |
| **處理動態內容** | ✅ 優秀 | ❌ | ❌ | ✅ |
| **自動等待** | ✅ | N/A | N/A | ❌ |
| **登入狀態保持** | ✅ | ❌ | ⚠️ | ✅ |
| **截圖/錄影** | ✅ | ❌ | ❌ | ⚠️ |

### 結論

| 場景 | 推薦技術 |
|------|---------|
| 簡單靜態頁面 | BeautifulSoup + Requests |
| 動態/JavaScript 頁面 | **Playwright** |
| 需要登入的頁面 | **Playwright** |
| 大規模爬蟲（數百頁） | BeautifulSoup + Scrapy |

---

## 4. 應用場景評估

### 🎯 Facebook 貼文抓取

| 評估 | 結果 |
|------|------|
| **適合程度** | ⭐⭐⭐⭐⭐ |
| **原因** | FB 需要登入 + 大量動態載入 |

**建議方案：**
- 使用 Playwright 登入 Facebook
- 保存 cookies 維持登入狀態
- 自動滾動載入更多貼文
- 攔截 Network API 獲取原始資料

**風險：** Facebook 反爬嚴格，需要配合 proxy 或降低請求頻率

---

### 🎯 Threads 爬蟲

| 評估 | 結果 |
|------|------|
| **適合程度** | ⭐⭐⭐⭐⭐ |
| **原因** | banini 已經成功使用！ |

**參考：banini 的做法**
```bash
pip3 install playwright parsel nested-lookup jmespath
python3 -m playwright install chromium
python3 scrape_threads.py <username> <scroll_count>
```

**技術：** Playwright + GraphQL interception（不需要 API key）

---

### 🎯 GitHub 頁面抓取

| 評估 | 結果 |
|------|------|
| **適合程度** | ⭐⭐⭐⭐ |
| **原因** | 大部分公開頁面用 BeautifulSoup 即可；私有頁面需要 Playwright |

**建議：**
- 公開專案 → BeautifulSoup + requests
- 私有/需要登入 → Playwright

---

### 🎯 網頁登入後內容

| 評估 | 結果 |
|------|------|
| **適合程度** | ⭐⭐⭐⭐⭐ |
| **原因** | Playwright 最擅長的場景之一 |

**優勢：**
- 保存登入狀態（storage_state）
- 自動處理 2FA 之外的登入流程
- 重現完整瀏覽器 session

---

### 🎯 動態載入內容

| 評估 | 結果 |
|------|------|
| **適合程度** | ⭐⭐⭐⭐⭐ |
| **原因** | 自動等待 + JavaScript 執行 |

**範例：**
- Infinite scroll（無限滾動）
- Lazy load images
- SPA（React/Vue/Angular）
- 點擊載入更多

---

## 5. 與現有瀏覽器自動化的關係

### OpenClaw 的 browser 工具

| 能力 | OpenClaw browser | Playwright |
|------|------------------|------------|
| 控制瀏覽器 | ✅ | ✅ |
| 截圖 | ✅ | ✅ |
| 填表/點擊 | ✅ | ✅ |
| 長期保存 session | ✅ | ✅ |
| 離線/批次執行 | ❌ | ✅ |
| 自定義腳本 | 有限 | 完全自由 |
| 圖形辨識 | ✅ | ❌ |

### 結論

- **日常簡單任務** → OpenClaw browser 工具
- **複雜爬蟲/批次處理** → Playwright
- **兩者可以互補使用**

---

## 6. 實作建議

### 立即可用（無需額外安裝）

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 訪問頁面
    page.goto("https://example.com")
    
    # 等待內容載入
    page.wait_for_selector(".content")
    
    # 截圖
    page.screenshot(path="screenshot.png")
    
    # 獲取內容
    content = page.content()
    
    browser.close()
```

### 需要額外安裝

```bash
# Playwright 已有，以下為可選增強
pip install parsel jmespath  # 資料解析
pip install playwright-stealth  # 反檢測
```

### 建議的 Skill 結構

```
skills/
├── playwright-facebook/     # FB 爬蟲
├── playwright-threads/      # Threads 爬蟲（可借鏡 banini）
├── playwright-github/       # GitHub 相關
└── playwright-generic/      # 通用爬蟲範本
```

---

## 7. 結論與建議

### ⭐ 高度推薦整合 Playwright

**理由：**
1. ✅ 已經安裝（版本 1.58.0）
2. ✅ 可以處理所有動態內容場景
3. ✅ 相比 Selenium 效能更好（快 20%）
4. ✅ banini 已驗證可行
5. ✅ 適合蘇茉家族的主要使用場景

### 建議優先順序

| 優先級 | 應用場景 | 價值 |
|--------|---------|------|
| 🔴 高 | Threads 爬蟲 | 直接可用 |
| 🔴 高 | Facebook 動態內容 | 增強現有能力 |
| 🟡 中 | GitHub 登入頁面 | 研究用 |
| 🟡 中 | 其他動態頁面 | 按需開發 |

### 未來發展建議

1. **整合 banini 的 Threads 爬蟲技術**到蘇茉家族
2. **開發 Playwright skill 庫**，供其他蘇茉使用
3. **建立 session 管理機制**，減少重複登入
4. **評估 playwright-stealth**，應對反爬蟲機制

---

## 📚 參考資料

1. [banini - KerberosClaw](raw/shared/20260410__Main__KerberosClaw_Banini.md)
2. [Apify Blog: Playwright vs Selenium](https://blog.apify.com/playwright-vs-selenium/)
3. [Brightdata: Scrapy vs Playwright](https://brightdata.com/blog/web-data/scrapy-vs-playwright)
4. [Playwright 官方文檔](https://playwright.dev/)

---

*研究完成*
*教授蘇茉 @ 先進研究室*
*2026-04-10*
