# Schema - 人類控制層

**此層級由人類定義，LLM 可讀不可寫**

## MOC.md - 總體架構

```
SumoNoteBook
├── Raw/          # 原始來源（嚴禁 LLM 覆寫）
│   ├── sources/   # 原始網頁、文章
│   └── raw_notes/# 老爺或蘇茉直接寫入的原始筆記
├── Wiki/         # LLM 整理層（自動維護）
│   ├── concepts/# 概念頁（由 LLM 生成並持續更新）
│   └── summaries/# 摘要頁（由 LLM 蒸餾產生）
└── Schema/      # 人類控制層（LLM 可讀不可寫）
    ├── MOC.md           # 總體架構（本文）
    ├── research_index.md # 研究分類框架
    └── custom_taxonomy.md# 標籤體系
```

## 層級規則

| 層級 | 讀取 | 寫入 | 說明 |
|------|------|------|------|
| Raw | ✅ | ❌ 禁止 | 原始來源，LLM 不得覆寫 |
| Wiki | ✅ | ✅ LLM | 自動維護，更新留 timestamp |
| Schema | ✅ | ❌ 禁止 | 人類定義結構 |