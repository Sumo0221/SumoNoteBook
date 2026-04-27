# Wenget - 跨平台 GitHub 二進位檔案管理器

## 基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | superYngo |
| **GitHub** | https://github.com/superyngo/Wenget |
| **類型** | Rust CLI 工具 |
| **用途** | 跨平台 GitHub 二進位檔案管理工具 |

---

## 這是什麼？

一個用 Rust 寫的跨平台套件管理器，專門管理 GitHub Releases 發布的二進位檔案。

> A cross-platform portable binary package manager powered by GitHub releases. Simple, fast, and always up-to-date.

---

## 核心功能

| 功能 | 說明 |
|------|------|
| **🚀 One-line Installation** | 一行指令快速安裝 |
| **🔄 Auto-update** | 自動安裝最新版本 |
| **📦 Bucket System** | 用 bucket manifest 管理套件 |
| **📜 Script Support** | 支援 PowerShell、Bash、Python 腳本 |
| **🌐 Cross-platform** | Windows、macOS、Linux |
| **📁 Organized Storage** | 所有套件放在 ~/.wenget/ |
| **🔍 Smart Search** | 搜尋所有 bucket 的套件 |
| **⚡ Fast Downloads** | 多執行緒下載 + 快取 |
| **🎯 Platform Detection** | 自動偵測平台架構 |
| **🔧 Smart Command Naming** | 自動移除執行檔的平台後綴 |

---

## 安裝方式

### Windows
```powershell
irm https://raw.githubusercontent.com/superyngo/Wenget/main/install.ps1 | iex
```

### Linux/macOS
```bash
curl -fsSL https://raw.githubusercontent.com/superyngo/Wenget/main/install.sh | bash
```

### 系統層級安裝（需要管理員/root）
```bash
# Linux/macOS
sudo curl -fsSL https://raw.githubusercontent.com/superyngo/Wenget/main/install.sh | sudo bash

# Windows (以系統管理員開啟 PowerShell)
irm https://raw.githubusercontent.com/superyngo/Wenget/main/install.ps1 | iex
```

---

## 常用指令

| 指令 | 說明 |
|------|------|
| `wenget init` | 初始化 Wenget 目錄和設定 |
| `wenget add <package>` | 安裝套件 |
| `wenget delete <package>` | 解除安裝套件 |
| `wenget list` | 列出已安裝的套件 |
| `wenget search <keyword>` | 搜尋套件 |
| `wenget update` | 更新已安裝的套件 |
| `wenget update self` | 更新 Wenget 本身 |
| `wenget bucket add <url>` | 新增 bucket |
| `wenget bucket create` | 從 repo 產生 bucket manifest |

---

## 目錄結構

### 使用者層級
```
~/.wenget/
├── apps/              # 已安裝的應用程式
├── bin/               # 符號連結（加入 PATH）
├── cache/             # 快取（manifest 和下載檔案）
├── config.toml        # 使用者設定
├── buckets.json     # Bucket 設定
└── installed.json   # 已安裝套件資訊
```

### 系統層級（root/Administrator）
```
/opt/wenget/          # Linux/macOS
%ProgramW6432%\wenget\  # Windows
├── app/              # 已安裝的應用程式
├── bin/              # 二進位檔案
├── cache/
├── buckets.json
└── installed.json
```

---

## Bucket System（桶系統）

### 這是什麼？
Bucket 是一個線上託管的套件清單（manifest.json），可以新增多個 bucket 來源。

### 官方 bucket
```bash
wenget bucket add wenget https://raw.githubusercontent.com/superyngo/wenget-bucket/main/manifest.json
```

### 建立自己的 Bucket
```bash
# 從 repo 清單產生 manifest
wenget bucket create -r repos.txt -o manifest.json

# 使用 GitHub token 提高 API 限制
wenget bucket create -r repos.txt -o manifest.json -t YOUR_TOKEN
```

### manifest.json 範例
```json
{
  "packages": [
    {
      "name": "my-tool",
      "repo": "https://github.com/username/repo",
      "description": "Tool description",
      "homepage": "https://example.com"
    }
  ]
}
```

---

## 與蘇茉家族的關係

### 可參考的功能

| Wenget 功能 | 蘇茉家族可以學 |
|-------------|----------------|
| **Bucket System** | 蘇茉家族的 skill 分享機制 |
| **Auto-update** | 套件自動更新 |
| **跨平台支援** | Windows/macOS/Linux |
| **多執行緒下載** | 加速下載 |

### 老爺可能感興趣的原因
- Wenget 和 AGM 是同一個作者（superyngo）
- 都是 Rust 寫的工具
- 都可以管理 CLI 工具

---

## 注意（v0.2.x → v0.3.0 遷移）

- Unix: `~/.wenget/bin/` → `~/.local/bin/`
- Windows: `%USERPROFILE%\.wenget\bin\` → `%USERPROFILE%\.local\bin\`

需要手動遷移！

---

## 標籤

#知識儲備 #Wenget #套件管理器 #Rust CLI #GitHub Releases #跨平台 #BucketSystem

---

*記錄者：總管蘇茉*
*時間：2026-04-09 12:09*
