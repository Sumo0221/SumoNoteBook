# SumoNoteBook LanceDB 整合開發記錄

> **日期**：2026-04-05
> **負責**：高工蘇茉（SeniorEngineerSuMo）
> **狀態**：已暫停（Gateway Timeout 問題待解決）

---

## 1. 開發思路（Option A/B/C 分析）

### Option A：Fork 原版並修改
- **做法**：直接修改 `memory-lancedb-pro` 原始碼
- **放棄原因**：
  - 破壞原版結構，難以追蹤更新
  - GitHub 有新版時 merge 困難
  - 不符合「保持原版純淨」的原則

### Option B：Standalone Skill
- **做法**：開發獨立 skill 包裝 SumoNoteBook 向量搜索
- **放棄原因**：
  - 記憶系統需要與 LanceDB 深度整合
  - 獨立 skill 無法共享同一個向量數據庫
  - 增加架構複雜度

### Option C：Fork + 深度整合（✅ 採用）
- **做法**：Fork 原版後在 `memory-lancedb-pro` 內部新增 `sumoNotebook` 功能
- **選擇原因**：
  - 保持原版完整性，Fork 版自成一格
  - 共享同一個 LanceDB 實例和配置
  - 向量搜索結果可以直接與 memory 結果合併
  - 便於日後手動 merge 原版更新

---

## 2. Fork 策略

### Fork 位置
```
C:\butler_sumo\developing_tools\memory-lancedb-pro-fork\
```

### 原版位置
```
C:\Users\rayray\.openclaw\workspace\plugins\memory-lancedb-pro\
```

### 為什麼用 Fork？
1. **保持原版純淨**：日後可以乾淨地 pull 原版更新
2. **實驗性質**：深度整合實驗，不影響生產環境
3. **版本比對**：可隨時比對原版與修改版差異

### 如何追蹤原版更新？
1. **手動 merge**（目前採用的方式）：
   ```bash
   # 在 fork 目錄執行
   git remote add upstream https://github.com/CortexReach/memory-lancedb-pro.git
   git fetch upstream
   git merge upstream/main
   # 解決衝突後 push
   ```

2. **版本監控**：
   - 原版 GitHub：https://github.com/CortexReach/memory-lancedb-pro
   - 本地版本：v1.0.26
   - GitHub 版本：v1.1.0-beta.10（較新）

---

## 3. 開發過程中遇到的問題

### 🚨 問題 1：Import Bug
- **症狀**：測試檔案無法正常 import
- **原因**：`join` 與 `pathJoin` 混用
  - Node.js 原生：`path.join()`
  - OpenClaw 環境：`pathJoin()`
- **修復**：統一使用 `pathJoin()`

### 🚨 問題 2：tableName 未傳遞
- **症狀**：`sumoNotebook.tableName` 設定無效，永遠使用 "sumo_notebook"
- **原因**：store 層硬編碼 tableName，未接收傳入參數
- **修復**：
  ```typescript
  // src/store.ts 新增
  private notebookTableName: string;
  
  openNotebookTable(): Promise<void> {
    // 使用 this.notebookTableName 而非硬編碼
  }
  ```

### 🚨 問題 3：configSchema 缺少定義
- **症狀**：`sumoNotebook` 設定無法被 OpenClaw 接受
- **原因**：`openclaw.plugin.json` 的 `configSchema` 沒有 `sumoNotebook` 屬性
- **修復**：在 `configSchema.properties` 加入：
  ```json
  "sumoNotebook": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "enabled": { "type": "boolean", "default": false },
      "tableName": { "type": "string", "default": "sumo_notebook" },
      "maxResults": { "type": "integer", "default": 3 },
      "minScore": { "type": "number", "default": 0.35 }
    }
  }
  ```

### 🚨 問題 4：向量搜索分數為 0
- **症狀**：`query_notebook.mjs` 查詢時所有 score 都是 `0.0000`
- **原因**：LanceDB JS SDK 回傳 `_distance` 不是 `_score`
- **修復**：
  ```javascript
  // 改為
  const distance = r._distance ?? r._score ?? 0;
  const score = 1 / (1 + distance);  // 轉換為相似度
  ```
- **修復者**：高工蘇茉（2026-04-06）

