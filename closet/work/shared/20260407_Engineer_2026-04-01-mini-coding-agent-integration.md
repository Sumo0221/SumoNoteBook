# Mini Coding Agent 整合 OpenClaw 研究報告

**日期**：2026-04-01
**研究人**：工程師蘇茉
**主題**：將 mini coding agent 整合進 OpenClaw 成為內建工具

---

## 1. OpenClaw 工具系統架構

### 三層系統

OpenClaw 的工具有三個層次：

| 層次 | 說明 | 實作位置 |
|------|------|---------|
| **Tools** | LLM 可呼叫的函式（類型化） | Plugin SDK `api.registerTool()` |
| **Skills** | Markdown 文件，注入 system prompt | `~/.openclaw/skills/*.md` |
| **Plugins** | 完整的插件系統（tools/channels/providers） | `~/.openclaw/extensions/` |

### 現有相關工具

- **`exec` tool**：執行 shell 命令，已支援 Codex、Claude Code、Pi 等外部 coding agent
- **`sessions_spawn`**：背景執行其他 agent 的內建工具
- **Plugin SDK**：`api.registerTool()` 讓插件註冊新工具

### Plugins 載入位置

```
~/.openclaw/extensions/       ← 本地插件
~/.openclaw/workspace/plugins/ ← 工作區插件
plugins.load.paths             ← 自定義路徑
node_modules/                  ← NPM 安裝的插件
```

---

## 2. 整合方案比較

| 方案 | 描述 | 複雜度 | 優點 | 缺點 |
|------|------|--------|------|------|
| **A：Plugin Tool** | 包裝成 OpenClaw 工具 | 中 | 其他蘇茉直接 `call mini_coding_agent()` 即可 | 需要 Plugin 開發 |
| **B：Subagent** | 用 `sessions_spawn` 執行 | 低 | 直接用現有 API | 會創建另一個 LLM agent，不是直接執行 mini coding agent |
| **C：Slash Command** | `/code` 指令觸發 | 低 | 使用簡單直觀 | 語法不如 tool 靈活 |

**結論**：**方案 A（Plugin Tool）最佳**，其他蘇茉可以像使用 `exec` 一樣直接呼叫 `mini_coding_agent(tool_call)`。

---

## 3. 實作產出

### Plugin 位置

```
~/.openclaw/extensions/openclaw-mini-coding-agent/
├── openclaw.plugin.json   # 插件清單（包含 configSchema）
├── package.json            # NPM package
├── SKILL.md               # 技能文件
└── src/
    └── index.ts            # 插件入口點
```

### Config 更新

在 `~/.openclaw/openclaw.json` 新增：
```json5
"plugins": {
  "load": {
    "paths": [
      // ... 現有路徑 ...
      "C:\\Users\\rayray\\.openclaw\\extensions\\openclaw-mini-coding-agent"
    ]
  },
  "entries": {
    // ...
    "openclaw-mini-coding-agent": {
      "enabled": true,
      "config": {}
    }
  }
}
```

### 工具參數

```typescript
mini_coding_agent(
  task: string,           // 必填：任務描述
  workdir?: string,        // 可選：工作目錄（預設 mini_coding_agent 目錄）
  max_iterations?: number  // 可選：最大迭代次數（預設 20）
)
```

### 技術實現

- 使用 Node.js `child_process.execSync` 執行 Python CLI
- Python 命令：`python main.py --task "..." --provider minimax --max-iterations N --quiet`
- 輸出解析：`Agent: {response}` 格式
- Windows UTF-8 處理：`PYTHONIOENCODING=utf-8` 環境變數
- 錯誤處理：超時 5 分鐘，捕獲 stderr
- 工具標記為 `optional: true`，需要用戶加入 `tools.allow` 才能啟用

---

## 4. 啟用方式

### Step 1：重啟 Gateway

```bash
openclaw gateway restart
```

### Step 2：在 config 中啟用工具

在 `tools.allow` 加入 `"mini_coding_agent"`：
```json5
{
  tools: {
    allow: ["mini_coding_agent", "..."]
  }
}
```

### Step 3：其他蘇茉使用方式

**直接呼叫（Tool）：**
```
mini_coding_agent(
  task="Fix the bug in auth.py where login fails with special characters",
  workdir="C:/my-project"
)
```

**透過 Skill（自然語言）：**
> 「幫我修一下 login 函式的 bug」
> 「這個功能要怎麼做？」
> 「幫我開一個新的 REST API」

---

## 5. Mini Coding Agent 功能

**位置**：`C:/butler_sumo/Tools/mini_coding_agent/`

**工具集**：
- ReadTool：讀取檔案
- WriteTool：寫入檔案
- EditTool：編輯檔案（regex + fuzzy matching）
- BashTool：執行命令（Unix → Windows 自動翻譯）
- WebSearchTool：透過 SearXNG 搜尋
- WebFetchTool：抓取網頁內容
- PythonREPLTool：執行 Python 程式碼

**Provider**：
- MockProvider（測試用）
- OpenRouterProvider
- MiniMaxProvider（目前使用）

---

## 6. 待老爺確認事項

1. ✅ Config 已更新，需要重啟 Gateway 生效
2. ⚠️ Plugin 需要編譯 TypeScript？OpenClaw 原生支援 TypeScript 執行
3. ⚠️ 啟動後需要驗證工具是否正確載入

---

*整理者：工程師蘇茉*
*研究時間：2026-04-01*
