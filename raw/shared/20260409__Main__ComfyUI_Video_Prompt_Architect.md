# ComfyUI-Video-Prompt-Architect - 影片提示詞建築師

## 基本資訊

| 項目 | 內容 |
|------|------|
| **作者** | JetterTW |
| **GitHub** | https://github.com/JetterTW/ComfyUI-Video-Prompt-Architect |
| **功能** | 自動生成描述影像轉場、運鏡、光影變化與風格演進的高品質影片提示詞 |
| **License** | MIT |

---

## 這是什麼？

專為**影片生成工作流**設計的高級 ComfyUI 節點。透過多模態大型語言模型 (Multimodal LLM) 同時分析「起始圖片」與「結束圖片」，自動生成高品質影片提示詞。

---

## 與 Prompt_Enhancer 的關係

| 工具 | 用途 |
|------|------|
| **Prompt_Enhancer** | 靜態圖片提示詞增強 |
| **Video-Prompt-Architect** | 動態影片轉場提示詞生成 |

---

## 核心功能

### 🖼️ 多模態視覺分析
- 獨特的**雙圖輸入機制**（起始圖 + 結束圖）
- LLM 能理解從第一張圖到第二張圖之間的**動態演變趨勢**

### 🎬 電影級描述
| 項目 | 說明 |
|------|------|
| Camera Movement | 自動運鏡方式 |
| Lighting Transitions | 光影轉換 |
| 環境氛圍 | 細節擴充 |

### 🎭 角色導向生成
- 透過 `system_role_instruction` 定義 LLM 的專業身分
- 例如：電影導演、MV 導演、特效專家

### 🌓 三語輸出機制
- **英文 Prompt**：用於影片生成模型
- **繁體中文 Prompt**：內容理解
- **簡體中文 Prompt**：內容理解

### 🔌 全兼容 API 介面
- OpenAI API 標準格式
- 支援 LM Studio、Ollama、vLLM 等

### 🛡️ 穩定 JSON 解析
- 內建強大的 JSON 解析機制
- 精準拆分至三個不同輸出埠

---

## 安裝方式

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/JetterTW/ComfyUI-Video-Prompt-Architect.git
pip install -r requirements.txt
重啟 ComfyUI
```

---

## 參數說明

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| start_image | IMAGE | - | 影片起始幀圖片 |
| end_image | IMAGE | - | 影片結束幀圖片（可省略）|
| user_description | STRING | A sunset to starry night | 原始轉場構想 |
| system_role_instruction | STRING | You are a professional... | LLM 角色設定 |
| api_url | STRING | 127.0.0.1:1234/v1/chat/completions | API 端點 |
| model_name | STRING | gemma4 | 多模態模型名稱 |
| api_key | STRING | not-needed | API 金鑰 |
| max_new_tokens | INT | 2048 | 生成文字最大長度 |
| temperature | FLOAT | 0.7 | 創意程度（0.0-2.0）|

---

## 使用範例

### 本地 Ollama
```yaml
api_url: http://127.0.0.1:1234/v1/chat/completions
model_name: local-vision-model
```

### 電影導演角色
```yaml
system_role_instruction: You are a professional Cinematographer.
api_url: http://192.168.1.9:8000/v1/chat/completions
model_name: gemma4
```

### 使用流程
1. **Input**：輸入起始圖、結束圖與轉場想法
2. **Generation**：將 `prompt_en` 輸出端連接至影片生成節點
3. **Review**：將 `prompt_zh_tw` 輸出端連接至 Show Text 節點

---

## 重要提醒

| 項目 | 說明 |
|------|------|
| **模型支援** | 務必使用支援 Vision（多模態）功能的模型 |
| **URL 格式** | 確保 API URL 指向 `/chat/completions` 結尾 |
| **網路環境** | 確認網路連線暢通且 Port 已開啟 |

---

## JetterTW 專案系列

| 專案 | 功能 |
|------|------|
| **Prompt_Enhancer** | 靜態圖片提示詞增強 |
| **Video-Prompt-Architect** | 動態影片轉場提示詞 |

---

## 標籤

#知識儲備 #ComfyUI #VideoPromptArchitect #影片生成 #轉場提示詞 #多模態 #LLM #電影運鏡 #JetterTW

---

*記錄者：總管蘇茉*
*時間：2026-04-09 17:18*
