# MiniMax 2.7 視覺功能破解技巧

> 來源：Facebook - OpenClaw 中文社群 - 喬瑟夫
> 日期：2026-04-13
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 原文標題

**從 OpenClaw 到 Hermes：兩套開源 AI Agent 框架的真實比較**

**另一篇**：原來 MiniMax 2.7 不是瞎子，只是大門沒開？打通高性價比 AI 的視覺神經！

---

## 🎯 核心洞見

### MiniMax 2.7 圖片輸入問題

**問題**：官方文件寫「不支援圖片輸入」，直接傳圖會報錯

**真相**：MiniMax 底層其實看得懂圖，只是官方沒有說清楚明確路徑

---

## 🔑 解決方法：Tool Calling + Base64

### 關鍵步驟

1. **使用 Tool Calling（工具呼叫）**，不要用一般對話 API
2. 遇到圖片時，**轉成 Base64 編碼**
3. **標記成「這是工具執行的結果」(tool_result)**
4. 把 Base64 代碼遞給 MiniMax 系統
5. MiniMax 會自動呼叫視覺模型解析圖片

### 底層邏輯

```
一般 API 接口 → 會擋掉傳圖
Tool Calling → 圖片轉 Base64 → 標記為 tool_result → MiniMax 看懂圖片
```

---

## 💡 評論精選

| 網友 | 建議 |
|------|------|
| **Hok To Li** | 把 MCP 封裝作 plugin，把官方 image 功能關掉，agent 就自動會懂得用 minimax 的圖片功能 |
| **Chung Jobria** | 想請教如何命令 openclaw 自動將圖片轉化為 base64 文字 |

---

## 📊 互動數據

| 指標 | 數值 |
|------|------|
| 讚 | 42 |
| 回覆 | 11 |
| 分享 | 12 |

---

## 📋 相關資源

- MiniMax API 文件：https://platform.minimax.io/subscribe/token-plan...
- 養龍蝦 (OpenClaw)
- 愛馬仕 (Hermes)

---

## 💭 蘇茉觀察

這是一個很實用的技術分享！說明了：
1. MiniMax 2.7 底層其實支援視覺，只是官方 API 擋掉了
2. 透過 Tool Calling + Base64 可以繞過這個限制
3. OpenClaw 和 Hermes 都適用這個方法

---

*最後更新：2026-04-13*