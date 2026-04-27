# OpenMythos

**研究日期**：2026-04-22 16:49:37
**來源**：https://github.com/kyegomez/OpenMythos
**標籤**：機器學習, 自然語言處理, 算法

---

## 📌 關鍵資訊
標題：OpenMythos
來源：https://pypi.org/project/open-mythos/
日期：未提供
摘要：OpenMythos 是一個開放原始碼的理論實現 Claude Mythos 模型。它採用了一種稱為 Recurrent-Depth Transformer (RDT) 的架構，包含三個階段：Prelude（Transformer Block）、循環 Block 和 Coda。Attention 可以切換為 MLA 和 GQA，而(feed-forward使用了稀疏的 MoE 來適配可計算調整和深度變化的推理。
標籤：機器學習, 自然語言處理, 算法

---

## 📄 原文內容（部分）

```
# OpenMythos

<p align="left">
  <a href="https://pypi.org/project/open-mythos/" target="_blank">
    <picture>
      <source srcset="https://img.shields.io/pypi/v/open-mythos?style=for-the-badge&color=3670A0" media="(prefers-color-scheme: dark)">
      <img alt="Version" src="https://img.shields.io/pypi/v/open-mythos?style=for-the-badge&color=3670A0">
    </picture>
  </a>
  <a href="https://twitter.com/kyegomezb/">
    <picture>
      <source srcset="https://img.shields.io/badge/Twitter-Follow-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" media="(prefers-color-scheme: dark)">
      <img src="https://img.shields.io/badge/Twitter-Follow-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter">
    </picture>
  </a>
  <a href="https://discord.gg/3keGBK9Pvr" target="_blank">
    <picture>
      <source srcset="https://img.shields.io/badge/Discord-Join-5865F2?style=for-the-badge&logo=discord&logoColor=white" media="(prefers-color-scheme: dark)">
      <img alt="Discord" src="https://img.shields.io/badge/Discord-Join-5865F2?style=for-the-badge&logo=discord&logoColor=white">
    </picture>
  </a>
  <a href="https://pytorch.org" target="_blank">
    <picture>
      <source srcset="https://img.shields.io/badge/PyTorch-Implemented-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" media="(prefers-color-scheme: dark)">
      <img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-Implemented-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white">
    </picture>
  </a>
</p>

> **Disclaimer:** OpenMythos is an independent, community-driven theoretical reconstruction based solely on publicly available research and speculation. It is not affiliated with, endorsed by, or connected to Anthropic or any of their proprietary systems.

OpenMythos is an open-source, theoretical implementation of the Claude Mythos model. It implements a Recurrent-Depth Transformer (RDT) with three stages: **Prelude** (transformer blocks), a looped **Recurrent Block** (up to `max_loop_iters`), and a final **Coda**. Attention is switchable between MLA and GQA, and the feed-forward uses a sparse MoE with routed and shared experts ideal for exploring compute-adaptive, depth-variable reasoning.


## Installation

```bash
pip install open-mythos

#uv pip install open-mythos
```

## Usage

```python

import torch
from open_mythos.main import OpenMythos, MythosConfig


attn_type = "mla"  # or "gqa"

base = {
    "vocab_size": 1000,
    "dim": 256,
    "n_heads": 8,
    "max_seq_len": 128,
    "max_loop_iters": 4,
    "prelude_layers": 1,
    "coda_layers": 1,
    "n_experts": 8,
    "n_shared_experts": 1,
    "n_experts_per_tok": 2,
    "expert_dim": 64,
    "lora_rank": 8,
    "attn_type": attn_type,
}

if attn_type == "gqa":
    cfg = MythosConfig(**base, n_kv_heads=2)
else:
    cfg = MythosConfig(
        **base,
        n_kv_heads=8,
        kv_lora_rank=32,
        q_lora_rank=64,
        qk_rope_head_dim=16,
        qk_nope_head_dim=16,
        v_h
...
```

---

## 🔬 四層分析

### 第一層：白話解構

#### 這篇文章在講什麼？

本文介紹了名为 OpenMythos 的开源项目，它是一个基于 Claude Mythos 模型的开放源代码实现。该模型使用了一个带有三个阶段的递归深度变换器 (RDT) 架构——“序曲”（transformer 结构）、一个循环“块”以及最终的“尾声”。文章还介绍了项目的安装方法和基本使用流程，包括如何通过简单的命令行或Python代码调用OpenMythos模型。此外，还提供了几种预配置的参数模型供用户选择。

#### 主要在說什麼故事或概念？

本文详细阐述了 OpenMythos 模型的基本结构、工作原理及各种版本的参数规模，并展示了模型的基础使用方法。它还说明了训练模型所需的细节信息和使用条件。

#### 目標讀者是誰？

该文章面向的是对自然语言处理感兴趣的技术人员和研究人员，尤其是那些正在研究或实现类似 Claude Mythos 模型或其他递归深度变换器架构的应用的读者。此外，对于希望探索不同参数规模（从10亿参数到1万亿参数）以及多GPU环境下训练 OpenMythos 的用户来说，该文章也非常有价值。

### 第二層：技術驗證

#### 這篇文章的 claims 過哪些？

- 使用了递归深度变换器 (RDT) 架构。
- 序曲、循环块和尾声是 RDT 架构的基本组成部分。
- OpenMythos 模型支持 MLA 和 GQA 的注意力机制。
- OpenMythos 是一个开放源代码项目。

#### 哪些是有根據的？哪些可能是錯的？

- **序曲（transformer 结构）**、**循环块（up to 4次迭代）**和**尾声（1个编码层，基于共享专家网络）**是 RDT 架构的基本组成部分。这个描述是准确无误的。
- **注意力机制的选择性设置**（MLA vs. GQA），以及不同版本参数规模的信息，也是直接从文中的内容中提取出来的，因此被认为是正确的。
- 关于 OpenMythos 是一个开源项目这一说法，则是符合实际情况。

#### 有沒有邏輯漏洞或 bias？

文章没有显示出明显的逻辑漏洞。关于注意力机制的选择性设置和参数规模的描述也都是基于原文信息给出的解释，并无误导之处。此外，提到的 OpenMythos 模型可以运行在多GPU环境中这一信息也是正确的。因此，在整体上来看，这篇文章的信息是可靠的。

### 第三層：核心洞察

#### 這篇文章最重要的 3 個 insight 是什麼？

1. **OpenMythos 使用递归深度变换器 (RDT) 架构进行建模**。
2. **该项目提供了多种参数规模的预配置模型供选择使用**，包括从10亿参数到1万亿参数的不同版本。
3. **训练数据集可选多样**（包含 FineWeb-Edu 数据集），以及支持多GPU环境下的训练。

#### 對讀者最有價值的啟發是什麼？

- 了解 OpenMythos 的架构及其工作原理；
- 意识到 OpenMythos 提供了不同参数规模的选择，用户可以根据需要进行调整；
- 理解该模型可以在多种 GPU 配置下运行。

#### 如果只能带走一件事，是什麼？

最核心的信息可能是关于 OpenMythos 使用递归深度变换器架构的事实以及能够选择不同的参数规模以适应各种应用场景。这将对那些希望实现类似 Claude Mythos 模型的项目的研究人员或开发人员最有帮助。

### 第四層：系統整合建議

#### 這個東西怎麼用在我們現有的系統？

1. **安装与使用**：
   - 通过 pip 进行模块化安装和调用。
   
2. **多 GPU 训练支持**：
   - OpenMythos 支持在多 GPU 环境中进行训练。可以通过 `torchrun` 命令来指定GPU数量，例如：`torchrun --nproc_per_node=$(python -c "import torch; print(torch.cuda.device_count())") training/3b_fine_web_edu.py`

3. **使用不同参数规模**：
   - 项目提供了从10亿到1万亿参数的预配置模型，用户可以根据需要选择合适的模型版本进行训练和测试。

4. **基于 FineWeb-Edu 数据集进行实验**：
   - 使用指定的数据集（如 `HuggingFaceFW/fineweb-edu`）作为基础数据源进行实验，以验证不同参数规模在实际应用中的表现。
   
5. **关注注意力机制的选择性设置**：
   - 选择适合项目需求的注意力机制类型，并基于此配置模型参数。

总之，OpenMythos 模型是一个具有灵活性和多样性的平台。它不仅提供了多 GPU 支持来加速训练过程，还允许用户通过调整不同参数规模来适应自己的具体应用场景。同时，通过指定不同的训练数据集支持实验与验证。

---

## 💾 元資料

- **研究時間**：2026-04-22 16:49:37
- **來源 URL**：https://github.com/kyegomez/OpenMythos
- **處理模型**：qwen2.5:3b (本地 Ollama)

---

*由 EnhancedStudy 技能自動產生*
