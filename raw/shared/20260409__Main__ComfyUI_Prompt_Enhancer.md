# ComfyUI-Prompt_Enhancer - 提示詞增強節點

## 基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | JetterTW |
| **GitHub** | https://github.com/JetterTW/ComfyUI-Prompt_Enhancer |
| **功能** | 將簡單描述自動擴展為細節豐富的視覺提示詞 |
| **License** | MIT |

---

## 這是什麼？

一個專為 **ComfyUI** 設計的提示詞增強節點，透過連接 LLM 將使用者的簡單描述自動擴展為細節豐富、高品質的視覺提示詞。

---

## 核心功能

### 🌓 雙語/多語言支援
- 一次生成**英文 Prompt**（用於繪圖）
- 並提供**繁體或簡體中文對照**
- 兼顧繪圖實用性與視覺理解

### ⚙️ 高度靈活性
| 項目 | 說明 |
|------|------|
| 自訂模型 | 直接在節點上指定 model_name（如 gemma4, gpt-4o, llama3）|
| 自訂端點 | 支援本地（LM Studio, Ollama）或遠端伺服器 |
| 自訂指令 | 透過 system_prompt 定義 LLM 的角色與風格 |

### 🔌 全兼容 API 介面
- 採用 **OpenAI API 標準格式**
- 支援幾乎所有主流 LLM 後端

### 🛡️ 穩定輸出
- 內建強大的 JSON 解析與 Markdown 清理機制
- 確保輸出結果能直接被 ComfyUI 節點讀取

---

## 安裝方式

```bash
# 進入 ComfyUI/custom_nodes 目錄
cd ComfyUI/custom_nodes

# Git 下載
git clone https://github.com/JetterTW/ComfyUI-Prompt_Enhancer.git

# 安裝依賴
pip install -r requirements.txt

# 重啟 ComfyUI
```

---

## 參數說明

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| user_prompt | STRING | A girl in a coffee shop | 原始描述 |
| system_prompt | STRING | You are a professional... | 角色與任務指令 |
| api_url | STRING | http://127.0.0.1:1234/v1/chat/completions | LLM API 端點 |
| model_name | STRING | ngemma4 | 模型名稱 |
| api_key | STRING | not-needed | API 金鑰 |
| max_new_tokens | INT | 2048 | 生成文字最大長度 |
| temperature | FLOAT | 0.7 | 創意程度（0.0-2.0）|

---

## 使用範例

### 本地 Ollama
```yaml
api_url: http://127.0.0.1:1234/v1/chat/completions
model_name: local-model
```

### 遠端 Gemma 4
```yaml
api_url: http://192.168.1.9:8000/v1/chat/completions
model_name: gemma4
```

### 使用流程
1. **Input**：使用 LLM Prompt Enhancer 節點輸入簡單想法
2. **Generation**：將英文 Prompt 輸出端連接至 CLIP Text Encode
3. **Review**：將繁體/簡體中文 Prompt 輸出端連接至 Show Text 節點

---

## 系統提示詞範例

參考 `SystemPrompt.md` 有一些系統提示詞範例。

---

## 注意事項

| 項目 | 說明 |
|------|------|
| **URL 格式** | 確保 API URL 指向 `/chat/completions` 結尾的完整路徑 |
| **網路環境** | 連接遠端 IP 時，確保網路暢通且 Port 已開啟 |
| **模型選擇** | 建議使用 7B 以上的模型以獲得最佳品質 |

---

## 與蘇茉家族的關係

| 項目 | 說明 |
|------|------|
| **AI 繪圖** | ComfyUI 是一個 AI 繪圖工具 |
| **提示詞增強** | 蘇茉家族可以研究這個概念 |
| **多語言支援** | 雙語輸出是個很好的功能 |

---

## 標籤

#知識儲備 #ComfyUI #PromptEnhancer #提示詞增強 #AI繪圖 #LLM #Ollama #Gemma4 #多語言

---

*記錄者：總管蘇茉*
*時間：2026-04-09 17:09*
