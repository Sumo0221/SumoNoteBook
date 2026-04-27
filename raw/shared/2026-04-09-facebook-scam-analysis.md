# Facebook 貼文研究：AI 自動回覆 LinkedIn 訊息抓到北韓駭客

**研究日期**：2026-04-09
**研究者**：駭客蘇茉
**貼文連結**：https://www.facebook.com/groups/366863238003058/permalink/1704389540917081/
**社團**：AI 技術研究社 ChatGPT/Gemini/Claude/OpenClaw

---

## 📋 貼文概述

這是一篇**防詐騙教育文**，作者 YuShang Lung 分享了他使用 AI（Claude Code）自動回覆 LinkedIn 訊息時，意外抓到兩個北韓 Lazarus 集團駭客的經歷。

### 貼文內容重點：

1. **技術做法**：使用 opencli 瀏覽器自動化 CLI 工具 + Claude 自動回覆 LinkedIn 訊息
2. **抓到兩個詐騙**：
   - **Jayde Johnston**：推銷去中心化租屋平台 Tirios.xyz，開時薪 $90-110 USD
   - **Kateryna Horshenina**：烏克蘭 recruiter，推薦 AI 餐廳點餐系統，月薪 $15-20K USD

3. **詐騙手法分析**：屬於「Contagious Interview（傳染性面試）」攻擊
   - 技術審計發現 Tirios 專案藏有 C2 beacon
   - Base64 編碼隱藏 npoint.io 的惡意 payload URL
   - MongoDB 連線被 comment 掉，後端無正常功能
   - 目的：竊取 .env、API keys、加密貨幣錢包

---

## 🔍 詐騙特徵識別（整理自貼文）

- 主動在 LinkedIn 找人、薪水開很高（$90/hr+ 或 $15K/mo+）
- 很快就要你 clone repo 或打開附件
- 公司網站看起來精美但是空殼
- LinkedIn profile 很新、connection 很少
- 面試流程怪怪的（AI 面試、限時十分鐘、要求裝特定工具）

---

## 🛡️ 蘇茉的資安建議

1. **AI 作為第一道防線**：讓 AI 處理陌生訊息，避免直接接觸惡意連結
2. **自動化背景審計**：收到陌生訊息時自動搜尋背景
3. **沙盒環境**：絕對不要在本機執行陌生人提供的程式碼
4. **零信任原則**：任何來自陌生人的 Repo 或檔案，先隔離分析

---

## ⚠️ 此貼文非詐騙

此貼文為**教育性質**，旨在提醒開發者注意 LinkedIn 詐騙手法。貼文含有以下標籤：
- #LinkedIn詐騙
- #北韓駭客
- #ContagiousInterview
- #開發者資安
- #Lazarus
- #ClaudeCode

---

## 📝 備註

此貼文獲得 32 個讚、1 個留言，顯示社群對此議題的高度關注。
