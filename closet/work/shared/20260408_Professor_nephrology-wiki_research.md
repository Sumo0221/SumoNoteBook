# 研究報告：nephrology-wiki（腎臟科 EBM 知識庫）分析

**研究日期：** 2026-04-08
**研究者：** 教授蘇茉
**來源：** https://github.com/copper0722/nephrology-wiki
**作者：** 王介立 醫師（腎臟專科，柏安透析中心）

---

## 1. 知識庫結構與格式

### 檔案架構
```
nephrology-wiki/
├── README.md
└── wiki/
    ├── wiki_nephrology_*.md       # 腎臟科各主題
    ├── wiki_cardiology_*.md        # 心臟科
    ├── wiki_endocrinology_*.md     # 內分泌
    ├── wiki_pharmacology_*.md      # 藥理
    ├── wiki_research_methods_ebm.md  # EBM 方法論
    └── ...
```

### 主題分類（共 12+ 個腎臟相關主題）
| 主題 | 檔案 |
|------|------|
| CKD 分期/流行病學/進展 | wiki_nephrology_ckd_part1.md |
| CKD 管理/保守治療/移植 | wiki_nephrology_ckd_part2.md |
| CKD 共病/心血管/骨代謝 | wiki_nephrology_ckd_part3.md |
| CKD 最新試驗/指引/生物標記 | wiki_nephrology_ckd_part4.md |
| 血液透析 | wiki_nephrology_dialysis_hd.md |
| 腹膜透析 | wiki_nephrology_dialysis_pd.md |
| AKI | wiki_nephrology_aki.md |
| 腎性貧血 | wiki_nephrology_anemia.md |
| 電解質與 CKD-MBD | wiki_nephrology_electrolytes.md |
| 高血壓與 CKD | wiki_nephrology_hypertension.md |
| CKD 減重 | wiki_ckd_obesity_weight_management.md |
| 考試範圍/缺口分析 | wiki_tsn_board_exam.md |

---

## 2. EBM 格式設計（核心價值）

### 每份文件的 Markdown Frontmatter
```yaml
---
type: wiki
topic: Nephrology Anemia
sources:
  - "10.7326/0003-4819-72-4-579"
  - "10.1016/j.kint.2023.02.019"
  - ...
paper_count: 8
generated: 2026-04-05
---
```

### 每篇文獻的結構化格式
每篇文獻都以下列格式組織：

```
## [文獻標題]
DOI: 10.xxxx/xxxxx
Design: [研究設計類型]
Key: [核心發現/臨床要點]
Clinical: [臨床應用價值]
Numbers: [關鍵數據（HR/CI/NNT 等）]
```

**Example（腎性貧血文獻）：**
```
## ASCEND-NHQ: Daprodustat in Non-Dialysis CKD Anemia (2023)
DOI: 10.1016/j.kint.2023.02.019
Design: Phase 3 RCT, 28-week double-blind, placebo-controlled
Key: HIF-PHI daprodustat achieves target Hb 11-12 g/dL and improves fatigue/QoL in non-dialysis CKD vs placebo.
Clinical: Oral HIF-PHI alternative to ESA; addresses HRQoL endpoints beyond hemoglobin correction in CKD anemia.
Numbers: Daprodustat groups sustained Hb 11-12 g/dL; superior fatigue/function scores vs placebo; 142 centers, 14 countries.
```

### EBM 方法論文件（wiki_research_methods_ebm.md）
包含完整的：
- **研究設計層級**：SR/MA > RCT > 前瞻性世代 > 回溯性世代 > 病例對照 > 横斷面 > 病例系列 > 專家意見
- **偏移分類**：選擇偏移、資訊偏移、混雜因子
- **統計指標**：OR、RR、HR、ARR、NNT/NNH、95% CI 判讀
- **SR/MA 方法學**
- **p-value 與信賴區間的正確解讀**

---

## 3. 與 SumoNoteBook 的比較

| 維度 | nephrology-wiki | SumoNoteBook |
|------|-----------------|--------------|
| **定位** | 單一專科 EBM 知識庫（腎臟科） | 多領域知識管理系統 |
| **內容格式** | 高度結構化的 EBM 格式（DOI/Design/Key/Clinical/Numbers） | 自由格式 Markdown，learning 目錄有分類 |
| **來源引用** | 完整 PMID/DOI 引用，每個 claim 皆可溯源 | 目前無強制引用格式 |
| **EBM 分級** | GRADE、NNT/ARR 等完整統計呈現 | 無內建 EBM 格式 |
| **維護方式** | LLM 維護，定期更新文獻 | 蘇茉家族成員協作維護 |
| **目標讀者** | 腎臟專科醫師考試準備 | 蘇茉家族內部知識沉澱 |
| **缺口追蹤** | 有（🔴缺/🟡薄弱 標記） | 無 |
| **License** | CC BY-NC-SA 4.0 | 無明確 License |

---

## 4. 值得蘇茉家族借鑒之處

### ✅ 值得借鑒的設計

**1. Frontmatter 結構化**
在文件頂部加入標準化的 frontmatter，包含：
- `type`：文件類型
- `topic`：主題
- `sources`：DOI 列表
- `paper_count`：文獻數量
- `generated`：生成日期

**→ 可應用於 SumoNoteBook 的 shared/ 知識沉澱文件**

**2. 每篇文獻的標準欄位**
固定五個欄位：Design、Key、Clinical、Numbers，讓 LLM 閱讀文獻後能快速產出結構化摘要。

**→ 可做為 SumoNoteBook 「文獻閱讀模板」**

**3. 缺口追蹤機制**
用 🔴🟡🟢 標記知識缺口，清楚知道哪裡還沒補齊。

**→ 可應用於蘇茉家族的研究項目追蹤**

**4. EBM 方法論作為 CC agents 的 reference**
所有 wiki 文章都引用同一個 EBM 方法文件，確保證據品質一致性。

**→ 可建立 SumoNoteBook 的「蘇茉家族研究方法標準」文件**

**5. 跨文件交叉引用**
```markdown
## Cross-references (FB posts)
- [wiki fb nephrology dialysis](/proj/wiki/wiki_fb_nephrology_dialysis.md)
```

**→ 可在 SumoNoteBook 建立「相關主題連結」慣例**

### ⚠️ 無需借鑒之處

- **考試題庫導向**：nephrology-wiki 針對腎臟專科考試，蘇茉家族不需要這種格式
- **引用付費文獻的處理**：DM 機制不適用於蘇茉家族場景

---

## 5. 建議的具體應用

### 短期（可立即實施）
1. **建立「蘇茉家族研究方法標準」文件**，放在 `SumoNoteBook/raw/shared/`
2. **制定「知識沉澱模板」**，包含 frontmatter + 結構化欄位

### 中期
1. **為重要研究主題建立 EBM 格式的文獻摘要**
2. **建立缺口追蹤系統**，標記待研究項目

---

## 6. 總結

nephrology-wiki 是一個非常出色的**領域專科 EBM 知識庫**範例。其核心價值在於：
- ✅ 完整的 DOI/PMID 引用鏈
- ✅ 標準化的 EBM 結構化格式
- ✅ LLM 可讀、可維護
- ✅ 缺口透明、持續迭代

蘇茉家族可以借鑒其**結構化格式**和**來源引用**的設計，提升 SumoNoteBook 的知識品質與可用性。

---
*報告完成時間：2026-04-08 11:40 GMT+8*