---

## 4. 解決方案

### 修改的檔案

| 檔案 | 變更內容 |
|------|---------|
| `src/store.ts` | 新增 `notebookTable`、`openNotebookTable()`、`notebookVectorSearch()` |
| `src/retriever.ts` | 新增 `sumoNotebook` config、`sumoNotebookSearch()`、`mergeNotebookResults()` |
| `index.ts` | 新增 `sumoNotebook` 到 PluginConfig |
| `openclaw.plugin.json` | 新增 `sumoNotebook` configSchema |
| `test/test_sumo_notebook_integration.mjs` | 新增整合測試 |
| `OPTION_C_DEV_GUIDE.md` | 新增開發指南 |

### sumoNotebook 配置結構
```json
{
  "sumoNotebook": {
    "enabled": false,
    "tableName": "sumo_notebook",
    "maxResults": 3,
    "minScore": 0.35
  }
}
```

### SumoNoteBook 現況（2026-04-05）
- **260 個 chunks** 已索引
- **117 個 Markdown 檔案**
- **327 KB 內容**

---

## 5. Fork 版維護指南

### 目錄結構
```
C:\butler_sumo\developing_tools\memory-lancedb-pro-fork\
├── src/                    # 修改的源碼
├── test/                   # 測試檔案
├── node_modules/           # 依賴
├── openclaw.plugin.json    # 插件配置（含 sumoNotebook schema）
├── index.ts               # 插件入口
└── OPTION_C_DEV_GUIDE.md  # 開發指南
```

### 手動 Merge 原版更新

```bash
# 1. 進入 fork 目錄
cd C:\butler_sumo\developing_tools\memory-lancedb-pro-fork\

# 2. 新增 upstream remote（若尚未設定）
git remote add upstream https://github.com/CortexReach/memory-lancedb-pro.git

# 3. 取得原版更新
git fetch upstream

# 4. 查看目前分支
git branch

# 5. Merge 原版更新
git merge upstream/main

# 6. 若有衝突，解決衝突後：
git add .
git commit -m "Merge: upstream/main"

# 7. 確認修改的檔案
git diff --name-only HEAD~1

# 8. 推送更新
git push origin main
```

### Merge 時的注意事項
1. **`src/store.ts`**：檢查是否有新的 vector search 方法
2. **`src/retriever.ts`**：檢查 retrieval 邏輯是否有變
3. **`openclaw.plugin.json`**：`configSchema` 是否相容
4. **測試**：merge 後執行整合測試確認功能正常

---

## 6. 重要技術細節

### sumoNotebook schema 加入 openclaw.plugin.json
```json
"sumoNotebook": {
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "enabled": { "type": "boolean", "default": false },
    "tableName": { "type": "string", "default": "sumo_notebook" },
    "maxResults": { "type": "integer", "default": 3 },
    "minScore": { "type": "number", "default": 0.35 }
  }
}
```

### sumoNotebook 設定寫入 openclaw.json
```json
{
  "plugins": {
    "entries": {
      "memory-lancedb-pro": {
        "enabled": true,
        "config": {
          "sumoNotebook": {
            "enabled": true,
            "tableName": "sumo_notebook",
            "maxResults": 3,
            "minScore": 0.35
          }
        }
      }
    }
  }
}
```

### 為什麼 sumoNotebook.enabled 是死設定？
- **原因**：`enabled` 選項在程式碼中從未被實作判斷
- **影響**：即使設為 `false`，SumoNoteBook 搜索仍會執行
- **建議**：日後需要實作 `if (!config.sumoNotebook?.enabled) return` 邏輯

---

## 7. 品管結果（2026-04-05）

### 🚨 嚴重問題（必須修復）
1. **測試檔案 Import Bug**：`join` vs `pathJoin` 混亂
2. **tableName 參數未傳遞**：store 層永遠用硬編碼 "sumo_notebook"
3. **configSchema 缺少定義**：`sumoNotebook` 設定無法被接受

### ⚠️ 中等問題
4. 結果合併邏輯：notebook 結果可能永遠被 memory 吃掉
5. 開發指南待辦事項未完成

---

## 8. Gateway Timeout 問題（2026-04-06）

