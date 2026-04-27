# MemPalace - AI 記憶系統

> 日期：2026-04-07
> 來源：https://github.com/milla-jovovich/mempalace
> 標籤：#memory #AI #agent #AAAK #local

---

## 🎯 核心理念

> Every conversation you have with an AI — every decision, every debugging session, every architecture debate — disappears when the session ends.

**解決方案**：儲存一切，讓它可被搜尋。

---

## 🏛️ The Palace（記憶宮殿）概念

借用古希臘演說家使用的方法：把想法放置在想像建築的房間裡，走過建築就能找到想法。

### 結構層次

| 元素 | 說明 |
|------|------|
| **Wing** | 人物或專案（person/project）|
| **Room** | 同一 wing 內的特定主題（auth, billing, deploy）|
| **Hall** | 同 wing 內相關房間的連接 |
| **Tunnel** | 不同 wing 之间房間的連接 |
| **Closet** | 壓縮摘要，指向原始檔案 |
| **Drawer** | 原始verbatim檔案 |

### 核心優點
- 結構本身就能提升檢索 34%
- AI 知道要去哪個 wing 搜尋，不需要遍歷所有關鍵字

---

## 📊 效能數據

| 指標 | 數值 |
|------|------|
| LongMemEval R@5 | **96.6%** |
| Zero API calls | ✅ |
| With Haiku rerank | 100% |
| 成本 | **$0/年**（純本地）|

### vs 其他方案

| 方案 | Tokens loaded | 年費 |
|------|----------------|------|
| Paste everything | 19.5M（無法放入 context）| Impossible |
| LLM summaries | ~650K | $507 |
| MemPalace wake-up | ~170 tokens | $0.70 |
| MemPalace + 5 searches | ~13,500 tokens | $10 |

---

## 🔧 AAAK - AI 壓縮語言

> Not meant to be read by humans — meant to be read by your AI, fast.

- **30x 壓縮**，零資訊損失
- 通用語法，適用於任何文字模型（Claude, GPT, Gemini, Llama, Mistral）
- 不需要 decoder、fine-tuning 或雲端 API
- 純本地運行

---

## 🛠️ 安裝方式

```bash
pip install mempalace

# 初始化
mempalace init ~/projects/myapp

# 挖掘資料
mempalace mine ~/projects/myapp --mode projects
mempalace mine ~/chats/ --mode convos
mempalace mine ~/chats/ --mode convos --extract general

# 搜尋
mempalace search "why did we switch to GraphQL"
```

### MCP 整合

```bash
claude mcp add mempalace -- python -m mempalace.mcp_server
```

19 個工具透過 MCP 供 AI 使用。

---

## 💡 和 SumoNoteBook/ACE 的關聯

| MemPalace | SumoNoteBook/ACE |
|-----------|------------------|
| Wings = Projects | 概念類似 |
| Rooms = Topics | 類似 concepts |
| Closets + Drawers | 類似 Wiki layers |
| Tunnels | 類似 backlinks |
| AAAK 壓縮 | 可以借鑒 |
| 96.6% recall | 可以學習他們的 benchmark |

### 可以學習的地方

1. **結構化提升檢索** - 記憶宮殿結構提升 34% 檢索
2. **壓縮語言 AAAK** - 30x 壓縮但不失資訊
3. **Closet/Drawer 分離** - 壓縮摘要 vs 原始檔案
4. **Benchmarks** - 建立我們自己的評估方式

---

## 📝 備註

這不是米拉·喬沃维奇本人開發的，而是 GitHub 用戶 milla-jovovich。但概念和技術都是真實的。