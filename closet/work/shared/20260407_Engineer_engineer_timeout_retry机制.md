# 逾時與重試機制設計

## 📋 文件資訊
- **版本：** 1.0
- **建立日期：** 2026-04-03
- **目的：** 為 sessions_spawn 建立 timeout 建議和 max_retries 處理機制

---

## 🎯 目的

防止 Sub-agent 掛起或無限期等待，確保系統資源有效利用，並提供穩定的錯誤恢復機制。

---

## ⏱️ Timeout 設計

### 建議 Timeout 值

| 任務類型 | 建議 Timeout | 說明 |
|---------|-------------|------|
| 快速查詢 | 30 秒 | 簡單檔案讀取、API 查詢 |
| 一般任務 | 5 分鐘 | 標準程式開發、資料處理 |
| 複雜任務 | 15 分鐘 | 深度研究、大規模分析 |
| 長時間任務 | 30 分鐘 | 訓練模型、批量處理 |

### Timeout 參數說明

```python
# sessions_spawn timeout 建議參數
{
    "timeout": 300,           # 預設 5 分鐘（秒為單位）
    "timeout_action": "terminate",  # terminate | fallback | retry
    "timeout_callback": null  # 逾時時的回調函數
}
```

### Timeout 策略

```
┌─────────────────────────────────────────────────────────┐
│                    Timeout 處理流程                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [開始執行] ──► [計時中...] ──► ┌─────────────────────┐   │
│                                │   是否逾時？         │   │
│                                └──────────┬──────────┘   │
│                              是            │ 否          │
│                    ┌───────────┴───┐       │             │
│                    ▼               ▼       ▼             │
│            ┌──────────────┐  ┌──────────────────┐       │
│            │ 終止任務     │  │  檢查是否完成     │       │
│            │ 記錄錯誤     │  └────────┬─────────┘       │
│            │ 等待回覆    │           │                  │
│            └──────────────┘    完成？                    │
│                                   │                      │
│                            是     │     否               │
│                            ▼      │      ▼               │
│                       [返回結果]  │  [繼續計時]           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 Retry 機制設計

### 重試策略

#### 1. 指數退避 (Exponential Backoff)

```python
import time
import random

def calculate_backoff(attempt, base_delay=1, max_delay=60):
    """
    計算指數退避等待時間
    
    參數:
        attempt: 當前嘗試次數（從 1 開始）
        base_delay: 基礎延遲秒數（預設 1 秒）
        max_delay: 最大延遲秒數（預設 60 秒）
    
    退避公式: min(base_delay * (2 ** attempt) + jitter, max_delay)
    
    範例:
        attempt=1 → 1-2 秒
        attempt=2 → 2-4 秒
        attempt=3 → 4-8 秒
        attempt=4 → 8-16 秒
        attempt=5 → 16-32 秒
    """
    jitter = random.uniform(0, base_delay)  # 添加隨機 jitter 避免同步
    delay = min(base_delay * (2 ** (attempt - 1)) + jitter, max_delay)
    return delay
```

#### 2. 重試參數配置

```python
RETRY_CONFIG = {
    "max_retries": 3,           # 最大重試次數
    "base_delay": 1,            # 基礎延遲（秒）
    "max_delay": 60,            # 最大延遲（秒）
    "retryable_errors": [       # 可重試的錯誤碼
        "TIMEOUT",
        "NETWORK_ERROR", 
        "SERVICE_UNAVAILABLE",
        "RATE_LIMITED"
    ],
    "non_retryable_errors": [    # 不可重試的錯誤碼
        "INVALID_INPUT",
        "PERMISSION_DENIED",
        "NOT_FOUND",
        "VALIDATION_ERROR"
    ]
}
```

---

### 重試流程圖

```
┌─────────────────────────────────────────────────────────┐
│                     Retry 處理流程                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [執行任務] ──► [成功？] ──► [返回結果]                   │
│                    │                                     │
│                  失敗                                     │
│                    │                                     │
│          ┌─────────▼─────────┐                           │
│          │ 檢查錯誤碼是否     │                           │
│          │ 可重試？           │                           │
│          └─────────┬─────────┘                           │
│         是          │          否                         │
│    ┌────▼────┐      │                                    │
│    │ 遞增    │      │                                    │
│    │ retry   │      │                                    │
│    │ _count  │      ▼                                    │
│    └────┬────┘  [記錄錯誤，返回失敗]                       │
│         │                                               │
│    ┌────▼────────┐                                      │
│    │ retry_count │                                      │
│    │ < max_retries│                                      │
│    └────┬────────┘                                      │
│    是    │         否                                     │
│    │     │         │                                     │
│    │     ▼         ▼                                     │
│    │  [等待 backoff]                                     │
│    │     │                                               │
│    │     └────────► [重新執行任務]                        │
│    │                                                │
│    └──────────────► [返回最終失敗]                        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 完整實作範例

