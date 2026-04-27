# SumoNoteBook MindForge - 開發紀錄

## 開發概要

本專案旨在借鏡 MindForge 優化 SumoNoteBook，實現知識蒸餾與品質控制。

## 開發項目

### P0 - 最高優先
- [x] Citation 追蹤系統
- [x] Lint 矛盾偵測升級
- [x] RDT 迭代深化引擎（2026-04-22 新增！）

### P1 - 高優先
- [x] Principle 0 SOUL

### P2 - 中優先
- [ ] KAL Ingest 自問自答驗證機制（暫緩）

## RDT 功能（2026-04-22 新增！）

基於 OpenMythos 的 Recurrent Depth Transformer (RDT) 概念，實現了迭代深化搜尋：

### 運作原理
1. **Prelude**: 初始搜尋，建立基礎理解
2. **Recurrent Block**: 迭代深化，根據初步結果優化查詢
3. **Coda**: 最終整合輸出

### 使用方式
```python
from query_interface import search_rdt, natural_search

# RDT 搜尋
result = search_rdt("複雜的查詢問題")

# 自然語言介面，搭配 RDT 模式
result = natural_search("查詢內容", use_rdt=True)
```

### 命令列
```bash
python query_interface.py --rdt "查詢內容"
```

## 開發時間線
- 2026-04-15: 初始開發
- 2026-04-22: RDT 迭代深化引擎實作完成