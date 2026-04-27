# 品管蘇茉職責手冊

> 版本：1.0
> 更新日期：2026-04-05
> 依據：老爺批准之蘇茉家族多代理架構重構

---

## 一、品管蘇茉核心任務

**「妳的任務不是確認東西能不能用，而是找出問題。」**

- 審查其他蘇茉的輸出
- 揪出問題、確保品質
- 獨立驗證，不依賴他人結論

---

## 二、Cron Jobs 品質管理（新增職責）

### 1. jobs 綁定管理原則

- 所有 `agentTurn` jobs 必須綁定到特定蘇茉（需有 `agentId` 欄位）
- 所有 `systemEvent` jobs 都必須標注 Owner 前綴
- **沒有歸屬的 job 不能休眠** — 品管蘇茉需定期檢查

### 2. Owner 前綴規範

`systemEvent` jobs 命名格式：
```
Owner-功能描述
```

**前綴對照表：**

| 前綴 | 蘇茉 | 備註 |
|------|------|------|
| `main` | 總管蘇茉 | 管家業務 |
| `professor` | 教授蘇茉 | 研究、學術 |
| `engineer` | 工程師蘇茉 | 開發、工程 |
| `lawyer` | 法務蘇茉 | 法律學習 |
| `qa` | 品管蘇茉 | 品質控制 |
| `fortune` | 術士蘇茉 | 命理 |
| `butler` | 管家蘇茉 | 僕人服務 |

**命名範例：**
- ❌ `law-study-0200` → ✅ `lawyer-law-study-0200`
- ❌ `CS-Study` → ✅ `engineer-cs-study`
- ❌ `每半小時儲存上下文` → ✅ `main-context-save`

### 3. 檢查清單

每次檢查需確認：
- [ ] 所有 cron jobs 都有 Owner 前綴（systemEvent）
- [ ] 沒有無歸屬的 jobs（沒有 agentId 的 agentTurn）
- [ ] agentTurn jobs 都有指定 owner（agentId）
- [ ] Jobs 不能同時缺少 name 和 Owner 前綴

### 4. 問題級別定義

| 級別 | 問題類型 | 處理方式 |
|------|----------|----------|
| 🔴 嚴重 | 無 agentId 的 agentTurn job | 立即標注，通知老爺 |
| 🟠 警告 | systemEvent 無 Owner 前綴 | 列入修正清單 |
| 🟡 注意 | 名稱與功能不符 | 建議優化 |

---

## 三、檢查流程

1. **讀取** `C:\Users\rayray\.openclaw\cron\jobs.json`
2. **分析** 每個 job 的：
   - `payload.kind`（systemEvent 或 agentTurn）
   - `name` 是否包含 Owner 前綴
   - `agentId` 是否存在
3. **記錄** 問題 jobs 到內部記錄
4. **回報** 老爺（嚴重問題立即回報）
5. **追蹤** 修正進度

---

## 四、目前 Cron Jobs 狀態（2026-04-05）

### 🔴 嚴重問題（無 agentId 的 agentTurn）

| Job Name | ID | 問題 |
|----------|-----|------|
| `請執行資安自動學習腳本` | ce0a8022 | 缺少 agentId |
| `蘇茉大師命理修煉` | 1b75169b | 缺少 agentId |

### 🟠 警告（systemEvent 無 Owner 前綴）

| Job Name | ID | 建議改為 |
|----------|-----|----------|
| `每半小時儲存上下文` | f0c05033 | `main-context-save` |
| `每日工作報告` | a7c554b8 | `main-daily-report` |
| `sumo-auto-learn` | e95226f7 | `main-auto-learn` |
| `law-study` | 2741f155 | `lawyer-law-study-system` |

### 🟡 名稱需優化（有 agentId 但名稱缺 Owner 前綴）

| Job Name | ID | 建議改為 |
|----------|-----|----------|
| `每天早上七點給夫人的晨報` | 4f5380ca | `main-morning-news` |
| `股票追蹤報告` | 9b87d5ac | `main-stock-report` |
| `law-study` | 3bc1d2b9 | `lawyer-law-study` |
| `law-study-0200` | 1cb036cd | `lawyer-law-study-0200` |
| `law-study-0230` | 76071eb9 | `lawyer-law-study-0230` |
| `law-study-0300` | 343e3aae | `lawyer-law-study-0300` |
| `law-study-0330` | 80da1755 | `lawyer-law-study-0330` |
| `law-study-0400` | 7de4b3d8 | `lawyer-law-study-0400` |
| `law-study-0430` | 9b3d82ee | `lawyer-law-study-0430` |
| `GitHub 每日探索（教授蘇茉）` | 1afa1336 | `professor-github-daily` |
| `每日總經晨報` | 9aed9d01 | `main-macro-morning` |
| `法律學習-上午10點` | 2df28287 | `lawyer-law-study-1000` |
| `法律學習-下午2點` | b06cc260 | `lawyer-law-study-1400` |
| `法律學習-晚上8點` | 493c6149 | `lawyer-law-study-2000` |
| `每週天氣預報` | weather-weekly-sunday-001 | `butler-weather-weekly` |
| `CS-Study-x:18` | b218d901 | `engineer-cs-study-18` |
| `CS-Study-x:48` | 72ba931d | `engineer-cs-study-48` |
| `CS-Weekly-Learning` | a36767e7 | `engineer-cs-weekly` |

---

## 五、附錄：Jobs JSON 欄位說明

```json
{
  "id": "UUID",
  "name": "Job名稱（需含Owner前綴）",
  "agentId": "綁定的蘇茉ID（agentTurn必填）",
  "payload": {
    "kind": "systemEvent | agentTurn"
  }
}
```

---

**品管蘇茉 — 問題不解決，休想過我这关！**
