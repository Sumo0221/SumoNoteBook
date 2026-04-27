# Star Office UI Relay 擴展規劃

## 目標
將 VPC Relay 功能結合到 Star Office UI，讓多個蘇茉可以透過辦公室互相對話。

---

## 現有資源

| 功能 | 狀態 |
|------|------|
| Star Office UI 後端 | ✅ 運行中 (http://127.0.0.1:19000) |
| 狀態管理 | ✅ 已實現 (/set_state, /status) |
| 多 Agent 支援 | ✅ 已實現 (/join-agent, /leave-agent) |
| Relay 訊息轉發 | ❌ 需開發 |

---

## 需要新增的功能

### 1. 訊息轉發 API

```python
# 新增 API
POST /relay/send     # 發送訊息給另一個蘇茉
GET  /relay/poll    # 長輪詢接收訊息
GET  /relay/inbox   # 查看訊息匣
```

### 2. 訊息格式

```json
{
  "from": "教授蘇茉",
  "to": "管家蘇茉", 
  "body": "今天的股票行情不錯哦！",
  "timestamp": 1234567890
}
```

### 3. 觸發回覆機制

當蘇茉收到訊息時，自動觸發對應的 OpenClaw session 回覆。

---

## 架構圖

```
┌─────────────────────────────────────────────┐
│           Star Office UI                    │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │ 教授蘇茉 │  │ 管家蘇茉 │  │ 其他蘇茉 │     │
│  └────┬────┘  └────┬────┘  └────┬────┘     │
│       │            │            │           │
│       └────────────┼────────────┘           │
│                    ▼                        │
│         ┌─────────────────┐                  │
│         │   Relay Module │                   │
│         │  - 訊息轉發   │                   │
│         │  - 狀態同步   │                   │
│         └─────────────────┘                  │
└─────────────────────────────────────────────┘
```

---

## 開發步驟

### Phase 1：基礎訊息轉發
- [ ] 新增 `relay.py` 模块
- [ ] 實現 `/relay/send` API
- [ ] 實現 `/relay/poll` API
- [ ] 測試兩端訊息傳遞

### Phase 2：結合 OpenClaw
- [ ] 收到訊息時觸發回覆
- [ ] 自動狀態切換（對話中 → writing）
- [ ] Session 管理

### Phase 3：完善體驗
- [ ] 訊息顯示在 UI
- [ ] 未讀訊息提示
- [ ] 多對話支援

---

## 挑戰與解決

| 挑戰 | 解決方案 |
|------|----------|
| 沒有公網 IP | 區域網路內運作，或使用 Tunnel |
| 多 session 管理 | 透過 session label 區分 |
| 觸發回覆 | 使用 OpenClaw CLI |

---

## 參考資源

- 原始 VPC Relay 方案：`C:\Users\rayray\.openclaw\media\inbound\file_16---e4380b08-cf2d-45ad-82a8-515276ae0d82.md`
- Star Office UI：`C:\Users\rayray\.openclaw\workspace\Star-Office-UI\`

---

*更新時間：2026-03-08*
