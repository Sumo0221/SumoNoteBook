# DeerFlow 架構研究報告：Sub-agent 派遣機制與 Skills 系統

**研究日期：** 2026-04-03  
**研究人：** 教授蘇茉  
**研究目標：** ByteDance DeerFlow 開源專案（https://github.com/bytedance/deer-flow）

---

## 一、DeerFlow Sub-agent 派遣機制

### 1.1 核心架構組件

DeerFlow 的 Sub-agent 系統由以下核心組件構成：

| 組件 | 檔案位置 | 功能 |
|------|----------|------|
| `task_tool.py` | `tools/builtins/task_tool.py` | 派遣工具（Agent 呼叫的工具） |
| `executor.py` | `subagents/executor.py` | 執行引擎（非同步執行 + 背景任務） |
| `config.py` | `subagents/config.py` | Sub-agent 配置定義 |
| `registry.py` | `subagents/registry.py` | Sub-agent 登錄與配置管理 |
| `builtins/` | `subagents/builtins/` | 內建 Sub-agent 定義 |

### 1.2 Sub-agent 派遣流程

```
主 Agent (Lead Agent)
    │
    ├── 呼叫 task 工具
    │   Args: description, prompt, subagent_type, max_turns?
    │
    ├── SubagentExecutor 建立
    │   ├── 根據 subagent_type 取得 SubagentConfig
    │   ├── 過濾工具清單（allowlist/denylist）
    │   ├── 繼承父 Agent 模型（可選）
    │   └── 注入 Skills Prompt Section
    │
    ├── 背景執行（execute_async）
    │   ├── ThreadPoolExecutor（非同步排程）
    │   ├── 計時器控制（timeout_seconds）
    │   └── Task ID 生成
    │
    └── 結果彙整
        ├── task_started → 任務啟動事件
        ├── task_running → AI 訊息即時串流
        ├── task_completed → 任務成功結果
        ├── task_failed → 失敗原因
        └── task_timed_out → 逾時錯誤
```

### 1.3 兩階段審查設計

DeerFlow 的 Sub-agent 系統**並非兩階段審查**。經過實際研究原始碼，DeerFlow 採用的是：

**單階段 + 即時回饋機制：**

1. **Task Tool 內建審查：**
   - 可用性檢查（subagent 是否存在）
   - 安全性檢查（bash subagent 需要 host_bash 權限）
   - 工具過濾（禁止嵌套：`disallowed_tools=["task"]`）

2. **後端輪詢機制（Backend Polling）：**
   - Tool 本身是 `async def task_tool()`
   - 內部每 5 秒輪詢一次，直到任務完成
   - 最大輪詢次數 = `(timeout_seconds + 60) / 5`

3. **即時串流事件（Real-time Streaming）：**
   - `task_started`：任務啟動
   - `task_running`：每個 AI 訊息產生時立即發送
   - 這些事件透過 LangGraph 的 `get_stream_writer()` 發送

**「兩階段審查」可能指的是：**
- 第一階段：Task Tool 接收任務並驗證
- 第二階段：後端執行並輪詢結果，最終返回給主 Agent

### 1.4 結果彙整機制

DeerFlow 的 Sub-agent 結果蒐集非常完善：

```python
@dataclass
class SubagentResult:
    task_id: str           # 任務唯一識別
    trace_id: str          # 分散式追蹤 ID
    status: SubagentStatus # PENDING/RUNNING/COMPLETED/FAILED/TIMED_OUT
    result: str | None     # 最終文字結果
    error: str | None      # 錯誤訊息
    started_at: datetime   # 開始時間
    completed_at: datetime # 完成時間
    ai_messages: list[dict] # 所有 AI 訊息（用於即時串流）
```

**結果彙整特點：**
- 完整保留執行過程的所有 AI 訊息
- 支援串流輸出（每個訊息即時傳送）
- 多種失敗狀態區分（FAILED vs TIMED_OUT）

### 1.5 錯誤處理與重試機制

