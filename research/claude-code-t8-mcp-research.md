# claude-code-t8 MCP 架構研究

日期：2026-04-05
來源：https://github.com/T8mars/claude-code-t8

---

## 警告
- 基於 Claude Code 洩漏原始碼
- 版權歸 Anthropic 所有，僅供技術研究
- 不得用於商業用途

---

## 核心檔案結構

```
src/services/mcp/
├── client.ts              # MCP 客戶端主體
├── config.ts             # 設定管理（.mcp.json）
├── types.ts              # 類型定義
├── auth.ts               # OAuth 認證
├── utils.ts              # 工具函式
├── InProcessTransport.ts # 行程內傳輸
├── StdioClientTransport.ts  # STDIO 傳輸
├── StreamableHTTPClientTransport.ts # HTTP 傳輸
├── SSEClientTransport.ts # SSE 傳輸
└── SdkControlTransport.ts # SDK 控制傳輸
```

---

## 關鍵技術亮點

### 1. 多傳輸協定支援

| 傳輸類型 | 用途 |
|---------|------|
| StdioClientTransport | 本地 STDIO 服務（Python 腳本等）|
| StreamableHTTPClientTransport | HTTP Streamable API |
| SSEClientTransport | Server-Sent Events |
| WebSocket | WebSocket 傳輸 |

### 2. 設定檔案管理

```typescript
// 寫入 .mcp.json（原子性寫入）
- 先寫入暫存檔
- flush to disk
- atomic rename
```

```typescript
// 自動偵測 server signature 做去重
- STDIO: `stdio:${command_array}`
- URL: `url:${unwrapCcrProxyUrl(url)}`
```

### 3. OAuth 認證整合

- `@modelcontextprotocol/sdk/client/auth.js` 的 `UnauthorizedError`
- token refresh 機制
- 401 錯誤處理

### 4. MCP 工具包裝

- `MCPTool` 類別封裝所有 MCP 工具
- `buildMcpToolName()` 建立工具名
- `normalizeNameForMCP()` 名稱正規化
- 輸出截斷（MAX_MCP_DESCRIPTION_LENGTH = 2048）

---

## 可借鑒的設計

| 設計 | 說明 |
|------|------|
| 多傳輸協定 | 類似 OpenClaw 的 tool transport abstraction |
| 設定檔分離 | `.mcp.json` 管理，與 OpenClaw plugin 系統類似 |
| Session 過期處理 | `isMcpSessionExpiredError()` 偵測 404 + JSON-RPC code |
| 原子性寫入 | temp file + atomic rename |
| Server Signature | 去重機制 |

---

## 蘇茉家族的 MCP 現況

蘇茉家族目前使用：
- Hermite MCP Server（工程師蘇茉主導）
- 透過 OpenClaw 的 MCP 整合

---

## 潛在改進方向

1. **多傳輸協定支援**
   - 目前主要支援 Stdio
   - 可考慮支援 HTTP Streamable

2. **設定檔管理**
   - 學習 .mcp.json 的原子性寫入
   - 學習 signature 去重機制

3. **錯誤處理**
   - 學習 session 過期偵測
   - 學習 401 自動 refresh

4. **工具描述截斷**
   - 借鑒 MAX_MCP_DESCRIPTION_LENGTH = 2048
   - 避免過長的 tool description 佔用 token

---

## 總結

這個專案的 MCP 整合做得相當完善，特別是：
- 多傳輸協定的抽象
- 設定檔的原子性寫入
- OAuth 認證整合

蘇茉家族可以借鑒這些設計來強化自己的 MCP 系統，但不需要抄襲程式碼。
