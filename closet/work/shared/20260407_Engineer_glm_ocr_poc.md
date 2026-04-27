# GLM-OCR POC 報告

**日期**: 2026-04-03  
**執行者**: 工程師蘇茉  
**狀態**: ✅ 安裝完成 | ⏳ 待 API Key

---

## 1. 安裝結果

```bash
pip install glmocr
```

**狀態**: ✅ 成功

安裝的版本：`glmocr-0.1.4`  
相依套件：pypdfium2, portalocker, requests, pydantic, python-dotenv

---

## 2. API Key 申請

### 官網
- **申請網址**: https://open.bigmodel.cn
- **免費額度**: 20,000,000 Tokens（2000萬tokens）

### 定價
| 項目 | 價格 |
|------|------|
| GLM-OCR 版面解析 | **0.2 元 / 百萬 Tokens** |
| 性價比 | 1 元可處理約 2000 張 A4 掃描圖片 |

> 備註：API 輸入輸出同價

### 現有 Key
- 目前系統中**尚無** `ZHIPU_API_KEY`
- 需要老爺前往 https://open.bigmodel.cn 註冊並建立 API Key

---

## 3. SDK 分析

### 支援模式

| 模式 | 說明 | 需要 GPU |
|------|------|----------|
| **MaaS（雲端）** | 透過 Zhipu 雲端 API 處理 | ❌ 不需要 |
| Self-hosted | 自架 OCR API | ✅ 需要 |

### API 端點
- URL: `https://open.bigmodel.cn/api/paas/v4/layout_parsing`
- 模型: `glm-ocr`
- 授權: Bearer Token

### 環境變數設定
```bash
# 主要（推薦）
export ZHIPU_API_KEY=your_api_key_here

# 備援
export GLMOCR_API_KEY=your_api_key_here
```

---

## 4. 使用方式

### Python SDK 用法

```python
import glmocr

# 初始化（使用 API Key）
ocr = glmocr.GlmOcr(api_key="your_api_key")

# 解析圖片
result = ocr.parse("document.png")

# 解析 PDF
result = ocr.parse("document.pdf", start_page_id=1, end_page_id=5)

# 取得 Markdown 結果
print(result.md_results)
```

### CLI 用法
```bash
glmocr parse document.png --api-key your_api_key
```

---

## 5. 功能評估

### ✅ 支援功能
- [x] 圖片 OCR（PNG, JPEG, WEBP）
- [x] PDF 文件解析
- [x] 數學公式辨識（Markdown 格式輸出）
- [x] 表格辨識
- [x] 版面佈局檢測（Layout Detection）
- [x] 原始 Markdown 格式輸出
- [x] 裁剪圖片返回

### 回傳格式
```json
{
  "id": "task_id",
  "model": "glm-ocr",
  "md_results": "## 標題\n\n文字內容...",
  "layout_details": [...],
  "data_info": {...},
  "usage": {
    "tokens": 12345
  }
}
```

---

## 6. 整合評估

### 與蘇茉對話流程整合

**可行方式**：
1. **鉤子鉤住圖片處理**：在收到圖片訊息時，自動呼叫 GLM-OCR
2. **懶人模式**：使用者貼圖後，蘇茉自動偵測並使用 OCR
3. **手動觸發**：使用者傳圖時加上關鍵字（如 `@蘇茉 ocr`）

**建議實作方式**：
- 在訊息處理流程中，偵測含有圖片的訊息
- 優先使用 GLM-OCR 提取文字（而非內建的 vision model）
- 將提取的 Markdown 文字傳給 LLM 回答

### 整合位置建議
```
使用者發送圖片
    ↓
蘇茉接收 → 偵測為課本/作業/試卷
    ↓
呼叫 glmocr.parse(image)
    ↓
取得 Markdown 文字
    ↓
蘇茉用提取的文字回答問題
```

---

## 7. 待辦事項

- [ ] 老爺提供 ZHIPU_API_KEY
- [ ] 實際測試（目前缺 Key 無法 POC）
- [ ] 整合到蘇茉訊息處理流程
- [ ] 設定 .env 檔

---

## 8. 結論

**GLM-OCR 是非常合適的工具**：
- ✅ 安裝簡單，`pip install glmocr` 即可
- ✅ 有免費額度（2000萬 tokens）
- ✅ 價格便宜（0.2元/百萬 tokens，性價比高）
- ✅ 不需要 GPU（MaaS 模式）
- ✅ 支援數學公式、表格、版面分析
- ✅ SDK 設計良好，Python CLI 皆可用

**唯一需要**：老爺去 https://open.bigmodel.cn 申請 API Key