### 問題描述
- 啟用 sumoNotebook Option C 功能後，Gateway 常常 timeout
- 錯誤：`gateway timeout after 100000ms`

### 老爺操作
1. 恢復到沒有 sumoNotebook 的備份版本
2. 將有 sumoNotebook 的版本備份為：
   ```
   memory-lancedb-pro.bak.20260406_has_sumonotebook_rag
   ```

### 待解決
- [ ] 高工蘇茉研究為什麼 sumoNotebook 會導致 Gateway timeout
- [ ] 等 Gateway 穩定後再派發任務

---

## 9. 新專案開發流程

根據老爺指示，Option C 完成後需加 **步驟 4**：

| 步驟 | 內容 | 負責 |
|------|------|------|
| 1 | 比較本地與 GitHub 版本 | 高工蘇茉 |
| 2 | Fork 最新版 | 高工蘇茉 |
| 3 | Option C 深度整合 | 高工蘇茉 |
| **4** | **品管蘇茉品管檢查**（新增）| 品管蘇茉 |

---

## 10. 重要路徑總整理

| 項目 | 路徑 |
|------|------|
| **Fork 版** | `C:\butler_sumo\developing_tools\memory-lancedb-pro-fork\` |
| **原版** | `C:\Users\rayray\.openclaw\workspace\plugins\memory-lancedb-pro\` |
| **SumoNoteBook** | `C:\butler_sumo\library\SumoNoteBook\` |
| **SumoNoteBook Scripts** | `C:\butler_sumo\library\SumoNoteBook\scripts\` |
| **有問題的備份** | `C:\butler_sumo\developing_tools\memory-lancedb-pro-fork\` (待確認) |
| **問題備份** | `memory-lancedb-pro.bak.20260406_has_sumonotebook_rag` |

---

## 11. 性能優化：Fallback 模式（2026-04-06）

### 問題描述
原本的 Option C 每次查詢都會同步搜尋 `memories` 和 `sumo_notebook` 兩個資料表，造成效能問題和 Gateway Timeout。

### 解決方案：Fallback 模式

**新邏輯**（修改 `retriever.ts`）：
```
1. 先搜 memories 資料表
2. 如果記憶體結果足夠好（>= 2 個結果 且 最高分 >= 0.5）
   → 直接回答，不搜 sumo_notebook
3. 如果記憶體結果不夠好
   → 才去搜 sumo_notebook，並合併結果
```

### 修改內容
修改了 `retriever.ts` 中的兩處：
1. `retrieve()` 方法（第 657 行附近）
2. `retrieveWithTrace()` 方法（第 735 行附近）

```typescript
// 原本：總是同時搜 notebook
if (this.config.sumoNotebook?.enabled) {
  const notebookResults = await this.sumoNotebookSearch(...);
  if (notebookResults.length > 0) {
    results = this.mergeNotebookResults(results, notebookResults, safeLimit);
  }
}

// 改為：只有在 memory 結果不足時才搜 notebook
if (this.config.sumoNotebook?.enabled && results.length > 0) {
  const hasSufficientMemoryResults = results.length >= 2 && results[0].score >= 0.5;
  if (hasSufficientMemoryResults) {
    // Memory 結果夠好，直接返回
    return results;
  }
  // Memory 結果不足，嘗試 notebook
  const notebookResults = await this.sumoNotebookSearch(...);
  if (notebookResults.length > 0) {
    results = this.mergeNotebookResults(results, notebookResults, safeLimit);
  }
}
```

### 好處
1. **減少資源消耗**：大多數時候不需要同時搜兩個資料表
2. **避免 Gateway Timeout**：只在需要的時候才搜 notebook
3. **維持效能**：記憶體搜尋快的時候就不浪費時間在 notebook

### 修改者
- 總管蘇茉（2026-04-06 08:00）

---

## 12. 待辦事項

- [ ] 觀察 Gateway Timeout 是否改善
- [ ] 持續優化 `sumoNotebook.enabled` 功能
- [ ] 確保 notebook 結果與 memory 結果正確合併
- [ ] 測試 fork 版本在未來可以順利 merge

---

*最後更新：2026-04-06 08:00 GMT+8*
*作者：總管蘇茉*


*最後更新：\