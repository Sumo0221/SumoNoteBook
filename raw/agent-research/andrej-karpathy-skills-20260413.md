# Andrej Karpathy's LLM Coding Pitfalls & Skills

> 來源：GitHub - forrestchang/andrej-karpathy-skills
> 日期：2026-04-13
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 概述

一個 CLAUDE.md 檔案，基於 Andrej Karpathy 對 LLM 編碼陷阱的觀察，專門用來改善 Claude Code 的行為。

---

## 🎯 Karpathy 指出的 LLM 問題

> "The models make wrong assumptions on your behalf and just run along with them without checking. They don't manage their confusion, don't seek clarifications, don't surface inconsistencies, don't present tradeoffs, don't push back when they should."

> "They really like to overcomplicate code and APIs, bloat abstractions, don't clean up dead code..."

---

## 📋 四大原則

| 原則 | 針對問題 |
|------|----------|
| **Think Before Coding** | 錯誤假設、隱藏困惑、忽略取捨 |
| **Simplicity First** | 過度複雜、膨脹抽象 |
| **Surgical Changes** | 正交編輯、觸碰不該動的程式碼 |
| **Goal-Driven Execution** | 透過測試優先、可驗證的成功標準 |

---

## 🧠 Think Before Coding

**核心**：不要假設。遇到困惑要說出來。

| 行為 | 應該 |
|------|------|
| 遇到不確定 | 先問清楚再猜 |
| 有多種解釋 | 不要默默選一個 |
| 有更簡單的方案 | 說出來 |
| 遇到困惑 | 說出不清楚的地方並尋求澄清 |

---

## ✂️ Simplicity First

**核心**：最小程式碼解決問題。沒有投機的東西。

| 不要 | 要 |
|------|------|
| 加入沒被要求的功能 | 只做被要求的事 |
| 為單次使用的程式碼建立抽象 | 沒有就不要做 |
| 加入沒被要求的「彈性」| 沒有就不要做 |
| 為不可能的場景處理錯誤 | 只處理可能發生的 |

**測試**：如果資深工程師說這太複雜了，那就簡化。

---

## 🔪 Surgical Changes

**核心**：只碰要碰的。清理自己造成的髒亂。

| 情況 | 怎麼做 |
|------|----------|
| 編輯現有程式碼 | 不要「改進」旁邊的程式碼、註解或格式 |
| 不要重構壞掉的東西 | 只改任務需要的 |
| 匹配現有風格 | 即使你會用不同方式 |
| 注意到無關的死亡程式碼 | 提到它 — 不要刪除 |

**只移除你的變更造成的 orphan**：不要刪除原本就存在的死亡程式碼（除非被要求）。

---

## 🎯 Goal-Driven Execution

**核心**：定義成功標準。迴圈直到驗證。

| Instead of... | Transform to... |
|---------------|------------------|
| "Add validation" | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug" | "Write a test that reproduces it, then make it pass" |
| "Refactor X" | "Ensure tests pass before and after" |

**多步驟任務**：陳述簡短計劃：
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

---

## 💡 蘇茉觀察

這個 CLAUDE.md 檔案可以幫助蘇茉：

1. **避免過度複雜化** - 不要加入沒被要求的功能
2. **先問清楚再動** - 遇到困惑時主動尋求澄清
3. **保持簡單** - 如果 200 行可以變成 50 行，就簡化
4. **精準改動** - 只改需要改的，不要順便重構其他東西

---

## 📦 安裝方式

### Option A：Claude Code Plugin（推薦）
```bash
/plugin marketplace add forrestchang/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills
```

### Option B：CLAUDE.md（每專案）
```bash
curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md
```

---

## 🔗 連結

- GitHub：https://github.com/forrestchang/andrej-karpathy-skills
- Karpathy 原文：https://x.com/karpathy/status/2015883857489522876

---

*最後更新：2026-04-13*