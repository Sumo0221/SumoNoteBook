# OpenClaw 實戰文章設定檢查報告

**檢查日期**：2026-04-10  
**研究者**：高工蘇茉（SeniorEngineerSuMo）

---

## 📋 研究主題

根據 OpenClaw 實戰文章，需檢查三個關鍵設定：
1. Session 膨脹閾值（softThresholdTokens）
2. Context Pruning TTL
3. 磁碟空間管理（session maintenance）

---

## 🔍 檢查結果

### 1️⃣ Session 膨脹閾值（softThresholdTokens）

| 項目 | 數值 |
|------|------|
| **目前設定** | `mode: "safeguard"`（預設值） |
| **文章建議** | softThresholdTokens = 40,000 |
| **差異** | ⚠️ 未設定具體數值 |

**現況分析**：
- 目前只有 `"compaction": { "mode": "safeguard" }`
- safeguard 模式應該有預設閾值，但文件中未明確定義為 40,000
- 需確認是否要明確設定 `softThresholdTokens: 40000`

---

### 2️⃣ Context Pruning TTL

| 項目 | 數值 |
|------|------|
| **目前設定** | ❌ 未設定 |
| **文章建議** | context TTL = 6 小時 |
| **差異** | ⚠️ 完全未配置 |

**現況分析**：
- 搜尋 openclaw.json 無發現 `contextPruning` 或 `ttl` 相關設定
- 這可能導致過期 session context 未被及時清理

---

### 3️⃣ 磁碟空間管理（session maintenance）

| 項目 | 數值 |
|------|------|
| **目前設定** | ❌ 未設定 |
| **文章建議** | 磁碟上限 100MB，7 天清理 |
| **差異** | ⚠️ 完全未配置 |
| **實際使用** | 📊 1,855.83 MB（~1.8GB） |

**現況分析**：
- openclaw 目錄總大小約 1.86 GB
- 主要來自眾多 `openclaw.json.clobbered.*` 備份檔案（約數百個）
- 無 session 維護相關設定

---

## 📊 總結對照表

| 設定項目 | 文章建議值 | 目前狀態 | 風險等級 |
|----------|-----------|----------|----------|
| softThresholdTokens | 40,000 | safeguard（未明確定義） | 🟡 中 |
| context TTL | 6 小時 | 未設定 | 🔴 高 |
| session 磁碟上限 | 100MB | 未設定（目前 1.8GB） | 🔴 高 |
| 清理週期 | 7 天 | 未設定 | 🟡 中 |

---

## 💡 調整建議

### 建議 1：設定 compaction 閾值
```json
"compaction": {
  "mode": "safeguard",
  "softThresholdTokens": 40000
}
```

### 建議 2：啟用 context pruning
```json
"contextPruning": {
  "enabled": true,
  "ttlHours": 6
}
```

### 建議 3：設定 session maintenance
```json
"sessionMaintenance": {
  "maxDiskSizeMB": 100,
  "retentionDays": 7
}
```

### 建議 4：清理過多備份檔案
- 考慮刪除舊的 `openclaw.json.clobbered.*` 檔案
- 目前有數百個備份檔，佔用大量空間

---

## 🎯 結論

老爺的 OpenClaw 設定缺少文章中建議的關鍵參數：
- **高優先**：context TTL 和 session maintenance 完全未設定
- **中優先**：compaction 閾值雖有 safeguard 模式，但未明確指定 40,000

建議老爺盡快補上這些設定，以確保系統穩定運作並控制磁碟空間。

---

*高工蘇茉，研究完成*