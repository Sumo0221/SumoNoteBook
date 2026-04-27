# Study: youtube_downloader_gui

## 📋 基本資訊

| 項目 | 內容 |
|------|------|
| **名稱** | youtube_downloader_gui |
| **作者** | milochen0418 |
| **描述** | yt-dlp Web GUI (使用 Python Reflex) |
| **GitHub** | https://github.com/milochen0418/youtube_downloader_gui |
| **學習日期** | 2026-04-24 |

---

## 🔧 技術架構

### 技術堆疊
| 技術 | 用途 |
|------|------|
| **Python 3.11** | 主要程式語言 |
| **Poetry** | 套件管理 |
| **Reflex** | Web GUI 框架 |
| **Playwright** | E2E 測試 |
| **yt-dlp** | YouTube 下載核心 |

### 專案結構
`
youtube_downloader_gui/
├── youtube_downloader_gui.py    # 主程式入口
├── components/                  # 左右面板元件
├── docs/images/                 # GUI 截圖
├── AGENTS.md                    # Agent 工作規範
└── README.md                    # 使用說明
`

---

## 🎯 功能特色

### 主要功能
1. **影片/播放清單抓取** - 輸入 YouTube URL 取得資訊
2. **元資料顯示** - 縮圖、標題、頻道、時長、觀看次數
3. **格式選擇** - 可用格式 ID、編碼、解析度、檔案大小
4. **下載進度** - 進度條、速度、ETA、檔案大小
5. **字幕下載** - 歌詞和字幕工具、語言選擇
6. **播放清單範圍** - 設定起始和結束索引下載

### 介面設計
- **左面板**: 網址輸入、下載控制、預設選擇
- **右面板**: Metadata、Formats、Download Log、Subtitles、Playlist、Raw Output

---

## 🚀 開發指南

### 前置需求
`ash
brew install python@3.11 poetry
poetry run playwright install
`

### 啟動開發伺服器
`ash
poetry run ./reflex_rerun.sh
#  доступен на http://localhost:3000
`

### 乾淨重建
`ash
./proj_reinstall.sh --with-rerun
`

---

## 📚 AGENTS.md 規範重點

1. **永遠先讀文件** - README.md, AGENTS.md
2. **Python 3.11 嚴格要求** - 使用 poetry env use python3.11
3. **優先使用 poetry run** - 執行所有腳本
4. **使用 reflex_rerun.sh** - 啟動/重啟 Reflex 應用
5. **使用 run_test_suite.sh** - 執行 E2E 測試

---

## 💡 對蘇茉家族的價值

| 價值 | 說明 |
|------|------|
| **Reflex 框架學習** | Python Web GUI 開發 |
| **Poetry 套件管理** | 現代 Python 專案管理 |
| ** yt-dlp 整合** | 影片下載技術 |
| **多任務處理** | 進度追蹤、取消、下載範圍 |

---

## 🔗 相關資源

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 影片下載核心
- [Reflex](https://reflex.dev/) - Python Web 框架
- [Poetry](https://python-poetry.org/) - 套件管理

---
*學習完成時間: 2026-04-24*
