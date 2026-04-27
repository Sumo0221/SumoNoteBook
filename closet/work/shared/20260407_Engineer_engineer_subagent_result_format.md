# SubagentResult 格式規範

## 📋 文件資訊
- **版本：** 1.0
- **建立日期：** 2026-04-03
- **目的：** 標準化 Sub-agent 結果結構

---

## 🎯 目的

統一 Sub-agent 結果回傳格式，確保主從架構（Main ↔ Sub-agent）之間的通訊一致性，簡化結果解析邏輯並提升錯誤處理效率。

---

## 📦 SubagentResult 結構

```json
{
  "status": "success|error|timeout",
  "session_key": "string",
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  },
  "result": {},
  "timestamp": "ISO8601"
}
```

### 欄位說明

| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `status` | string | ✅ | 執行狀態：success / error / timeout |
| `session_key` | string | ✅ | 工作階段唯一識別碼（UUID 或自訂格式） |
| `error` | object | ❌ | 錯誤資訊（僅在 status=error 時存在） |
| `error.code` | string | ❌ | 錯誤碼（如：TIMEOUT, NOT_FOUND, PERMISSION_DENIED） |
| `error.message` | string | ❌ | 人類可讀的錯誤訊息 |
| `error.details` | object | ❌ | 額外錯誤詳情 |
| `result` | any | ✅ | 執行結果資料 |
| `timestamp` | string | ✅ | ISO8601 格式時間戳記 |

---

## 💻 使用範例

### 成功結果

```python
import json
from datetime import datetime, timezone

def create_success_result(session_key, result_data):
    return {
        "status": "success",
        "session_key": session_key,
        "error": None,
        "result": result_data,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# 使用範例
result = create_success_result(
    session_key="sess_abc123",
    result_data={
        "items": [1, 2, 3],
        "count": 3
    }
)
print(json.dumps(result, indent=2))
```

**輸出：**
```json
{
  "status": "success",
  "session_key": "sess_abc123",
  "error": null,
  "result": {
    "items": [1, 2, 3],
    "count": 3
  },
  "timestamp": "2026-04-03T10:30:00.000000+00:00"
}
```

---

### 錯誤結果

```python
def create_error_result(session_key, code, message, details=None):
    return {
        "status": "error",
        "session_key": session_key,
        "error": {
            "code": code,
            "message": message,
            "details": details or {}
        },
        "result": None,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# 使用範例
error_result = create_error_result(
    session_key="sess_abc123",
    code="FILE_NOT_FOUND",
    message="找不到指定的檔案",
    details={"path": "/tmp/test.txt"}
)
```

---

### 逾時結果

```python
def create_timeout_result(session_key, timeout_seconds):
    return {
        "status": "timeout",
        "session_key": session_key,
        "error": {
            "code": "TIMEOUT",
            "message": f"操作超過 {timeout_seconds} 秒仍未完成",
            "details": {"timeout_seconds": timeout_seconds}
        },
        "result": None,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
```

---

## 🔧 主代理端解析範例

```python
def parse_subagent_result(response):
    """
    解析 Sub-agent 回傳結果的統一介面
    """
    if not response:
        return {
            "success": False,
            "message": "Empty response",
            "data": None
        }
    
    status = response.get("status")
    session_key = response.get("session_key")
    
    if status == "success":
        return {
            "success": True,
            "message": "完成",
            "data": response.get("result")
        }
    elif status == "timeout":
        return {
            "success": False,
            "message": f"逾時: {response.get('error', {}).get('message', '未知')}",
            "data": None
        }
    else:
        error_info = response.get("error", {})
        return {
            "success": False,
            "message": f"錯誤 [{error_info.get('code', 'UNKNOWN')}]: {error_info.get('message', '未知錯誤')}",
            "data": None,
            "error_code": error_info.get("code"),
            "error_details": error_info.get("details")
        }
```

---

## 📊 錯誤碼參考

| 錯誤碼 | 說明 | 處置建議 |
|--------|------|----------|
| `TIMEOUT` | 操作逾時 | 增加 timeout 或簡化任務 |
| `NOT_FOUND` | 資源不存在 | 檢查輸入路徑/ID |
| `PERMISSION_DENIED` | 權限不足 | 確認存取權限 |
| `INVALID_INPUT` | 輸入參數錯誤 | 檢查輸入格式 |
| `SYSTEM_ERROR` | 系統錯誤 | 查看 details 進行除錯 |
| `TOOL_NOT_AVAILABLE` | 工具不可用 | 檢查工具白名單 |
| `MAX_RETRIES_EXCEEDED` | 重試次數超限 | 降低任務複雜度 |

---

## ✅ 預期效益

1. **一致性：** 所有 Sub-agent 回傳格式統一，主代理易於解析
2. **可追蹤性：** timestamp + session_key 方便日誌追蹤
3. **錯誤處理：** 結構化錯誤資訊便於程式化處理
4. **可擴展性：** error.details 可彈性擴展新欄位

---

## 📝 實作檢查清單

- [x] 定義 SubagentResult JSON Schema
- [x] 提供 Python 輔助函數
- [x] 提供主代理端解析範例
- [x] 建立錯誤碼參考表
