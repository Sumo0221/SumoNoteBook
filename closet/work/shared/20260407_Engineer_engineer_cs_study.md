# CS 課程學習筆記 - MIT 6.006 Introduction to Algorithms

**學習日期**：2026-04-07  
**課程來源**：MIT OCW  
**URL**：https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/

---

## 課程概述

MIT 6.006 是 MIT 最經典的演算法入門課程之一，介紹計算問題的數學建模、常見演算法、演算法範式和數據結構。

---

## 主要主題

### 1. 演算法基礎（Algorithm Fundamentals）
- **時間複雜度（Time Complexity）**：Big-O notation
- **空間複雜度（Space Complexity）**
- **漸進分析（Asymptotic Analysis）**

### 2. 核心數據結構
| 數據結構 | 操作複雜度 | 應用場景 |
|---------|-----------|---------|
| Array | O(1) 隨機存取 | 基礎儲存 |
| Linked List | O(n) 查找 | 動態大小 |
| Stack | O(1) push/pop | 遞迴呼叫 |
| Queue | O(1) enqueue/dequeue | 排程任務 |
| Hash Table | O(1) 平均 | 快速查詢 |
| Binary Heap | O(log n) | 優先隊列 |
| Binary Search Tree | O(log n) 平均 | 有序操作 |

### 3. 經典演算法範式

#### 3.1 分治法（Divide and Conquer）
- **概念**：將問題分解為子問題，遞迴求解，再合併
- **範例**：Merge Sort、Quick Sort、Binary Search
- **複雜度**：通常 T(n) = 2T(n/2) + O(n) → O(n log n)

#### 3.2 貪心演算法（Greedy Algorithms）
- **概念**：每步選擇當前最優解
- **適用問題**：最小生成樹、最短路徑（Huffman Coding）
- **注意**：需證明最優性

#### 3.3 動態規劃（Dynamic Programming）
- **概念**：記錄子問題最優解，避免重計算
- **經典問題**：Fibonacci、最短路徑、最長公共子序列
- **解題步驟**：
  1. 定義子問題
  2. 寫出遞迴關係
  3. 計算順序（bottom-up）
  4. 追蹤解

### 4. 圖論演算法

#### 4.1 遍歷
- **BFS（廣度優先搜尋）**：O(V+E)，找最短路徑
- **DFS（深度優先搜尋）**：O(V+E)，拓撲排序、連通分量

#### 4.2 最短路徑
| 演算法 | 複雜度 | 適用場景 |
|-------|--------|---------|
| Dijkstra | O((V+E)logV) | 無負權 |
| Bellman-Ford | O(VE) | 可有負權 |
| Floyd-Warshall | O(V³) | 全面路徑 |

#### 4.3 最小生成樹
- **Prim**：O(E log V)
- **Kruskal**：O(E log V)

### 5. 計算複雜度理論
- **P 類問題**：多項式時間可解
- **NP 類問題**：多項式時間可驗證
- **NP-Complete**：最難的 NP 問題
- **NP-Hard**：至少和 NP-Complete 一樣難

---

## 關鍵學習心得

1. **複雜度分析是基礎**：理解 Big-O 才能寫高效程式
2. **資料結構選型很重要**：根據操作需求選擇合適結構
3. **範式思維**：分治、貪心、DP 是解決問題的通用框架
4. **圖論是核心**：很多實際問題都能轉換為圖問題

---

---

# 🆕 第二階段：CS 61B - Data Structures (Java) - UC Berkeley

**學習日期**：2026-04-07  
**課程來源**：UC Berkeley CS 61B Fall 2025  
**URL**：https://fa25.datastructur.es/

---

## 課程概述

CS 61B 是 UC Berkeley 的經典資料結構課程，使用 Java 教學。相較於 MIT 6.006 更強調**實作能力**，從基礎語法到複雜資料結構都有完整訓練。

---

## 課程進度表

|週次|主題|
|---|---|
|Week 1|Java 入門、類別定義、List/Set/Map|
|Week 2|References、Recursion、Linked Lists|
|Week 3|DLLists、ALists、Testing|
|Week 4|Array Resizing、Circular Arrays|
|Week 5|Interface/Implementation Inheritance|
|Week 6|Iterators、Object Methods、Comparators|
|Week 7|Asymptotics I、中期考試|
|Week 8|Disjoint Sets、Asymptotics II|

---

## 核心主題

### 1. Java 基礎與類別設計
- **Instance Variables**：物件狀態儲存
- **Constructors**：物件初始化
- **Static vs Instance**：類別層級 vs 物件層級
- **Scope**：作用域規則

### 2. Linked Lists（鏈結串列）
- **SLList（單向鏈結串列）**：Sentinel Node 設計
- **DLLists（雙向鏈結串列）**：前後指標
- **Operations**：addFirst, addLast, removeFirst, removeLast
- **Time Complexity**：O(1) 頭尾操作，但 O(n) 隨機存取

### 3. Array Lists（動態陣列）
- **Resizing Strategy**：幾何成長（倍增）
- **Circular Array**：環形陣列優化
- ** amortized O(1)**：攤提複雜度概念
- **Java ArrayList 實作原理**

### 4. 繼承（Inheritance）
- **Interface**：行為契約
- **Extends**：類別擴展
- **Casting**：型態轉換
- **Polymorphism**：多型
- **Comparable vs Comparator**：比較器

### 5. 複雜度分析（Asymptotics）
- **Worst-case vs Average-case**
- **空間複雜度**
- **amortized**：攤提分析
- **Theta vs Big-O vs Big-Ω**

### 6. Disjoint Sets（互斥集合）
- **Union-Find 資料結構**
- **Path Compression**：路徑壓縮
- **Union by Rank**：按階合併
- **複雜度**：幾乎 O(1)（反函數）

---

## 與 MIT 6.006 的比較

|面向|MIT 6.006|CS 61B|
|---|---|---|
|語言|偽代數|M Java|
|焦點|理論證明|實作|
|資料結構|基礎|深入|
|複雜度|演算法分析|Asymptotics|
|專案|No|Yes|

---

## 關鍵學習心得

1. **Java 是 OO 典範**：理解 class、interface、inheritance 的組合
2. **Linked List vs Array**：依操作需求選擇
3. **amortized 分析**：理解攤提複雜度的重要性
4. **Disjoint Sets**：看似簡單但極度實用的資料結構

---

## 參考資源

- CS 61B 官方教材：https://cs61b-2.gitbook.io/cs61b-textbook-fall-2025/
- YouTube 課程影片
- LeetCode 練習平台