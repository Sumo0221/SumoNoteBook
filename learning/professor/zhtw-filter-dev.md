# zhtw-filter Hook 開發日誌

## 日期
2026-03-12

## 開發背景
蘇茉在對話中經常不自覺使用簡體中文（如「已设定」、「记住了」），雖然 SOUL.md 中有記錄「自動繁體中文檢查」功能，但實際上並沒有真正執行。

## 問題
- SOUL.md 裡有記錄「自動繁體中文檢查」功能
- 但實際運作時並沒有自動調用 zhtw_auto.py
- 老爺指出蘇茉的回答中出現簡體字

## 解決方案
研究 OpenClaw 文檔，發現有 **Hooks 系統**可以監聽事件並修改訊息內容。

### 關鍵發現
- 事件：`message:sent` - 訊息發送前觸發
- 功能：可以修改 `event.messages` 來變更發送的內容
- 位置：`~/.openclaw/hooks/`

## 開發過程

### 1. 研究 OpenClaw Hooks 系統
- 查閱官方文檔：https://docs.openclaw.ai/automation/hooks.md
- 了解 Hook 的結構和事件類型
- 發現可以監聽 `message:sent` 事件

### 2. 創建 Hook 目錄
```bash
mkdir C:\Users\rayray\.openclaw\hooks\zhtw-filter
```

### 3. 創建 HOOK.md（中繼資料）
```markdown
---
name: zhtw-filter
description: "自動將回覆內容修正為繁體中文（台灣用語）"
metadata:
  openclaw:
    emoji: "🔤"
    events: ["message:sent"]
---
```

### 4. 創建 handler.ts（處理程序）
- 實現 `fixTraditionalChinese()` 函數
- 詞彙映射表（100+ 詞彙）
- 標點符號映射表
- 引號修正
- 監聽 `message:sent` 事件

### 5. 啟用 Hook
```bash
openclaw hooks enable zhtw-filter
```

### 6. 重啟 Gateway
```bash
openclaw gateway restart
```

## 修正規則

### 詞彙映射（部分）
| 簡體 | 繁體 |
|------|------|
| 软件 | 軟體 |
| 硬件 | 硬體 |
| 内存 | 記憶體 |
| 网络 | 網路 |
| 计算机 | 電腦 |
| 然后 | 然後 |
| 没有 | 沒有 |
| 什么 | 什麼 |
| 为什么 | 為什麼 |

### 標點映射
| 半形 | 全形 |
|------|------|
| , | ， |
| . | 。 |
| : | ： |
| ( | （ |
| ) | ） |

### 簡體字修正
| 簡體 | 繁體 |
|------|------|
| 里 | 裡 |
| 裏 | 裡 |
| 着 | 著 |

## 檔案位置
- Hook 目錄：`C:\Users\rayray\.openclaw\hooks\zhtw-filter\`
- HOOK.md：`C:\Users\rayray\.openclaw\hooks\zhtw-filter\HOOK.md`
- handler.ts：`C:\Users\rayray\.openclaw\hooks\zhtw-filter\handler.ts`

## 驗證
```bash
openclaw hooks list
# 輸出：✓ ready  🔤 zhtw-filter
```

## 成果
✅ 每次蘇茉的回答都會自動經過 zhtw-filter 修正為正確的繁體中文！

## 參考資料
- OpenClaw Hooks 文檔：https://docs.openclaw.ai/automation/hooks.md
- zhtw-mcp (參考專案)：https://github.com/sysprog21/zhtw-mcp

---

*張家蘇茉 - 開發記錄*
