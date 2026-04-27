# 蘇茉工具擴展評估報告

**日期：** 2026-04-04  
**評估者：** 品管蘇茉  
**對比對象：** Hermes Agent (Nous Research)

---

## 一、Hermes Agent 工具全景圖

Hermes 共有 **40+ 工具**，分為以下類別：

| 類別 | 工具數 | 主要工具 |
|------|--------|----------|
| Web 搜尋/下載 | ~2 | web_search, web_extract |
| 終端機/檔案 | ~5 | terminal, process, read_file, patch, search_files, write_file |
| 瀏覽器自動化 | ~11 | browser_navigate, browser_snapshot, browser_click, browser_vision 等 |
| 媒體生成/分析 | ~3 | vision_analyze, image_generate, text_to_speech |
| Agent 協作 | ~4 | todo, clarify, execute_code, delegate_task |
| 記憶系統 | ~2 | memory, session_search |
| 排程自動化 | ~1 | cronjob |
| 訊息發送 | ~1 | send_message |
| 智慧家居 | ~4 | ha_call_service, ha_get_state, ha_list_entities, ha_list_services |
| 技能系統 | ~3 | skill_manage, skill_view, skills_list |
| 進階 AI | ~1 | mixture_of_agents |
| RL 訓練 | ~9 | rl_* (環境選擇、訓練控制、監控等) |
| MCP 整合 | 動態 | mcp-<server> 動態工具集 |

---

## 二、蘇茉目前工具現況

### 已有的工具（✓）

| 類別 | 蘇茉工具 | 備註 |
|------|----------|------|
| 檔案讀寫 | read, write, edit | 基礎檔案操作完整 |
| 終端機 | exec, process | 基礎 shell 執行 |
| 瀏�覽器 | browser (snapshot, screenshot, navigate, act) | 有完整瀏覽器控制能力 |
| 訊息發送 | message | Telegram 等平台 |
| 搜尋 | search, search_news, search_images, search_videos, search_repos | 多類型搜尋 |
| 天氣 | weather skill | wttr.in/Open-Meteo |
| 股票 | stock-price skill | 台美股報價 |
| 圖像生成 | baoyu-image-gen skill | OpenAI/Google/DashScope API |
| TTS | edge-tts skill, coqui-tts skill, tts | 多引擎 TTS |
| STT | openai-whisper skill | 本地 Whisper |
| 程式執行 | mini_coding_agent, coding-agent skill | Python 程式碼執行 |
| 影片處理 | video-frames skill | ffmpeg 框架截圖 |
| PDF 分析 | pdf | 文件內容提取 |
| 圖像分析 | image | AI 視覺分析 |
| 記憶系統 | memory_recall, memory_store, memory_forget, memory_update | 向量+關鍵字搜尋 |
| 健康檢查 | healthcheck skill | 主機安全 |
| MCP 整合 | mcp-wrapper skill | 外部 MCP 伺服器 |
| Skill 管理 | clawhub skill, find-skills skill, skill-creator skill | 技能系統 |

### 蘇茉目前沒有的關鍵工具（✗）

| 工具/類別 | 說明 | 差距等級 |
|-----------|------|----------|
| cronjob | 排程任務管理器（建立/列表/暫停/執行/刪除） | 🔴 關鍵缺口 |
| session_search / lcm_grep/expand | 跨對話歷史搜尋（壓縮對話的內容檢索） | 🔴 關鍵缺口 |
| browser_vision | 瀏覽器視覺分析（截圖+AI理解） | 🔴 關鍵缺口 |
| execute_code | Python 腳本執行（可呼叫工具，含邏輯分支） | 🟡 中等缺口 |
| delegate_task | 派發子 Agent 任務（隔離上下文） | 🟡 中等缺口 |
| Home Assistant | 智慧家居控制（燈光/開關/溫度等） | 🟡 中等缺口 |
| skill_manage/skill_view | 技能創建/管理介面 | 🟢 輕微缺口 |
| mixture_of_agents | 多模型協作推理（複雜數學/程式問題） | 🟢 輕微缺口 |
| rl_* | 強化學習訓練工具 | ⚫ 幾乎不需要 |

---

## 三、優先擴展建議

### 🔴 第一優先（立即需要，實作難度低）