| 錯誤類型 | 處理方式 |
|----------|----------|
| 子代理執行失敗 | `SubagentStatus.FAILED` + 錯誤訊息 |
| 執行逾時 | `SubagentStatus.TIMED_OUT` + 逾時時長 |
| 任務消失 | 錯誤訊息 + cleanup |
| 輪詢逾時 | 安全網：最多輪詢 `(timeout + 60) / 5` 次 |

**重試機制：** DeerFlow **本身不包含自動重試**，而是依賴：
- 計時器超時設定（`timeout_seconds`，預設 900 秒 = 15 分鐘）
- 最大輪數限制（`max_turns`，預設 50）
- 主 Agent 可以再次呼叫 task tool 進行重試

### 1.6 內建 Sub-agent 類型

```python
BUILTIN_SUBAGENTS = {
    "general-purpose": SubagentConfig(
        name="general-purpose",
        description="複雜多步驟任務，需要探索與行動兼具",
        system_prompt="你是一個通用子代理...",
        tools=None,  # 繼承所有工具
        disallowed_tools=["task", "ask_clarification", "present_files"],
        model="inherit",  # 繼承父模型
        max_turns=50,
        timeout_seconds=900,
    ),
    "bash": SubagentConfig(
        name="bash",
        description="命令執行專家",
        # ...
    ),
}
```

---

## 二、DeerFlow Skills 系統

### 2.1 SKILL.md 格式

```yaml
---
name: skill-name
description: 觸發條件和功能描述（用於技能發現）
license: MIT  # 可選
---

# Skill 主體（Markdown 格式）

## 內容結構（範例）
### When to Use
### How to Use
### Examples
### Tips
```

**解析方式：**
- YAML Frontmatter：`name` + `description`（必要欄位）
- 主體：Markdown 格式，自由結構
- Parser 位於：`skills/parser.py`

### 2.2 三層載入機制（Progressive Disclosure）

```
第一層：Metadata（name + description）
       ↓ ~100 words，Always in context
       
第二層：SKILL.md 主體
       ↓ <500 lines ideal，When skill triggers
       
第三層：Bundle Resources（scripts/, references/, assets/）
       ↓ Unlimited，As needed
```

### 2.3 技能發現機制

DeerFlow 的技能發現有兩種方式：

**1. 描述匹配觸發：**
- Agent 系統提示包含所有 Skills 的 `name` + `description`
- 當描述關鍵字匹配時，載入對應的 SKILL.md

**2. find-skills 技能：**
```markdown
# Find Skills - 技能發現技能

When to Use:
- 用戶問「how do I do X」
- 用戶問「find a skill for X」
- 用戶表達興趣擴展能力

How to Use:
bash npx skills find [query]
```

**Skills 生態系：**
- 發布平台：https://skills.sh/
- 安裝方式：`bash /path/to/skill/scripts/install-skill.sh owner/repo@skill-name`
- 封裝格式：`.skill` 檔案（ZIP 壓縮，包含 SKILL.md）

### 2.4 技能組合能力

DeerFlow 支援技能注入到 Sub-agent：

```python
# task_tool.py 中的技能注入
skills_section = get_skills_prompt_section()
if skills_section:
    overrides["system_prompt"] = config.system_prompt + "\n\n" + skills_section
```

**技能組合方式：**
1. **多技能同時啟用：** 所有啟用的 Skills 都會出現在 Lead Agent 的 system prompt
2. **Sub-agent 技能隔離：** Sub-agent 預設繼承所有 Skills（除非配置過濾）
3. **技能分類：** `skills/public/`（內建）vs `skills/custom/`（用戶安裝）

### 2.5 技能安裝與驗證

```python
# 安裝流程
install_skill_from_archive(zip_path) → 
    safe_extract_skill_archive() →  # 安全檢查
    _validate_skill_frontmatter() →  # 驗證
    shutil.copytree() → custom_dir/
```

**安全驗證：**
- ZIP 路徑安全：防止 `..` 目錄穿越
- 符號連結：跳過不執行
- 大小限制：最大 512MB
- Frontmatter 驗證：確保 `name` + `description` 存在

---

## 三、蘇茉家族 vs DeerFlow 架構對比

