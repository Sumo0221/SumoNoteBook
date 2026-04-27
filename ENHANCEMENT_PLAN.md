# SumoNoteBook Lint + 搜尋增強計劃

## 📋 功能項目

### 1. Lint 流程增強（health_check.py v3.0）✅
- [x] 孤兒檔案檢測（orphan files）
- [x] 斷裂連結檢測（broken links）
- [x] 損壞檔案檢測（corrupted files）
- [x] 檔案類型統計
- [x] 矛盾檢測（contradictions）
- [x] 過時內容檢測（stale claims）
- [x] 建議新連結（missing cross-references）
- [x] 孤立概念檢測
- [ ] 自動修復斷裂連結（待實現）

### 2. qmd 搜尋引擎整合 ✅
- [x] 研究 qmd 安裝方式
- [x] 建立 qmd 安裝指南
- [ ] 安裝 qmd
- [ ] 配置 qmd MCP server
- [x] 更新 SOUL.md 加入 qmd 說明

### 3. Obsidian 整合 ✅
- [x] 建立 Obsidian 使用指南
- [ ] 配置 Obsidian vault 掛鉤
- [x] 更新 SOUL.md 加入 Obsidian 說明

### 4. log.md 增強 ✅
- [x] 更新 log.md 格式（Karpathy 風格）
- [x] 更新 SOUL.md log 規範

---

## 📁 實作檔案

| 檔案 | 位置 | 功能 |
|------|------|------|
| health_check_v3.py | scripts/ | 完整 Lint 檢查 v3.0 |
| qmd_guide.md | docs/ | qmd 安裝指南 |
| obsidian_guide.md | docs/ | Obsidian 使用指南 |
| SOUL.md | Sumo_wiki/ | 已更新（Lint v3.0 + qmd）|
| log.md | Sumo_wiki/ | 已更新（Karpathy 風格）|
| health_report.md | Sumo_wiki/ | 健康報告（自動產生）|

---

## 🔄 log.md Karpathy 風格格式

```markdown
## [2026-04-06] ingest | 文章標題
- 來源：URL or 檔案
- 概念：[概念1], [概念2]
- 頁面更新：page1.md, page2.md

## [2026-04-06] query | 問題摘要
- 使用的頁面：page1.md, page2.md
- 答案：新頁面名

## [2026-04-06] lint | 健康檢查
- 問題：3 個孤兒、2 個斷裂連結
- 修復：5 個
- 待處理：1 個矛盾
```