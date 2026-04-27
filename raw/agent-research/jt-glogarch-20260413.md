# jt-glogarch 研究：Graylog Open Archive 解決方案

> 來源：GitHub - jasoncheng7115/jt-glogarch
> 日期：2026-04-13
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 概述

jt-glogarch 為 Graylog Open 提供完整的日誌歸檔和還原功能，填補了 Enterprise 版才有的 Archive 功能。

**作者**：Jason Cheng
**許可**：Apache 2.0

---

## 🎯 解決什麼問題

Graylog Open 沒有 Enterprise 版的 Archive 功能，jt-glogarch 填補了這個缺口。

---

## 📊 兩種匯出模式

| 模式 | 速度 | 特色 |
|------|------|------|
| **Graylog REST API** | ~730 records/s | 支援 Stream filter |
| **OpenSearch Direct** | ~3,300 records/s | 快 5 倍，不走 Graylog |

---

## ✨ 核心功能

| 功能 | 說明 |
|------|------|
| **壓縮歸檔** | 匯出為 .json.gz（含 SHA256 驗證）|
| **還原日誌** | 透過 GELF (TCP/UDP) 或 OpenSearch Bulk 回灌 |
| **排程管理** | Cron 排程（每小時/每天/每週/每月）|
| **自動清理** | 根據保留政策自動刪除 |
| **平行處理** | --workers N 平行驗證 |
| **跨模式去重** | 防止 API 和 OpenSearch 模式重複匯出 |
| **中斷恢復** | 已完成的 chunks 不會重新匯出 |
| **Streaming Write** | 不把全部資料放記憶體，直接寫入磁碟 |

---

## 📈 還原模式

| 模式 | 速度 | 特色 |
|------|------|------|
| **GELF (Pipeline)** | ~5,000 msg/s | 完整 Graylog 處理流程，支援 pipeline rules、alerts |
| **OpenSearch Bulk** | ~30,000-100,000 msg/s | 直接寫入，略過 Graylog |

---

## 🔔 通知頻道

| 頻道 |
|------|
| Telegram、Discord、Slack、Microsoft Teams、Nextcloud Talk、Email (SMTP) |

---

## 💡 可借鑽的功能

| 設計 | 說明 | 對蘇茉家族的應用 |
|------|------|------------------|
| **雙模式架構** | API vs Direct（速度快 5x）| MemPalace 可以有「快速檢索 vs 深度檢索」模式 |
| **Streaming Write** | 不把全部資料放記憶體 | 蘇茉日總結可以串流寫入 |
| **完整性驗證** | SHA256 sidecar | Compaction-Validator 可加入 hash 驗證 |
| **中斷恢復** | 已完成的不重做 | 記憶寫入可參考斷點續傳 |
| **時間分塊** | 每小時分塊，預防大檔 | SumoMemory 可做時間分塊歸檔 |
| **Retention Policy** | 自動清理過期資料 | 蘇茉可以設定記憶保留期限 |
| **Preflight Check** | 還原前完整檢查 | 重要操作前先驗證 |
| **Web UI + CLI** | 兩種操作介面 | Sumo-HUD 可以有 CLI + GUI |
| **6 頻道通知** | Telegram/Discord/Slack/等 | 蘇茉通知系統可參考 |
| **Dashboard 設計** | 統計卡片 + sparkline | Sumo-HUD 可以用圖表 |
| **SQLite WAL** | thread-safe + 高速 | 蘇茉的資料庫可以用 WAL |
| **雙語支援** | English + 繁體中文 | 蘇茉的文件可以雙語 |

---

## 📋 蘇茉家族行動項目

| 功能 | 優先級 | 負責蘇茉 | 狀態 |
|------|--------|----------|------|
| Compaction SHA256 驗證 | 🔴 高 | 總管蘇茉 | 待處理 |
| Streaming 日總結 | 🟡 中 | 工程師蘇茉 | 待處理 |
| 記憶保留期限 | 🟡 中 | 總管蘇茉 | 待處理 |
| Sumo-HUD Dashboard | 🟢 低 | 高工蘇茉 | 已在開發 |

---

## 📁 相關連結

- [GitHub](https://github.com/jasoncheng7115/jt-glogarch)

---

*最後更新：2026-04-13*