### 3.1 Sub-agent 系統對比

| 項目 | 蘇茉現有 | DeerFlow | 差距分析 |
|------|----------|----------|----------|
| **派遣方式** | `sessions_spawn` 直接喚醒 | `task` 工具（LangChain Tool） | 蘇茉是跨 Agent 派遣；DeerFlow 是同進程 Sub-agent 派遣 |
| **審查機制** | 無明確審查 | Task Tool 內建驗證（可用性、安全性） | **蘇茉落後** |
| **結果彙整** | 依賴 Agent 自然回傳 | 結構化 `SubagentResult` + 即時串流 | **蘇茉落後** |
| **錯誤處理** | 基本（例外往上拋） | 多狀態區分（FAILED/TIMED_OUT）+ 錯誤訊息 | **蘇茉落後** |
| **逾時控制** | 無法指定 | `timeout_seconds` + `max_turns` 雙重控制 | **蘇茉落後** |
| **工具過濾** | 無 | allowlist/denylist 機制 | **蘇茉落後** |
| **執行隔離** | 依賴作業系統（不同行程） | ThreadPoolExecutor（同行程，不同執行緒） | 各有優劣 |
| **追蹤能力** | 無 | `trace_id` 分散式追蹤 | **蘇茉落後** |
| **狀態持久化** | 無 | Background task 結果持久化於記憶體 | **蘇茉落後** |

### 3.2 Skills 系統對比

| 項目 | 蘇茉現有 | DeerFlow | 差距分析 |
|------|----------|----------|----------|
| **格式** | SKILL.md（YAML frontmatter + Markdown） | SKILL.md（YAML frontmatter + Markdown） | **相近** |
| **觸發方式** | 讀取檔案並掃描描述關鍵字 | 描述關鍵字匹配（LLM 自然觸發） | **蘇茉略優**（明確的掃描機制） |
| **發現機制** | 無 | `find-skills` 技能 + skills.sh 生態系 | **蘇茉落後** |
| **組合能力** | 無 | 技能可注入 Sub-agent 執行 | **蘇茉落後** |
| **安裝機制** | 無 | `.skill` 封裝格式 + 安全驗證 | **蘇茉落後** |
| **啟用控制** | 無 | `extensions_config.json` 動態控制 | **蘇茉落後** |
| **目錄結構** | `~/.openclaw/skills/` | `skills/public/` + `skills/custom/` | DeerFlow 分類更清楚 |
| **三層載入** | 無 | Progressive Disclosure 機制 | **蘇茉落後** |
| **驗證機制** | 無 | 安全驗證（ZIP 穿越、symlink） | **蘇茉落後** |

---

## 四、具體優化建議

### 優化一：建立 Sub-agent 結果結構化回傳機制

**優化什麼：**
為 `sessions_spawn` 的結果建立結構化的 `Result` 格式，而非純文字回傳。

**為什麼值得做：**
目前蘇茉的 Sub-agent 結果只是自然語言文字，無法：
- 區分「成功」與「部分成功」
- 擷取結構化資料（如檔案路徑、數據）
- 支援下游處理的程式化解析

**如何實作：**
```python
# 新增 result_schema.py
@dataclass
class SubagentResult:
    status: str  # "success" | "partial" | "failed" | "timeout"
    summary: str  # 自然語言摘要
    artifacts: list[dict]  # 產出物清單
    errors: list[str]  # 錯誤列表
    trace_id: str  # 追蹤 ID
    metadata: dict  # 額外元資料
```

### 優化二：建立 Skills 觸發描述關鍵字索引

**優化什麼：**
在 Skills 系統中建立描述關鍵字索引，支援更精確的技能發現。

**為什麼值得做：**
目前蘇茉的 Skills 只是被動載入（讀取所有 SKILL.md），沒有：
- 關鍵字索引
- 觸發條件的明確匹配
- `find-skills` 這類主動發現能力

