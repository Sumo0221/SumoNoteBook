# Khazix Skills

**研究日期**：2026-04-20 10:18:12
**來源**：https://github.com/KKKKhazix/khazix-skills
**標籤**：技術, 機器學習, AI

---

## 📌 關鍵資訊
標題：[Khazix Skills]
來源：https://github.com/KKKKhazix/khazix-skills
日期：未指定
摘要：Khazix 提供了两种工具箱：“Prompts”和“Skills”，旨在将积累的方法论转化为可复用的工具。"Prompts"是一种轻量级的框架，适用于任何AI对话或深度研究；而"Skills"则包含结构化的指令集，安装后智能代理会自动加载使用。Khazix 提供了横纵分析法和卡兹克公众号长文写作Skill等技能。
標籤：技術, 機器學習, AI

---

## 📄 原文內容（部分）

```
# Khazix Skills

数字生命卡兹克的 AI 工具箱。

这里是我自己在用的、经过长期打磨的 Prompts 和 Skills，现在决定把它们完整地、一字不改地开源出来。

两种东西，一个目的：把我积累的方法论变成可复用的工具。

- **Prompts** — 轻量级，复制粘贴到任何 AI 对话或 Deep Research 里就能用
- **Skills** — 重量级，遵循 [Agent Skills](https://agentskills.io) 开放标准的结构化指令集，安装后 Agent 会自动加载

## Prompts

| Prompt | 说明 | 用法 | 讲解 |
|--------|------|------|------|
| [**横纵分析法**](./prompts/横纵分析法.md) | 通用深度研究框架，融合历时-共时分析与竞争战略视角，半小时出一份万字级研究报告 | 复制 Prompt，修改「研究对象」，丢进任何支持 Deep Research 的模型 | [公众号文章](https://mp.weixin.qq.com/s/Y_uRMYBmdLWUPnz_ac7jWA) |

## Skills

| Skill | 说明 | 讲解 |
|-------|------|------|
| [**hv-analysis**](./hv-analysis/) | 横纵分析法深度研究 Skill，自动联网收集信息，纵向追时间深度 + 横向追竞争广度，最终输出排版精美的 PDF 研究报告 | [公众号文章](https://mp.weixin.qq.com/s/Y_uRMYBmdLWUPnz_ac7jWA) |
| [**khazix-writer**](./khazix-writer/) | 卡兹克公众号长文写作 Skill，包含完整的写作风格规则、四层自检体系、内容方法论和风格示例库 | [公众号文章](https://mp.weixin.qq.com/s/AtxGrii_K-nzkwUM9SNhEg) |

### Skill 安装方式

**通过 Agent 安装**

在 Claude Code、Codex、OpenClaw 等支持 Skill 的 Agent 中，直接对话：

```
安装这个 skill：https://github.com/KKKKhazix/khazix-skills
```

**手动安装**

1. 在本仓库的 [Releases](https://github.com/KKKKhazix/khazix-skills/releases) 页面下载对应 Skill 的 `.skill` 安装包
2. 将 `.skill` 文件拖动到对应工具的 Skills 目录下

各工具的 Skills 安装路径：

| 工具 | 路径 |
|------|------|
| Claude Code | `~/.claude/skills/` |
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |

## License

[MIT](./LICENSE)

...
```

---

## 🔬 四層分析

### 第一層：白話解構
這篇文章是在分享卡兹克（Khazix）積累的Prompt和技能，這些工具旨在幫助用戶進行深度研究和寫作。文章提到了一些具體的例子，如橫縱分析法，以及它們如何在不同的平臺上使用。

### 第二層：技術驗證
- **claims**：
  - 横縱分析法是一個可以輕鬆複製粘貼到任何深層研究模型中的通用框架。
  - hv-analysis技能是一種自動化收集信息並生成專業報告的工具，適合深度研究和寫作。
  - khazix-writer是一個包含完整的寫作风格規則、四層自檢體系和內容方法論的長文撰寫工具。

- **有根據的 claims**：
  - 横縱分析法能夠在數分鐘內生成一份萬字級的報告，適用範圍廣泛。
  - hv-analysis技能支持用戶通過自動化過程來生成專業研究報告。
  - khazix-writer提供了一整套完整的寫作工具和規則，包括寫作風格、四層自檢體系等。

- **邏輯漏洞或偏見**：
  - 無明顯的邏輯漏洞。但需要確認這些Prompt和技能在實際使用中的有效性。
  - 横縱分析法的應用範圍和深度研究報告的质量未進一步評估，hv-analysis技能的自動化過程可能會受到網絡速度等因素的影響。

### 第三層：核心洞察
- **最重要的3個 insight**：
  - 洞察一：橫縱分析法是一個高效的通用框架，適用於多種應用場景。
  - 洞察二：hv-analysis技能能夠提供一個自動化的解決方案來進行深度研究和寫作，提高效率。
  - 洞察三：khazix-writer提供了完整的寫作文本方法論和規則，對用戶有很高的指導意義。

- **讀者最有價值的啟發**：
  - 如何使用這些工具來提高自己在多個領域的研究和寫作效率。
  - 留意這些工具在實際應用中的有效性及可擴展性。

- **如果只能帶走一件事，是什麼？**
  - 如果我只能選一個工具帶走，會選擇hv-analysis技能，因為它提供了一種自動化的解決方案來進行深度研究和寫作，對用戶最有價值。

### 第四層：系統整合建議
#### 這個東西怎麼用在我們現有的系統？
- **作為模組**：
  - 我們可以將這篇文章中的hv-analysis技能打包成一個模組，並在公司內部的AI工具中實現自動化的研究和寫作支持。
  
- **一條規則**：
  - 在公司内部建立一套使用這些技能的規則，以確保其有效性和可持續性。

#### 具體建議怎麼實作
- **通過Agent安裝**：
  - 將hv-analysis技能打包成一個`.skill`文件，并將其放在專門為這個工具設置的安裝路徑中。例如，在Claude Code、Codex或OpenClaw等支持Skill的工具上實現自動化。
- **在本仓库的Releases頁面下載**：
  - 建立一個清單，列明各個工具和其技能的相關信息，方便用戶進行查找和使用。

- **安裝步驟**：
  1. 在Claude Code中，通過直接對話命令來安裝技能。
  2. 在OpenClaw或Codex等工具上，將`.skill`文件拖到指定的Skills目錄下进行安装。

---

## 💾 元資料

- **研究時間**：2026-04-20 10:18:12
- **來源 URL**：https://github.com/KKKKhazix/khazix-skills
- **處理模型**：qwen2.5:3b (本地 Ollama)

---

*由 EnhancedStudy 技能自動產生*
