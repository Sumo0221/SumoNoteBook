# MindForge × SumoFamily 深度研究報告

> 日期：2026-04-15
> 研究者：教授蘇茉（ProfessorSuMo）
> 任務：深度研究 MindForge 並提出借鏡方案

---

## 📝 MindForge 核心概念

### 1. Knowledge Acquisition Loop（KAL）

MindForge 的核心創新是**讓 AI 自己判斷「學夠了沒有」**。

```
傳統 RAG：你餵文件 → 它回答
MindForge KAL：
  你丟 URL/關鍵字 → 系統啟動學習循環
    → 搜尋相關文件 → 擷取蒸餾
    → 自我反問：「我能解釋這個東西了嗎？」
    → 能 → 通知你「學完了，可以問我了」
    → 不能 → 針對答不出的問題再搜尋 → 再蒸餾 → 再反問
    → 重複直到通過或達到上限
```

### 2. Principle 0：「知道自己不知道」優先於「零幻覺」

- 答不出來就說答不出來，**絕對不編**
- 每句話都掛 source citation，點得到原文
- 這是**個人知識場景的核心原則**

### 3. 三層知識組織

| 層次 | MindForge | SumoNoteBook 現況 |
|------|-----------|------------------|
| **Raw** | 原文 | `Raw/` ✅ |
| **Wiki** | LLM 維護的結構化知識 | `Sumo_wiki/` ✅ |
| **Schema** | 人類控制的組織規則 | `docs/SCHEMA.md` ✅ |

> 📌 **SumoNoteBook 已經有對應的三層架構！** 只是命名和實作細節不同。

### 4. 蒸餾流程

從多個來源文件中**蒸餾出原子主張**（atomic claims），再進行自問自答驗證。

---

## 🔍 SumoMemory 借鏡點

### 現況分析

```
目前結構：
memories/     → 純 JSON（id, content, keywords, entities, timestamp, source）
entities/    → 純 Markdown 卡片（無結構化屬性）
```

**問題：**
- 無引用機制（citation）
- 無知識層級區分（Raw/Wiki/Schema）
- 無自我學習判斷
- 無矛盾偵測

### 借鏡方案

#### 🔴 P0 - 最高優先：Principle 0 引入

```
新增規則：
- 每則記憶必附 source（URL、對話來源、人工記錄）
- 無 source 的資訊明確標記為「未經驗證」
- 回答問題時，優先說「我不知道」而非編造
```

**實作方式：**
```python
# 在 SumoMemory 記憶格式中新增必填欄位
{
  "id": "mem_xxx",
  "content": "...",
  "source": "https://...",  # 必填
  "source_type": "url|chat|manual",  # 必填
  "confidence": "high|medium|low|unverified",  # 必填
  "verification_status": "verified|pending|disputed"
}
```

#### 🟡 P1 - 高優先：三層知識組織

| 層次 | SumoMemory 新結構 |
|------|------------------|
| **Raw** | `raw/` - 未處理的原始記憶 |
| **Wiki** | `memories/` - LLM 整理後的結構化記憶 |
| **Schema** | `schema/` - 組織規則元資料 |

**實作方式：**
```python
# 遷移腳本：將現有 JSON 分類到三層
# high confidence + 有 source → memories/ (Wiki)
# unverified / low confidence → raw/ (Raw)
# 建立 schema/rules.md 定義組織邏輯
```

#### 🟡 P1 - 高優先：KAL 概念引入（雛型）

```
自我學習迴圈（雛型版）：
1. 新記憶攝入時，LLM 自問：「這則資訊是否與現有記憶衝突？」
2. 若衝突，標記為 "disputed"，通知管理者
3. 若順暢，整合進現有記憶網絡
```

**實作方式：**
```python
# 在 ingest 時呼叫矛盾偵測
def ingest_memory(memory):
    conflicts = detect_conflicts(memory)
    if conflicts:
        memory["verification_status"] = "disputed"
        memory["conflicts_with"] = conflicts
        notify_admin(f"新記憶與現有記憶衝突：{conflicts}")
    else:
        memory["verification_status"] = "verified"
    store(memory)
```

---

## 🔍 SumoNoteBook 借鏡點

### 現況分析

```
已有：
✅ 三層結構（Raw / Sumo_wiki / Schema）
✅ Wiki 概念/摘要分類
✅ 健康檢查（Lint）
✅ 內部連結語法

缺少：
❌ KAL（自我學習迴圈）
❌ Citation 引用追蹤
❌ 自問自答驗證機制
❌ 矛盾偵測整合
❌ Precision-first 明確宣告
```

### 借鏡方案

#### 🔴 P0 - 最高優先：新增 Citation 追蹤

```
MindForge 的 citation 是核心！
每個 Wiki 頁面都必須標明：
- 資訊來源（哪些 Raw 文件蒸餾而來）
- 信心等級（蒸餾時的置信度）
- 驗證狀態（已驗證/待驗證）
```