**如何實作：**
```python
# 在 SKILL.md 解析時，建立索引
skills_index = {
    "股票報價": ["stock-price", "股票", "股價", "加權指數"],
    "天氣查詢": ["weather", "天氣", "溫度", "預報"],
    # ...
}

def find_relevant_skills(user_message: str) -> list[str]:
    # TF-IDF 或關鍵字匹配
    # 回傳最相關的 Skills 清單
```

### 優化三：建立任務逾時與重試配置

**優化什麼：**
為 `sessions_spawn` 增加 `timeout` 和 `max_retries` 參數。

**為什麼值得做：**
目前的 `sessions_spawn` 是 fire-and-forget 模式：
- 無法指定任務執行上限時間
- 失敗時無自動重試
- 長時間任務沒有進度追蹤

**如何實作：**
```python
# sessions_spawn 增加參數
sessions_spawn(
    agentId="...",
    task="...",
    timeout_seconds=300,  # 預設 5 分鐘
    max_retries=2,       # 預設不重試
    on_timeout="return_error" | "retry",
)
```

### 優化四：建立 Sub-agent 工具過濾機制

**優化什麼：**
允許主 Agent 對 Sub-agent 進行工具授權控制。

**為什麼值得做：**
安全性與權限控制：
- 不是每個 Sub-agent 都需要所有工具
- 防止 Sub-agent 執行危險操作
- 遵循最小權限原則

**如何實作：**
```yaml
# 在 AGENTS.md 中定義
subagent_permissions:
  researcher:
    allow_tools: ["web_fetch", "read", "search"]
    deny_tools: ["exec", "write", "delete"]
  coder:
    allow_tools: ["read", "write", "exec"]
    deny_tools: []
```

### 優化五：建立 Skills 安裝與驗證系統

**優化什麼：**
建立 `.skill` 封裝格式與安裝機制，支援從外部安裝新技能。

**為什麼值得做：**
- 技能無法從外部輕鬆擴展
- 無法分享和重用其他蘇茉成員的技能
- 缺少安全驗證（ZIP 穿越、恶意代码）

**如何實作：**
1. 定義 `.skill` 封裝格式（ZIP）
2. 建立 `install_skill.py` 安裝腳本
3. 實作安全驗證：
   - 路徑穿越檢查
   - symlink 處理
   - 大小限制
4. 支援 `skills/custom/` 目錄安裝

---

## 五、研究結論

### 5.1 DeerFlow 的優勢

1. **架構完整性高：** Sub-agent + Skills 兩大系統緊密整合
2. **工程品質佳：** 完整的錯誤處理、逾時控制、追蹤機制
3. **Skills 生態系成熟：** skills.sh 平台 + npx skills CLI
4. **安全意識強：** ZIP 驗證、工具過濾、Sandbox 隔離

### 5.2 蘇茉家族的定位

蘇茉家族的 Agent 架構（`sessions_spawn`）與 DeerFlow 的 Sub-agent 架構有本質差異：
- **DeerFlow：** 同進程、不同執行緒的 Sub-agent（高效但需信任）
- **蘇茉家族：** 跨 Agent（行程隔離、獨立上下文，但延遲較高）

這不是優劣之分，而是適用場景不同。蘇茉的架構更適合真正獨立的 Agent 協作。

### 5.3 建議優先順序

| 優先順序 | 優化項目 | 預期效益 | 實作難度 |
|----------|----------|----------|----------|
| 🔴 高 | 優化一：結果結構化 | 提升可靠性、可解析性 | 中 |
| 🔴 高 | 優化三：逾時與重試 | 防止任務卡死 | 低 |
| 🟡 中 | 優化二：Skills 索引 | 精確觸發、減少上下文污染 | 中 |
| 🟡 中 | 優化四：工具過濾 | 安全性提升 | 中 |
| 🟢 低 | 優化五：安裝系統 | 生態擴展 | 高 |

---

## 六、參考資料

- **DeerFlow GitHub：** https://github.com/bytedance/deer-flow
- **Skills 生態系：** https://skills.sh/
- **DeerFlow 官方網站：** https://deerflow.tech/

---

*報告產出：教授蘇茉 @ 先進研究室*
*產出日期：2026-04-03*
