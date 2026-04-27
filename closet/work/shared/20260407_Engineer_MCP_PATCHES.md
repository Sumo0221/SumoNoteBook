# MCP 系統強化 Patch 記錄

## 檔案位置
- Target: `C:\Users\rayray\AppData\Roaming\npm\node_modules\openclaw\dist\pi-embedded-BaSvmUpW.js`

---

## P0: 工具描述截斷

### 目標
在 line 163810 的 tool description 設定處加入長度限制

### 修改前 (line 163807-163811)
```javascript
tools.push({
    name: tool.name,
    label: tool.title ?? tool.name,
    description: tool.description?.trim() || `Provided by bundle MCP server "${serverName}" (${describeStdioMcpServerLaunchConfig(launchConfig)}).`,
    parameters: tool.inputSchema,
```

### 修改後
在 `createBundleMcpToolRuntime` 函數一開始加入 helper function:

```javascript
// P0: 新增 - MCP tool description 截斷
const MAX_MCP_DESCRIPTION_LENGTH = 2048;
function truncateMcpDescription(desc) {
    if (!desc || desc.length <= MAX_MCP_DESCRIPTION_LENGTH) return desc || "";
    return desc.substring(0, MAX_MCP_DESCRIPTION_LENGTH - 3) + "...";
}
```

然後修改 line 163810:
```javascript
description: truncateMcpDescription(tool.description?.trim()) || `Provided by bundle MCP server "${serverName}" (${describeStdioMcpServerLaunchConfig(launchConfig)}).`,
```

---

## P1.1: Server Signature 去重

### 目標
在 `createBundleMcpToolRuntime` 函數中，在啟動 server 前檢查是否已有相同 signature 的 server 已啟動

### 新增函數 (在 createBundleMcpToolRuntime 之前)
```javascript
// P1.1: 新增 - 計算 MCP server signature
function computeMcpServerSignature(serverName, rawServer, launchConfig) {
    if (rawServer.url) return `url:${rawServer.url}`;
    if (launchConfig.command) {
        return `stdio:${launchConfig.command}:${JSON.stringify(launchConfig.args || [])}`;
    }
    return `unknown:${serverName}`;
}
```

### 修改位置 (line 163771 for loop 之前)
```javascript
// P1.1: 新增 - 追蹤已處理的 server signatures
const seenServerSignatures = new Set();

for (const [serverName, rawServer] of Object.entries(loaded.mcpServers)) {
    const launch = resolveStdioMcpServerLaunchConfig(rawServer);
    if (!launch.ok) {
        logWarn(`bundle-mcp: skipped server "${serverName}" because ${launch.reason}.`);
        continue;
    }
    const launchConfig = launch.config;
    
    // P1.1: 新增 - 檢查是否已有相同 signature 的 server
    const serverSignature = computeMcpServerSignature(serverName, rawServer, launchConfig);
    if (seenServerSignatures.has(serverSignature)) {
        logWarn(`bundle-mcp: skipped duplicate server "${serverName}" with signature "${serverSignature}".`);
        continue;
    }
    seenServerSignatures.add(serverSignature);
    
    // ... 現有程式碼繼續
```

---

## P1.2: Session 過期偵測 + 自動重連

### 目標
在 tool execute 時偵測 session 過期錯誤，並自動重連

### 新增函數
```javascript
// P1.2: 新增 - 偵測 MCP session 過期錯誤
function isMcpSessionExpiredError(error) {
    if (!error) return false;
    const errorMessage = error instanceof Error ? error.message : String(error);
    
    // 404 或 session 相關錯誤
    if (errorMessage.includes("404") || 
        errorMessage.includes("session") ||
        errorMessage.includes("Session")) return true;
    
    // JSON-RPC 錯誤碼
    if (typeof error === "object") {
        const e = error;
        if (e.code === -32600 || e.code === -32601 || e.code === -32603) return true;
        // MCP 特定的過期錯誤
        if (e.code === -32000 && errorMessage.includes("expired")) return true;
    }
    
    return false;
}
```

### 修改 execute 函數 (line 163812-163821)
```javascript
execute: async (_toolCallId, input) => {
    try {
        const result = await client.callTool({
            name: tool.name,
            arguments: isRecord(input) ? input : {}
        });
        return toAgentToolResult({
            serverName,
            toolName: tool.name,
            result
        });
    } catch (error) {
        // P1.2: 偵測 session 過期並重試
        if (isMcpSessionExpiredError(error)) {
            logWarn(`bundle-mcp: session expired for tool "${tool.name}", attempting reconnect...`);
            try {
                // 重新連接
                await client.close().catch(() => {});
                await transport.close().catch(() => {});
                await client.connect(transport);
                
                // 重試 tool call
                const result = await client.callTool({
                    name: tool.name,
                    arguments: isRecord(input) ? input : {}
                });
                return toAgentToolResult({
                    serverName,
                    toolName: tool.name,
                    result
                });
            } catch (retryError) {
                logWarn(`bundle-mcp: reconnect failed for tool "${tool.name}": ${String(retryError)}`);
                throw retryError;
            }
        }
        throw error;
    }
}
```

---

## 施作狀態

| 功能 | 狀態 | 備註 |
|------|------|------|
| P0: 工具描述截斷 | ✅ 已完成 | 使用 truncateMcpDescription() 截斷至 2048 字元 |
| P1.1: Server 去重 | ✅ 已完成 | 使用 computeMcpServerSignature() 偵測重複 |
| P1.2: Session 過期偵測 | ✅ 已完成 | 使用 isMcpSessionExpiredError() + 自動重連 |

## 施作時間
- 完成時間: 2026-04-05 21:xx GMT+8
- 備份檔案: `C:\Users\rayray\AppData\Roaming\npm\node_modules\openclaw\dist\pi-embedded-BaSvmUpW.js.backup`

## 注意事項
⚠️ 此修改位於 compiled bundle 中，會在 `npm update openclaw` 後被覆蓋！
如需保留修改，請考慮：
1. 建立 postinstall script 自動重新套用
2. 或向 OpenClaw 開發團隊提出 PR

---

## 施作方式

由於 `pi-embedded-BaSvmUpW.js` 是 compiled bundle，建議的施作方式是：

1. **直接修改** (測試用，會在 npm update 後被覆蓋):
   ```
   直接編輯該檔案
   ```

2. **建立 patch script** (建議):
   ```bash
   # 在 npm update 後執行
   node scripts/apply-mcp-patch.js
   ```

3. **修改原始碼** (長期方案):
   - 在 GitHub repo 修改 TypeScript 原始碼
   - 重新編譯並發布

---

## 施作風險

| 功能 | 風險 | 說明 |
|------|------|------|
| P0 | 低 | 只影響 display description |
| P1.1 | 低 | 只是 skip duplicate servers |
| P1.2 | 中 | 涉及 reconnect 邏輯，可能有 race condition |

---

## 建立 Patch Script

如果需要，我可以建立一個 `apply-mcp-patch.js` script 來自動套用這些修改。