**實作方式：**
```markdown
<!-- 蒸餾頁面抬頭 -->
# 頁面標題

> Source: [[Raw/原始檔案]]
> Confidence: high
> Verified: 2026-04-15 by SumoMemory

## 內容...
```

#### 🔴 P0 - 最高優先：Wiki Lint 升級 - 矛盾偵測

MindForge 的健康檢查不只查斷裂連結，還要**偵測矛盾**。

```python
# health_check_v3.py 新增功能：
def detect_contradictions():
    """偵測 Wiki 中互相矛盾的聲明"""
    claims = extract_all_claims()
    # NLP 相似度比對
    # 找出主題相同但結論相反的聲明
    return contradictions
```

#### 🟡 P1 - 高優先：KAL 自問自答機制（新增 Ingest 流程）

```
攝入流程升級：
1. Ingest 原始文件
2. 蒸餾原子主張（atomic claims）
3. 自問自答驗證：
   - 「我能用一句話解釋這個嗎？」
   - 「這與現有 Wiki 衝突嗎？」
   - 「我對這個主題還有哪些未知？」
4. 通過 → 寫入 Wiki
5. 未通過 → 回頭搜尋更多來源（模擬 MindForge Round 2）
```

**實作方式：**
```python
# ingest_notebook.mjs 升級：
async function kal_ingest(source):
    claims = distill(source)
    questions = generate_self_check_questions(claims)
    answers = await self_answer(questions)
    passed = evaluate_answers(answers)
    
    if not passed:
        more_sources = await search_additional_sources(questions)
        # 回到步驟 2 重新蒸餾
        return kal_ingest(more_sources)
    
    await write_to_wiki(claims)
    await update_citations(source, claims)
```

#### 🟢 P2 - 中優先：Precision-first 明確宣告

在 `Sumo_wiki/SOUL.md` 或 `Wiki/SOUL.md` 中新增：

```markdown
## Principle 0：知道自己不知道

> 「說錯比少說嚴重。」
> 
> 在 SumoNoteBook，每則知識都必須：
> 1. 可溯源（附 citation）
> 2. 精準優先（寧缺毋濫）
> 3. 不確定就說不確定
```

---

## 📊 優先順序建議

### SumoMemory

| 優先順序 | 項目 | 說明 |
|---------|------|------|
| 🔴 P0 | Principle 0 引入 | source/citation/confidence 必填 |
| 🟡 P1 | 三層資料夾 | raw/memories/schema 分類 |
| 🟡 P1 | 矛盾偵測雛型 | ingest 時檢查衝突 |
| 🟢 P2 | KAL 雛型 | 自問自答驗證 |

### SumoNoteBook

| 優先順序 | 項目 | 說明 |
|---------|------|------|
| 🔴 P0 | Citation 追蹤 | 每頁必附來源 |
| 🔴 P0 | Lint 矛盾偵測 | health_check 升級 |
| 🟡 P1 | KAL Ingest 流程 | 自問自答驗證機制 |
| 🟢 P2 | Principle 0 SOUL | 明確宣告精準優先原則 |

---

## 💡 實作方式總覽

### 短期（1-2 週）：制度建立
- [ ] SumoMemory 記憶格式新增必填欄位（source, confidence）
- [ ] SumoNoteBook Wiki 頁面新增 Citation 抬頭
- [ ] Wiki/SOUL.md 新增 Principle 0 宣告

### 中期（1 個月）：功能實作
- [ ] SumoMemory 三層資料夾遷移腳本
- [ ] SumoMemory 矛盾偵測（ingest hook）
- [ ] SumoNoteBook Lint 矛盾偵測升級

### 長期（2-3 個月）：KAL 系統
- [ ] SumoNoteBook KAL Ingest 流程
- [ ] SumoMemory KAL 自問自答驗證
- [ ] 整合蒸餾腳本自動化

---

## 🔗 與現有蘇茉家族系統的整合

| MindForge 元件 | 蘇茉家族對應 | 借鏡方式 |
|---------------|------------|---------|
| KAL | `/notebook-rag` + 健康檢查 | 強化為閉環學習 |
| 三層儲存 | MemPalace V2 | 對齊 MindForge 命名 |
| Citation | Wiki 內部連結 | 強化為外部可追蹤 |
| 矛盾偵測 | Lint 腳本 | 升級 NLP 分析 |
| Precision-first | 批判性反思技能 | 明確寫入 SOUL |

---

## 📚 靈活借鑑

MindForge 的設計啟示：
1. **制度勝於功能** - Principle 0 是文化，不是程式碼
2. **閉環學習** - KAL 的自問自答是關鍵，不是 vector search
3. **精準優先** - 個人知識不需要多，需要對

蘇茉家族不需要複製 MindForge 的 PostgreSQL + pgvector 架構，而是要引進**它的學習紀律和知識品質觀念**。

---

*研究者：教授蘇茉（ProfessorSuMo）*
*研究完成：2026-04-15 23:50*
