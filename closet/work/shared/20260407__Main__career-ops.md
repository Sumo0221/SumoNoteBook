# career-ops 研究報告

**研究日期**：2026-04-07  
**來源**：https://github.com/santifer/career-ops  
**分類**：工具研究 / AI 應用

---

## 專案概述

**career-ops** 是一個基於 **Claude Code** 建構的 AI 求職系統，由 Santiago（Head of Applied AI）開發。

> 他本人用這個系統評估了 740+ 工作機會、生成 100+ 客製化履歷，並成功獲得 Head of Applied AI 職位。

**核心理念**：這不是一個「海投工具」，而是一個**過濾器**——幫助你在數百個職缺中找出少數值得投入時間的機會。系統強烈建議不要申請評分低於 4.0/5 的職位。

---

## 核心功能

| 功能 | 說明 |
|------|------|
| **Auto-Pipeline** | 貼上 URL，自動完成評估 + PDF + 追蹤 |
| **A-F 評價系統** | 10 個加權維度的結構化評分 |
| **ATS PDF 生成** | 關鍵字優化的履歷 PDF（Space Grotesk + DM Sans 設計） |
| **入口網站掃描器** | 45+ 公司預設配置（Anthropic, OpenAI, ElevenLabs, Retool, n8n...） |
| **批次處理** | 並行評估 10+ 職缺（使用 Claude Code sub-agents） |
| **面試故事庫** | 累積 STAR+Reflection 故事，回答任何行為面試問題 |
| **談判腳本** | 薪資談判框架、地理折扣反駁、競爭offer槓桿 |
| **Terminal Dashboard** | Go 語言的 TUI 介面，瀏覽、過濾、排序 pipeline |

---

## 技術架構

- **Agent 引擎**：Claude Code + 14 種 skill modes
- **PDF 生成**：Playwright/Puppeteer + HTML 模板
- **入口網站掃描**：Playwright + Greenhouse API + WebSearch
- **Dashboard UI**：Go + Bubble Tea + Lipgloss（Catppuccin Mocha 主題）
- **資料格式**：Markdown tables + YAML config + TSV batch files

---

## 專案目錄結構

```
career-ops/
├── CLAUDE.md          # Agent 指令
├── cv.md              # 你的履歷
├── config/            # 設定檔
├── modes/             # 14 種 skill modes
│   ├── oferta.md      # 單一評估
│   ├── pdf.md         # PDF 生成
│   ├── scan.md        # 入口掃描
│   └── batch.md       # 批次處理
├── templates/         # HTML 模板、portals 配置
├── dashboard/         # Go TUI
├── data/              # 追蹤資料
├── reports/           # 評估報告
└── output/            # 生成的 PDF
```

---

## 對蘇茉家族的價值評估

**價值程度：🟡 中等**

### 有價值的部分：
- **多模式 Agent 架構**：14 種 skill modes 的設計模式值得參考
- **批次處理**：Claude Code sub-agents 的並行處理模式
- **入口掃描器**：整合多個招聘平台的技術實作
- **PDF 生成流程**：Playwright HTML to PDF 的技術方案

### 不太相關的部分：
- 這是個人求職工具，與蘇茉家族的 AI Agent 研究方向不太直接相關
- 主要是應用層面的工具，非基礎架構

---

## 結論

作為研究參考資料有一定價值，但無需深入整合。可以借鑒其：
1. 多模式 Agent 架構設計
2. 批次處理並行化模式
3. 入口網站爬蟲技術
