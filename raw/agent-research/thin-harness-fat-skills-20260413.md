# Thin Harness, Fat Skills：Garry Tan 的 AI 架構筆記

> 來源：Facebook - 張維峰 分享
> 日期：2026-04-12
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 概述

Garry Tan（Y Combinator 總裁）分享的 AI 架構筆記。核心概念：**同樣的 AI 模型，有人用出 100 倍、有人只有 2 倍。差別不在模型，在架構。**

---

## 🎯 核心命題

> Steve Yegge says: people using AI coding agents are **10x to 100x as productive** as engineers using Cursor and chat today.
>
> 這是真的數字。但當人們聽到這個數字時，他們會去找錯誤的解釋——更好的模型、更聰明的 Claude、更多的參數。
>
> 然而，那些只做到 2 倍效率和做到 100 倍效率的人，用的是**同一個模型**。
>
> **差別不在智力，而在架構。**

---

## 📊 五個定義

### 1. Skill Files（技能檔案）

Skill file 是一份可重複使用的 markdown 文件，教模型「怎麼做」某件事。不是「做什麼」，那由使用者決定。Skill file 提供的是流程。

**核心洞察**：Skill file 的運作方式就像一個**函式呼叫**。它接受參數，你用不同的引數來呼叫它。同一套流程根據你傳入的不同內容，可以產生截然不同的能力。

```
同一個 skill，同樣七個步驟，同一個 markdown 檔案。
Skill 描述的是一套判斷的流程，呼叫的時候才賦予它真實的世界。
```

---

### 2. Harness（駭馭工程）

Harness 是運行 LLM 的程式。它只做四件事：
- 在迴圈中執行模型
- 讀寫你的檔案
- 管理上下文
- 強制執行安全規則

**反面模式**：Fat harness with thin skills
- 40 多個工具定義吃掉一半的 context window
- 萬能型的 God-tools，每次 MCP 來回要 2 到 5 秒
- REST API wrapper 把每個 endpoint 都變成一個獨立工具

**結果**：三倍的 token 消耗、三倍的延遲、三倍的失敗率。

---

### 3. Resolvers（解析器/路由器）

Resolver 是上下文的路由表。當任務類型 X 出現時，先載入文件 Y。

Skills 告訴模型「怎麼做」。Resolvers 告訴模型「載入什麼、什麼時候載入」。

**Claude Code 的 resolver**：每個 skill 都有一個 description 欄位，模型會自動將使用者意圖與 skill 描述配對。你不需要記住指令存在，Description 本身就是 resolver。

---

### 4. Latent vs. Deterministic（潛在空間 vs. 確定性運算）

| 類型 | 說明 | 例子 |
|------|------|------|
| **Latent** | 智力所在，模型閱讀、詮釋、決策 | 判斷、綜合、模式識別 |
| **Deterministic** | 信任所在，同樣輸入同樣輸出 | SQL 查詢、編譯後的程式碼、算術運算 |

**核心原則**：搞清楚哪些任務該讓 AI 判斷，哪些該用傳統程式。搞混這兩者是 agent 設計中最常見的錯誤。

---

### 5. Diarization（結構化摘要）

讓 AI 真正能用於知識工作的那一步。模型閱讀關於某個主題的所有資料，然後寫出一份結構化的 profile，從幾十或幾百份文件中，蒸餾出的一頁判斷摘要。

**這不是 SQL 查詢能產出的東西，也不是 RAG pipeline 能產出的。** 模型必須真正去閱讀、在腦中同時持有矛盾之處、注意到什麼在什麼時候改變了，然後綜合成結構化的情報。

---

## 🏗️ 三層架構

```
┌─────────────────────────────────────┐
│  Fat Skills（最上層）               │ ← 90% 的價值在這裡
│  Markdown 格式的流程、判斷、領域知識 │
├─────────────────────────────────────┤
│  Thin Harness（中層）               │ ← ~200 行程式碼
│  JSON 輸入，文字輸出，預設唯讀      │
├─────────────────────────────────────┤
│  你的應用在最底層                   │ ← 確定性基礎層
│  QueryDB、ReadDoc、Search、Timeline │
└─────────────────────────────────────┘
```

**原則**：把智力往上推進 skills，把執行往下推進確定性的工具。保持 harness 精簡。

---

## 🔄 會學習的系統

```
活動結束後 → /improve skill → 分析回饋 → 提取模式 → 回寫到 skill file
                                                    ↓
下一次執行自動使用新規則，skill 自己改寫了自己！
```

---

## 📝 Garry Tan 的指令

> 「你不准做一次性的工作。如果我叫你做一件事，而且它是那種、以後還會再做的事，你必須：
> 1. 先手動做 3 到 10 個項目
> 2. 給我看結果
> 3. 如果我批准，就把它寫成一個 skill file
> 4. 如果它應該自動執行，就放上 cron」

**測試標準**：如果我需要同一件事跟你說兩次，就是你的失敗。

---

## 💡 對蘇茉家族的對照

| Garry Tan 的概念 | 蘇茉家族 |
|-----------------|----------|
| **Thin Harness** | OpenClaw 層（精簡）|
| **Fat Skills** | 各專業蘇茉的技能檔案 |
| **Resolver** | 總管蘇茉的角色（協調分配）|
| **Latent vs. Deterministic** | 蘇茉思考 vs. 工具執行 |
| **會學習的系統** | SumoMemory Brain-Agent Loop |
| **Skill as Method Call** | 蘇茉的任務派發系統 |

---

*最後更新：2026-04-13*
