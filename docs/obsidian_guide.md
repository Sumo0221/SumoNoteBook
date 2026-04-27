# Obsidian 整合指南

## 📋 概述

Obsidian 是一個强大的本地 Markdown 知識庫工具，可以作為 SumoNoteBook 的 IDE（整合開發環境）。

```
Obsidian = IDE
LLM Agent = 程式設計師
SumoNoteBook Wiki = 程式碼庫
```

---

## 🎯 為什麼要用 Obsidian？

| 功能 | 說明 |
|------|------|
| 圖譜視圖 | 可視化 Wiki 的連結結構 |
| 快速導航 | 雙向連結、標籤搜尋 |
| 外掛生態 | Web Clipper、模板、統計 |
| 本地存儲 | 純文字，安全可控 |

---

## 🔧 Obsidian 安裝與配置

### 1. 安裝 Obsidian

下載地址：https://obsidian.md/

### 2. 建立 Vault

1. 打開 Obsidian → 新建 Vault
2. Vault 名稱：`SumoNoteBook`
3. 選擇路徑：`C:\butler_sumo\library\SumoNoteBook\Sumo_wiki`

### 3. 核心設定

#### 檔案與連結
```
Settings → Files & Links
- 附件資料夾路徑：raw/assets/
- 自動更新的內部連結：開啟
- 偵測所有內部連結類型：開啟
```

#### 快捷鍵（可自訂）
| 功能 | 快捷鍵 |
|------|--------|
| 下載附件 | Ctrl+Shift+D |
| 快速切換 | Ctrl+O |
| 圖譜視圖 | Ctrl+G |
| 搜尋 | Ctrl+Shift+F |

---

## 🔌 必備外掛

### 1. Obsidian Web Clipper（必須）

用於從網頁擷取內容為 Markdown。

**安裝方式**：
1. Obsidian → Settings → Community Plugins → 搜尋 "Web Clipper"
2. 安裝並啟用

**使用方式**：
1. 在瀏覽器中安裝 Obsidian Web Clipper 擴充功能
2. 瀏覽網頁時，點擊擴充功能圖示
3. 選擇 "Clip to SumoNoteBook"
4. 內容會存到 `raw/` 資料夾

### 2. Dataview（建議）

用於查詢和統計 Wiki 內容。

**查詢範例**：
````markdown
```dataview
TABLE file.ctime, file.size
FROM "concepts"
WHERE file.size > 1000
SORT file.ctime DESC
```
````

### 3. Find Orphaned Files（建議）

找出沒有被引用的孤兒檔案。

### 4. Link Styles（可選）

自訂連結樣式。

---

## 📊 Obsidian 作為 Wiki IDE

### 工作流程

```
1. 老爺在瀏覽器看到好文章
   ↓
2. 使用 Web Clipper 擷取到 raw/
   ↓
3. LLM Agent（蘇茉）自動執行 Ingest
   ↓
4. Wiki 頁面更新
   ↓
5. 老爺在 Obsidian 中查看結果
   ↓
6. 追蹤連結、查看圖譜
```

### Obsidian 視圖

#### 圖譜視圖（Graph View）
- 按 Ctrl+G 開啟
- 顯示所有頁面和連結
- 節點大小 = 引用次數
- 顏色 = 分類（概念/摘要/QA）

#### 局部圖譜
- 在某個頁面按 Ctrl+G
- 只顯示該頁面的連結網絡

#### 反向連結面板
- 右側面板預設顯示
- 所有引用該頁面的連結

---

## 🔄 自動同步

### 觸發 Ingest 的方式

#### 方式 A：自動（每日）
在 `HEARTBEAT.md` 中設定每日 4:12 AM 自動執行。

#### 方式 B：手動
老爺說：「蘇茉，執行 Ingest」

#### 方式 C：Obsidian 觸發
使用 Obsidian Shell Commands 外掛：
1. 安裝 "Obsidian Shell Commands" 外掛
2. 設定命令：`python "C:\butler_sumo\library\SumoNoteBook\scripts\ingest_notebook.mjs"`
3. 快捷鍵：Ctrl+Shift+I

---

## 📱 行動版 Obsidian

iOS/Android 有 Obsidian 行動版：
1. 安裝 Obsidian 行動版
2. 開啟 vault 同步（iCloud/Dropbox/自架伺服器）
3. 隨時隨地查看 Wiki

---

## 🎨 樣式設定

### 推薦主題
- **Blue Topaz**（淺色護眼）
- **Obsidian Dark**（深色）

### 程式碼區塊主題
- **Obsidian Dark** 或 **Dracula**

---

## 🚀 進階技巧

### 1. 模板系統
建立模板自動插入：
- 日期
- 標籤
- 摘要區塊

### 2. 標籤整理
使用統一的標籤階層：
- `#技術/Python`
- `#概念/架構`
- `#項目/SumoNoteBook`

### 3. 日曆外掛
使用 Calendar 外掛：
- 每日筆記
- 回顧過去某天的記錄

---

## 📞 獲取幫助

- Obsidian 官方文檔：https://publish.obsidian.md/help
- 中文社群：Reddit r/ObsidianMD
- 插件搜尋：https://obsidian.md/plugins

---

## ✅ 檢查清單

- [ ] 安裝 Obsidian
- [ ] 建立 Vault 並指向 Sumo_wiki
- [ ] 安裝 Web Clipper 外掛
- [ ] 安裝瀏覽器 Web Clipper 擴充
- [ ] 設定快捷鍵
- [ ] 試用圖譜視圖
- [ ] 試用 Web Clipper 擷取一篇文章