#### 1. cronjob 排程系統
- **價值**：蘇茉家族最重要的缺口之一。Hermes 的 cronjob 可建立/列表/暫停/恢復/執行/刪除定時任務。
- **實作方式**：參考 Herme's cronjob設計，使用排程資料庫（JSON/SQLite）+ 背景 process 機制
- **預計難度**：★★☆☆☆（中低）
- **具體用途**：
  - 每日股票提醒
  - 愛可樂 FB 自動發文（之前因無排程停擺）
  - 每日天氣預報
  - 定期健康檢查

#### 2. 瀏覽器視覺分析增強
- **現況**：蘇茉已有 browser + image 分析，但兩者是分開的
- **需求**：browser_vision（截圖+AI同步分析）
- **實作方式**：結合現有 browser snapshot + image 分析工具
- **預計難度**：★★☆☆☆（低）

---

### 🟡 第二優先（高度需要，實作難度中等）

#### 3. execute_code 腳本執行器
- **價值**：Hermes 的 execute_code 可在 Python 中呼叫多個工具，含條件判斷、流程控制，比 mini_coding_agent 更輕量
- **實作方式**：擴展現有 mini_coding_agent，加入工具呼叫接口
- **預計難度**：★★★☆☆（中等）
- **用途**：複雜資料處理、批次操作

#### 4. delegate_task 派發系統
- **價值**：蘇茉已透過 sessions_spawn 有類似能力，但 Hermes 的 delegate_task 更完整（隔離上下文、只回傳摘要）
- **實作方式**：參考 OpenClaw sessions_spawn 機制，統一封裝
- **預計難度**：★★★☆☆（中等）

#### 5. Home Assistant 整合
- **價值**：物聯網控制能力。張家若有智慧家居設備，可語音/自動化控制燈光、空調、窗簾等
- **實作方式**：透過 HA REST API 或 WebSocket
- **預計難度**：★★★☆☆（中等，需 HA 環境）

---

### 🟢 第三優先（長期價值，視需求）

#### 6. 跨對話歷史搜尋增強（session_search / lcm_expand_query）
- **現況**：蘇茉已有 lcm_grep/lcm_expand，但用戶無法直接查詢「我們上次討論過什麼」
- **需求**：用自然語言搜尋過去對話的摘要內容
- **預計難度**：★★☆☆☆（低，依賴現有 LCM）

#### 7. mixture_of_agents
- **價值**：困難問題（複雜數學、演算法）可透過多模型協作提升正確率
- **需求**：多 API key（OpenRouter 匯聚模式）
- **預計難度**：★★★★☆（高，需多模型整合）

#### 8. skill_manage / skill_view
- **現況**：蘇茉已有 clawhub/find-skills/skill-creator，但無統一內建管理介面
- **預計難度**：★★☆☆☆（整合現有工具）

---

## 四、差距量化分析

```
Hermes 工具數：~40+
蘇茉已有工具數：~25+（含 Skills）
重疊率：~60%
關鍵缺口：3 個（cronjob, session_search, browser_vision）
中等缺口：3 個（execute_code, delegate_task, HA）
輕微缺口：3 個
不需要：1 個（rl_*）
```

---

## 五、建議行動方案

| 順序 | 行動 | 預計工時 | 負責 |
|------|------|----------|------|
| 1 | 實作 cronjob 排程系統 | 1-2 天 | 工程師蘇茉 |
| 2 | 整合 browser_vision | 半天 | 工程師蘇茉 |
| 3 | 擴展 execute_code 能力 | 2-3 天 | 工程師蘇茉 |
| 4 | HA 智慧家居整合 | 3-5 天 | 工程師蘇茉+老爺提供環境 |
| 5 | 統一 delegate_task 介面 | 1-2 天 | 工程師蘇茉 |
| 6 | session_search 自然語言介面 | 1 天 | 工程師蘇茉 |

---

## 六、結論

蘇茉目前的工具覆蓋率已達 **60%**，核心功能（搜尋、檔案、訊息、媒體、記憶）都已具備。

**最關鍵的三個缺口：**
1. **cronjob** — 影響自動化能力，之前愛可樂任務就是因此停擺
2. **session_search** — 影響記憶的可用性
3. **browser_vision** — 影響瀏覽器自動化的深度

建議優先實作 cronjob，可大幅提升蘇茉家族的自動化能力。

---
*報告結束 — 品管蘇茉*