```python
import time
import random
from datetime import datetime, timezone
from typing import Callable, Any, Optional

class SubagentExecutor:
    """Sub-agent 執行器，封裝 timeout 和 retry 機制"""
    
    def __init__(
        self,
        timeout: int = 300,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0
    ):
        self.timeout = timeout
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.retryable_errors = ["TIMEOUT", "NETWORK_ERROR", "SERVICE_UNAVAILABLE"]
    
    def _calculate_backoff(self, attempt: int) -> float:
        """計算指數退避延遲"""
        jitter = random.uniform(0, 0.5)
        return min(self.base_delay * (2 ** attempt) + jitter, self.max_delay)
    
    def _is_retryable(self, error_code: str) -> bool:
        """判斷錯誤是否可重試"""
        return error_code in self.retryable_errors
    
    def execute(self, task_func: Callable, *args, **kwargs) -> dict:
        """
        執行任務，自動處理 timeout 和 retry
        
        參數:
            task_func: 要執行的任務函數
            *args, **kwargs: 傳給任務函數的參數
        
        返回:
            SubagentResult 格式的字典
        """
        last_error = None
        start_time = time.time()
        
        for attempt in range(self.max_retries + 1):
            try:
                # 執行任務
                result = task_func(*args, **kwargs)
                
                return {
                    "status": "success",
                    "session_key": f"sess_{int(start_time)}",
                    "error": None,
                    "result": result,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "attempts": attempt + 1,
                    "duration_ms": int((time.time() - start_time) * 1000)
                }
                
            except Exception as e:
                error_code = getattr(e, "code", "SYSTEM_ERROR")
                last_error = e
                
                if not self._is_retryable(error_code):
                    # 不可重試的錯誤，立即返回
                    return {
                        "status": "error",
                        "session_key": f"sess_{int(start_time)}",
                        "error": {
                            "code": error_code,
                            "message": str(e),
                            "details": {"attempt": attempt + 1}
                        },
                        "result": None,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "attempts": attempt + 1,
                        "duration_ms": int((time.time() - start_time) * 1000)
                    }
                
                # 檢查是否還有重試機會
                if attempt < self.max_retries:
                    delay = self._calculate_backoff(attempt)
                    time.sleep(delay)
                else:
                    # 已達最大重試次數
                    return {
                        "status": "error",
                        "session_key": f"sess_{int(start_time)}",
                        "error": {
                            "code": "MAX_RETRIES_EXCEEDED",
                            "message": f"已重試 {self.max_retries} 次，仍失敗: {str(e)}",
                            "details": {"original_error": error_code}
                        },
                        "result": None,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "attempts": attempt + 1,
                        "duration_ms": int((time.time() - start_time) * 1000)
                    }
        
        # 不應執行到這裡
        return {
            "status": "error",
            "session_key": f"sess_{int(start_time)}",
            "error": {"code": "UNKNOWN", "message": "Unexpected error"},
            "result": None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
```

---

## ⚙️ sessions_spawn 整合建議

```python
# 建議的 sessions_spawn 呼叫格式
def spawn_with_retry(agentId, task, config=None):
    """
    帶有 timeout 和 retry 的 sessions_spawn 包裝函數
    
    參數:
        agentId: 目標 agent ID
        task: 任務描述
        config: {
            "timeout": 300,        # 秒
            "max_retries": 3,
            "retry_delays": [1, 2, 4]  # 自定義退避序列
        }
    """
    default_config = {
        "timeout": 300,
        "max_retries": 3,
        "retry_delays": [1, 2, 4]
    }
    config = {**default_config, **(config or {})}
    
    executor = SubagentExecutor(
        timeout=config["timeout"],
        max_retries=config["max_retries"]
    )
    
    # 這裡應該呼叫實際的 sessions_spawn
    # return sessions_spawn(agentId=agentId, task=task, timeout=config["timeout"])
    pass
```

---

## 📊 預期效益

1. **防止系統資源被長期佔用**
   - Sub-agent 預設 5 分鐘 Timeout
   - 超過 Timeout 自動終止

2. **提升整體穩定性**
   - 網路瞬斷等暫時性錯誤自動重試
   - 指數退避避免風暴效應

3. **便於問題排查**
   - 完整記錄嘗試次數和耗時
   - 區分可重試和不可重試錯誤

4. **提高任務成功率**
   - 瞬間錯誤可自動恢復
   - 使用者無需手動重試

---

## 📝 實作檢查清單

- [x] 定義 Timeout 分級策略
- [x] 實作指數退避演算法
- [x] 建立 Retry 流程圖
- [x] 提供完整 Python 實作
- [x] 定義 sessions_spawn 整合建議
