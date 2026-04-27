# 8zz-banini-tracker 研究摘要

## 這個專案是什麼？

追蹤「反指標女神」巴逆逆（8zz）的 Threads / Facebook 貼文，系統持續巡檢，一抓到新貼文就立刻做 AI 反指標分析，並推送到 Telegram / Discord / LINE。

## 主要功能

1. **雙平台追蹤**：Threads + Facebook
2. **自動去重**：只處理新貼文
3. **AI 反指標分析**：
   - 辨識她提到的標的（個股、ETF、原物料）
   - 判斷她的操作（買入 / 被套 / 停損）
   - 反轉推導（她停損 → 可能反彈、她買入 → 可能下跌）
   - 推導連鎖效應（油價跌 → 製造業利多 → 電子股受惠）
4. **多平台通知**：Telegram / Discord / LINE
5. **即時輪詢模式**：作者一發文，系統下一輪檢查就會直接推送
6. **TradingView Pine Script 指標**：手動把巴逆逆訊號標到 K 線圖上

## 反指標邏輯

| 巴逆逆動作 | 指標解讀 |
|-----------|----------|
| 她停損 / 賣出 | 反指標偏多 |
| 她認錯 / 畢業 | 反指標偏多 |
| 她買進 / 加碼 | 反指標偏空 |
| 她看多 / 抄底 | 反指標偏空 |
| 她被套 / 繼續抱 | 反指標偏空 |
| 觀望 / 不明 | 中性觀察 |

##技術架構

- Node.js 20+
- Apify 抓取 Threads + Facebook
- OpenAI 相容 LLM（預設 DeepInfra / MiniMax-M2.5）
- 支援 Telegram Bot、Discord Webhook、LINE Messaging API

## 可用指令

```bash
npm run dev    # Threads + FB 各 3 篇，AI 分析 + 通知
npm run dry    # 只抓取，不呼叫 LLM（測試用）
npm run market # 盤中模式：FB only, 1 篇
npm run evening# 盤後模式：Threads + FB, 各 3 篇
npm run backtest # 回測過去一年貼文，計算勝率
```

## 回測功能

- 抓取過去一年內各最多 300 篇貼文
- 用台股日線資料計算貼文後第 1/3/5/10 個交易日的漲跌
- 依照反指標方向統計勝/負/平與勝率
- 存成 data/backtest-*.json

## 檔案結構

```
src/
  index.ts      # 主程式 + 排程邏輯
  threads.ts    # Apify Threads Scraper
  facebook.ts   # Apify Facebook Scraper
  analyze.ts    # LLM 反指標分析
  telegram.ts   # Telegram 通知
  discord.ts    # Discord Webhook
  line.ts       # LINE 推送
  report.ts     # 通知內容格式化
tradingview/
  banini-reverse-indicator.pine  # TradingView Pine Script
data/           # 執行資料（gitignore）
```

## 筆記

這是一個很有趣的反指標交易系統！
適合當作教育用途或參考學習用，不構成投資建議。