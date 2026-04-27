# attention-research × SumoNoteBook 整合建議報告

**研究日期**：2026-04-22 15:49  
**研究者**：教授蘇茉  
**目標**：將 attention-research 的智慧研究管道功能整合到 SumoNoteBook

---

## 一、attention-research 核心概念分析

### 1.1 每日兩次自動監控
- **設計**：早晨 + 下午兩個時間點自動執行研究任務
- **排程**：使用 cron job 驅動，確保紀律性
- **價值**：將被動研究轉為主動式情報收集

### 1.2 主題監控框架
- **META.json**：每個主題有獨立的中繼資料（時間戳、狀態）
- **新鮮度門檻**（Freshness Gate）：避免重複執行
- **Domain-specific prompts**：每個主題有專屬的監控 prompt

### 1.3 變化偵測
- **跨時間整合信號**：不僅收集資訊，還要識別「改變了什麼」
- **Threshold Alert**：達到特定條件時主動警告用戶
- **不是新聞聚合器**：是信號追蹤系統

### 1.4 結構化摘要
- ** Digest 格式**：統一的研究輸出格式
- **Prompt Stack Order**：系統化的提示堆疊（Core → Topics → Templates）
- **Delivery**：透過 Telegram/WhatsApp 主動推送

---

## 二、SumoNoteBook 現有功能評估

### 2.1 研究報告儲存
| 功能 | 現況 | 評估 |
|------|------|------|
| 研究報告存放 | `research/` 目錄 | ✅ 已有結構化儲存 |
| 研究索引 | `research_index.md` | ✅ 有分類框架 |
| 原始資料 | `Raw/` → `processed/` | ✅ 每日整理流程 |
| 摘要產生 | `daily_organizer.py` | ✅ 自動摘要 |

### 2.2 知識庫管理
| 功能 | 現況 | 評估 |
|------|------|------|
| 概念筆記 | `Sumo_wiki/concepts/` | ✅ 概念驅動 |
| 摘要筆記 | `Sumo_wiki/summaries/` | ✅ 檔案摘要 |
| 反向連結 | `Sumo_wiki/backlinks/` | ✅ 關聯追蹤 |
| 矛盾偵測 | `contradiction_detector.py` | ✅ Lint 功能 |
| 健康檢查 | `health_check_v3.py` | ✅ 完整檢測 |

### 2.3 搜尋和檢索
| 功能 | 現況 | 評估 |
|------|------|------|
| 雙索引搜尋 | `dual_index_search.py` | ✅ LanceDB + 關鍵字 |
| 引用追蹤 | `citation_tracker.py` | ✅ |
| 查詢介面 | `query_interface.py` | ✅ |

### 現有缺口分析
| 缺口 | 影響 |
|------|------|
| ❌ 無主動式監控 | 研究是被動的，不會自動追蹤感興趣的主題 |
| ❌ 無變化偵測 | 無法自動識別資訊的改變 |
| ❌ 無定時摘要推送 | 需要手動查詢，沒有主動通知 |
| ❌ 主題管理分散 | 研究主題沒有統一的管理機制 |

---

## 三、整合方案

### 3.1 整合架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                    attention-research                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Cron 排程    │  │ 主題監控     │  │ 變化偵測引擎        │ │
│  │ (早+晚)      │→ │ (META.json)  │→ │ (Signal Detection)  │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│         ↓                ↓                   ↓              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              Structure Digest Output                    ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    SumoNoteBook                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ research/   │  │ Sumo_wiki/  │  │ 通知系統            │  │
│  │ (研究報告)   │  │ (知識庫)     │  │ (Telegram)          │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 具體功能規劃

#### 功能一：主題監控中心（Topic Monitor）
```
位置：SumoNoteBook/topic-monitor/
├── topics/
│   ├── ai/
│   │   ├── META.json        # 監控狀態
│   │   ├── config.yaml      # 監控設定
│   │   └── digest/          # 每日摘要
│   ├── tech-trends/
│   └── finance-markets/
└── config.yaml              # 全域設定
```

**META.json 結構**：
```json
{
  "topic": "ai",
  "lastMorningUpdate": "2026-04-22T08:00:00",
  "lastAfternoonUpdate": "2026-04-22T15:00:00",
  "alertThreshold": "major_development",
  "status": "active"
}
```

#### 功能二：變化偵測系統（Change Detection）
- 每日比對新資訊與歷史資料
- 識別「新增」、「刪除」、「修改」的信號
- 輸出變化報告到 `Raw/changes/`

#### 功能三：結構化摘要產生器
- 沿用 attention-research 的 Digest Format
- 輸出到 `research/` 目錄
- 自動更新研究索引

#### 功能四：主動通知整合
- 整合現有 Telegram 通知
- 異常變化即時推播
- 每日摘要定時發送

---

## 四、實作優先順序

### P0 - 最高優先（立即可做）

