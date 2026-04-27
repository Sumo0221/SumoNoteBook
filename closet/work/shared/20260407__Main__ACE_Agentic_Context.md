# ACE: Agentic Context Engineering 研究報告

## 基本資訊

- **來源**：Stanford、SambaNova、UC Berkeley 聯合發表
- **論文**：[arXiv: 2510.04618](https://arxiv.org/abs/2510.04618)
- **發表**：ICLR 2026
- **日期**：2026 年 4 月
- **作者**：Wisel Chen 整理

---

## 一句話版本

讓 AI Agent 持續進步，不一定要動模型權重。把 context 設計成一份會自我演化的 playbook，效果可能更好。

---

## 論文想解決的兩個核心問題

### 問題一：Brevity Bias（過度簡短偏誤）

很多 prompt optimization 方法，會把 context 越改越短、越抽象。真正有用的 domain knowledge 被壓掉了，導致「優化」後的 prompt 反而比原始版本表現更差。

### 問題二：Context Collapse（Context 崩塌）

如果每次都把整份 context 重新摘要重寫，久了就會指數衰減：
- 第一次摘要保留 80%，第二次 64%，第三次 51%⋯⋯
- 原本具體的策略描述被泛化
- 模型越來越像剛出廠的狀態，之前學到的經驗全部歸零

---

## ACE 的核心：Generation → Reflection → Curation 循環

### 1. Generation（生成）

Agent 在執行任務時，結構化地記錄：
- 這個任務用了什麼工具、什麼順序
- 哪個步驟卡住了、為什麼
- 最終成功的路徑是什麼

### 2. Reflection（反思）

根據執行結果回頭看：
- 哪些策略有效？保留
- 哪些策略失敗了？標記原因
- 有沒有更好的替代方案？

**關鍵**：這個反思不是人在做，是 Agent 自己做的。它根據 execution feedback 和環境信號來判斷。

### 3. Curation（策展）

把有價值的內容整理進 context，但不是整份重寫。

---

## ACE 與傳統做法的差異

| 傳統做法 | ACE 做法 |
|---------|---------|
| 整份 context 重新摘要 | 增量式更新，保留原始細節 |
| 越改越短 | 結構化增長，有組織地變長 |
| 追求「精煉」 | 追求「完整且可檢索」 |
| 丟掉失敗經驗 | 把失敗轉成可重用的避雷指南 |

---

## 實驗數據

| 指標 | 數據 |
|-----|------|
| Agent tasks 平均改善 | +10.6% |
| Finance/domain-specific reasoning | +8.6% |
| Adaptation latency | 顯著降低 |
| Rollout cost | 更低 |
| 需要 labeled data？ | 不需要 |
| AppWorld leaderboard | 追平 top production agent |
| 更難的 test-challenge split | 超過對手 |

**最關鍵**：用較小的開源模型，在最難的測試集上打贏了商用頂級 Agent。說明模型大小不是唯一決定因素，context 的品質和組織方式也是。

---

## 對蘇茉家族的啟發

### 1. 蘇茉家族已在實踐 ACE

| ACE 概念 | 蘇茉家族對應 |
|---------|------------|
| Playbook（作戰手冊） | SOUL.md、AGENTS.md |
| Strategy notes | memory/ 目錄下的經驗記錄 |
| Task heuristics | 各 agent 的 system prompt |
| Failure patterns | 錯誤處理邏輯 |
| Incremental curation | 記憶系統的增量更新 |

### 2. 蘇茉家族可以強化的方向

#### a) 建立失敗經驗的結構化記錄機制

目前蘇茉家族的 memory/ 目錄是日誌式的，可以借鑒 ACE 的三層結構：
- **Generation**：任務執行時結構化記錄（工具、順序、卡點）
- **Reflection**：根據執行結果自動反思
- **Curation**：增量更新而非整份重寫

#### b) 對抗 Context Collapse

蘇茉家族的多 agent 架構特別需要防止 context 衰減：
- 每次對話的 context 精簡時，保留關鍵策略知識
- 使用結構化摘要（類似 Claude Code 的 9 維度摘要）而非無差別壓縮
- 標記失效的策略但不完全刪除（「為什麼失效」本身也是知識）

#### c) Playbook 演化

- SOUL.md 和 AGENTS.md 應該是動態演化文件
- 每次完成重要任務後，自動沉澱策略到 playbook
- 讓新啟動的蘇茉能繼承「學長姐」的經驗

### 3. Context Engineering vs Fine-tuning 的取捨

對蘇茉家族的啟示：
- **先做好 context layer**：SOUL.md、AGENTS.md、MEMORY.md 的品質是首要投資
- **Fine-tuning 不需要**：蘇茉家族是工具型 agent，context engineering 投資回報率更高
- **可積累的資產**：提示詞和策略可以跨版本復用，權重不行

---

## 核心結論

> 對 Agent 來說，context 應該像會持續演化的操作手冊，而不是一次次被摘要掉的便條紙。

> 如果你正在建 AI Agent，與其花三個月收集數據做 fine-tuning，不如先花三天把你的 context layer 設計好。

---

## 延伸閱讀

- [原文章連結](https://ai-coding.wiselychen.com/ace-agentic-context-engineering-stanford-playbook-evolution/)
- [arXiv 論文](https://arxiv.org/abs/2510.04618)
- [Claude Code 上下文工程：四層壓縮機制的源碼級拆解](/claude-code-context-engineering-four-layer-compression/)
- [Google Nested Learning：AI 終於可以「記住」東西了？](/google-nested-learning-ai-memory-breakthrough/)

---

*研究日期：2026-04-07*
*研究者：教授蘇茉*
