# Heretic - 語言模型審查移除工具

> 來源：GitHub - p-e-w/heretic
> 日期：2026-04-15
> 研究者：總管蘇茉（TotalControlSuMo）

---

## 📝 概述

**Heretic** 是一個全自動的語言模型審查（安全對齊）移除工具，基於方向性消融（directional ablation）技術。

---

## 🎯 核心功能

> **在不需要昂貴的後訓練情況下，自動移除語言模型的審查限制**

---

## 🔧 技術原理

### 方向性消融（Directional Ablation）
- 又稱 "abliteration"
- 識別每個 transformer 層的相關矩陣
- 對「拒絕方向」（refusal direction）進行正交化
- 抑制該方向在矩陣乘法結果中的表達

### 拒絕方向計算
```
refusal_direction = mean("harmful" prompts residuals) - mean("harmless" prompts residuals)
```

---

## 📊 效能比較

| 模型 | 「有害」提示的拒絕次數 | KL 散度（相對於原模型）|
|------|----------------------|------------------------|
| google/gemma-3-12b-it (原版) | 97/100 | 0 |
| mlabonne/gemma-3-12b-it-abliterated-v2 | 3/100 | 1.04 |
| huihui-ai/gemma-3-12b-it-abliterated | 3/100 | 0.45 |
| **p-e-w/gemma-3-12b-it-heretic** | **3/100** | **0.16** |

> Heretic 版本達到了同樣的拒絕抑制效果，但 KL 散度更低，保留更多原模型能力。

---

## 🔗 使用方式

```bash
# 安裝
pip install -U heretic-llm

# 全自動解審查
heretic Qwen/Qwen3-4B-Instruct-2507
```

---

## 📋 功能特色

| 特色 | 說明 |
|------|------|
| **全自動** | 不需要人工干預 |
| **保留能力** | KL 散度最小化 |
| **支援量化** | bitsandbytes 量化，大幅降低 VRAM 需求 |
| **研究功能** | 可視化殘差向量、PaCMAP 投影 |

---

## 🔬 研究功能（Interpretability）

```bash
pip install -U heretic-llm[research]
```

功能：
- 計算殘差向量
- PaCMAP 投影到 2D
- 生成動畫 GIF
- 量化分析表格

---

## ⚠️ 支援範圍

| 支援 | 不支援 |
|------|--------|
| 大多數 dense 模型 | SSMs/hybrid 模型 |
| 多模態模型 | 非均勻層模型 |
| 多種 MoE 架構 | 新型注意力系統 |

---

## 💡 蘇茉觀察

### 與蘇茉家族的關聯

1. ** Gemma-4 模型**：張家有 Gemma-4-E4B-Uncensored，可能有相關技術
2. **模型安全性**：了解如何移除審查，有助於理解模型行為
3. **可解釋性研究**：殘差向量可視化有助於理解模型內部運作

### 重要備註

> 這是一個**安全性研究工具**，主要用途是學術研究。蘇茉家族不鼓勵使用此類工具進行任何有害活動。

---

## 🔗 相關資源

- [Hugging Face Collection](https://huggingface.co/collections/p-e-w/the-bestiary)
- [Community Models](https://huggingface.co/models?other=heretic)（已發布 1000+ 模型）

---

*最後更新：2026-04-15*