| 順序 | 功能 | 說明 | 預期效益 |
|------|------|------|----------|
| 1 | **主題設定系統** | 在 SumoNoteBook 建立 `topic-monitor/` 目錄結構 | 統一管理研究主題 |
| 2 | **Cron 排程整合** | 借用 daily_organizer.py 的排程經驗，新增晨間/午間研究任務 | 自動化情報收集 |
| 3 | **Digest Format 採用** | 將 attention-research 的摘要格式引進 SumoNoteBook | 標準化研究輸出 |

### P1 - 高優先（1-2週內）

| 順序 | 功能 | 說明 | 預期效益 |
|------|------|------|----------|
| 4 | **變化偵測腳本** | 基於 `contradiction_detector.py` 延伸，開發 `change_detector.py` | 及時發現資訊變化 |
| 5 | **Alert Threshold 系統** | 設定關鍵事件的觸發條件，達標即通知 | 重點事件不漏接 |
| 6 | **研究索引自動更新** | 研究報告產生後自動更新 `research_index.md` | 減少手動維護 |

### P2 - 中優先（1個月內）

| 順序 | 功能 | 說明 | 預期效益 |
|------|------|------|----------|
| 7 | **雙語言支援** | 英文研究自動翻譯為中文（整合現有 AutoTranslator） | 擴大適用範圍 |
| 8 | **多 Agent 協作** | 讓工程師蘇茉负责技術研究、律師蘇茉负责法規監控 | 分工專業化 |
| 9 | **視覺化儀表板** | 參考 `dashboard.html`，加入主題監控狀態 | 一目了然 |

---

## 五、具體實作建議

### 5.1 第一階段：直接借用 attention-research

**立即行動**：將 attention-research 安裝為 SumoNoteBook 的技能

```bash
# 建議安裝位置
~/.openclaw/skills/attention-research/

# 配置研究根目錄指向 SumoNoteBook
~/.openclaw/workspace/docs/research → C:\butler_sumo\library\SumoNoteBook\research\
```

**優點**：
- 最小改动，立即可用
- 保持兩個系統的独立性和靈活性

### 5.2 第二階段：深度整合

**長期目標**：將 attention-research 的核心概念內化到 SumoNoteBook

1. **採用 Prompt Stack Order**：
   - CORE: SumoNoteBook 的 SOUL.md / MEMORY.md
   - TOPICS: 每個蘇茉的專業領域（engineer/lawyer/professor）
   - TEMPLATES: 統一的 Digest Format

2. **建立 Topic Monitor 資料夾**：
   ```
   SumoNoteBook/topic-monitor/
   ├── ai/META.json, config.yaml, digest/
   ├── tech-trends/
   ├── finance-markets/
   └── config.yaml (全域設定)
   ```

3. **開發 SumoNoteBook 版本的 Daily Research Script**：
   - 基於 `daily_organizer.py` 經驗
   - 加入早晨/下午兩個時間點
   - 輸出統一 Digest 格式

### 5.3 技術參考

| attention-research 組件 | SumoNoteBook 對應/改編 |
|--------------------------|----------------------|
| `PROMPTS/TOPICS/<topic>.md` | `topic-monitor/<topic>/config.yaml` |
| `META.json` freshness gate | `scripts/daily_organizer.py` 的 processed 機制 |
| `TEMPLATES/morning-research.md` | 新增 `scripts/morning_research.py` |
| `signal-rules.md` | `scripts/contradiction_detector.py` 延伸 |
| `digest-format.md` | `Schema/research_index.md` 整合 |

---

## 六、風險與注意事項

### 6.1 整合風險
| 風險 | 應對 |
|------|------|
| 雙系統維護負擔 | 優先採用「借用」而非「複製」策略 |
| 研究資源重複 | 統一研究根目錄，避免資料分散 |
| 通知過載 | 設定 Alert Threshold，只在關鍵時刻通知 |

### 6.2 建議先用後整合
1. 先將 attention-research 當作外部技能使用
2. 觀察一個月，評估是否完全內化
3. 根據實際使用情況，選擇性移植功能

---

## 七、結論

**核心價值**：attention-research 為 SumoNoteBook 帶來「主動式智慧監控」能力

| 對比 | SumoNoteBook（目前） | 整合後 |
|------|---------------------|--------|
| 研究觸發 | 被動（手動查詢） | 主動（定時監控） |
| 變化偵測 | 需人工比對 | 自動偵測並通知 |
| 摘要輸出 | 檔案摘要 | 結構化 Digest |
| 系統整合 | 獨立運作 | 蘇茉家族協同 |

**推薦策略**：「借用 + 逐步內化」
- 短期：直接使用 attention-research 作為技能
- 中期：將核心功能移植到 SumoNoteBook 原生
- 長期：建立統一的蘇茉家族研究管道

---

*報告完成*
**研究者**：教授蘇茉  
**完成時間**：2026-04-22 15:49 GMT+8