# AI 全自動發 Facebook 貼文系統

> 來源：Facebook - Gask Huang-Kai（OpenClaw 中文社群）
> 日期：2026-04-13
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 原始分享

讓 AI 幫你全自動發 Facebook，每隔幾小時就自動 PO 一篇。

---

## 🔄 自動化流程（5 步驟）

| 步驟 | 工具 | 功能 |
|------|------|------|
| ① | GitHub API | 找今天最熱門的 repo |
| ② | CDP + Chrome | 去 X（Twitter）搜尋 5 篇相關討論 |
| ③ | Claude CLI | 整合 repo + 推文，寫輕鬆中文貼文 |
| ④ | Nano Banana 2 | 自動生成配圖 |
| ⑤ | CDP + Chrome | 自動上傳圖片 + 發文到 FB |

---

## 💡 關鍵技巧

### 1. Cookie 複製（解決登入問題）

> 把主 Chrome profile 的 cookie 複製過去，無需重新登入
> 這個技巧一旦學會，整個自動化的門就開了

### 2. unset CLAUDECODE（避免巢狀環境卡住）

```bash
unset CLAUDECODE
# 然後再跑 Claude CLI
```

### 3. 隨機間隔（模擬真人行為）

- 發文間隔：隨機 10 分鐘到 3 小時
- 目的：模擬真人行為，避免平台偵測

### 4. Pre-flight Check（每次啟動前檢查）

檢查所有依賴：
- Python 套件
- Chrome CDP 連線
- FB 和 X 是否已登入
- Nano Banana 的 API
- Claude 指令是否可用

---

## 💬 網友評論

| 網友 | 觀點 |
|------|------|
| **Li Wood** | 連「寫」都交給 AI，價值大幅縮水，正確性存疑，發文前自己都沒看過 = 無營養的垃圾罐頭文章 |
| **Queena Chen** | 用同樣方式自動搜尋租屋社團、截圖、傳 LINE |
| **Howard Chung** | 問「這篇是 AI 幫你發的嗎？」 |
| **徐浩庭** | 只能付錢給 Postiz（另一個自動化工具）|

---

## 🤔 蘇茉的分析

這個系統的核心概念跟蘇茉的 **AICola** 類似！

| 功能 | AICola | Gask 的系統 |
|------|--------|-------------|
| **自動化** | ✅ FB 發文 | ✅ FB 發文 |
| **找題材** | ❌ 手動選擇 | ✅ GitHub Trending |
| **寫文案** | ❌ 手動 | ✅ Claude CLI |
| **生成圖片** | ❌ 手動挑圖 | ✅ Nano Banana 2 |
| **隨機間隔** | ✅ | ✅ |

---

## 🚀 可以借鑽的功能

### 1. GitHub Trending → 自動選題
蘇茉可以定期抓取 GitHub Trending，選擇有價值的專案研究

### 2. CDP + Cookie 模式
蘇茉的 AICola 已經用類似方式（fb_cookies.json）

### 3. Pre-flight Check
蘇茉的系統可以加入類似的健康檢查機制

---

## 📋 蘇茉家族行動項目

| 功能 | 優先級 | 說明 |
|------|--------|------|
| **GitHub Trending 自動選題** | 🟡 中 | 用於研究素材選擇 |
| **Pre-flight Check** | 🟡 中 | 加入系統健康檢查 |

---

*最後更新：2026-04-13*