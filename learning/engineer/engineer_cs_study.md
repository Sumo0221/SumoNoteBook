# CS 課程學習記錄：MIT 6.006 - Introduction to Algorithms

**學習日期：** 2026-04-05
**課程來源：** https://github.com/Developer-Y/cs-video-courses
**影片連結：** https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/

---

## 📚 課程概覽

MIT 6.006 是演算法的基礎課程，涵蓋以下核心主題：
- 資料結構（Data Structures）
- 演算法設計與分析（Algorithm Design & Analysis）
- 圖論（Graph Algorithms）
- 動態規劃（Dynamic Programming）
- 複雜度理論（Complexity）

---

## 🔥 Lecture 1: Algorithms and Computation

### 核心概念
- **演算法**：輸入 → 計算步驟 → 輸出
- **正確性**：對所有輸入都產生正確輸出
- **效率**：以時間複雜度（Time Complexity）和空間複雜度（Space Complexity）衡量
- **大步樂記號（Big O Notation）**：描述上界，常用於分析最壞情況

### 常見複雜度排名（由快到慢）
```
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)
```

### 工程師觀點
```
面試常考：能快速說出各複雜度的實際意義
O(1):   陣列隨機存取
O(log n): 二分搜尋 Binary Search
O(n):   線性走訪
O(n log n): 高效排序（Merge Sort, Heap Sort）
O(n²):  氣泡排序（面試別寫這個）
O(2ⁿ):  暴力枚舉組合
```

---

## 🔥 Lecture 2: Data Structures and Dynamic Arrays

### 陣列（Array）
- 連續記憶體區塊，支援 O(1) 隨機存取
- 缺點：大小固定，插入/刪除代價高

### 動態陣列（Dynamic Array / Vector）
- 當空間不足時，擴展為原本的 2 倍大小（Amortized Analysis）
- 均攤插入代價：O(1)（每次擴展代價均攤後）
- Python `list` 就是動態陣列的實作

### Python 程式碼範例
```python
import sys
# Dynamic Array 概念展示
class DynamicArray:
    def __init__(self):
        self.n = 0          # 元素數量
        self.capacity = 1   # 初始容量
        self.A = [None]     # 底層儲存
    
    def append(self, item):
        if self.n == self.capacity:
            self._resize(2 * self.capacity)
        self.A[self.n] = item
        self.n += 1
    
    def _resize(self, new_cap):
        B = [None] * new_cap
        for i in range(self.n):
            B[i] = self.A[i]
        self.A = B
        self.capacity = new_cap
    
    def __len__(self):
        return self.n
    
    def __getitem__(self, i):
        if 0 <= i < self.n:
            return self.A[i]
        raise IndexError("Index out of range")
```

### 複雜度分析
| 操作 | 陣列 | 動態陣列（均攤） |
|------|------|------------------|
| 存取 | O(1) | O(1) |
| 尾部插入 | O(n) | O(1) 均攤 |
| 中間插入 | O(n) | O(n) |
| 刪除 | O(n) | O(n) |

---

## 🔥 Lecture 3: Sets and Sorting

### 集合操作與複雜度
- **搜尋**：O(n) 平均（無排序），O(log n)（已排序+二分）
- **插入/刪除**：O(n)（陣列實作）

### 排序演算法對比

| 演算法 | 平均 | 最壞 | 額外空間 | 穩定 |
|--------|------|------|----------|------|
| Merge Sort | O(n log n) | O(n log n) | O(n) | ✅ |
| Quick Sort | O(n log n) | O(n²) | O(log n) | ❌ |
| Heap Sort | O(n log n) | O(n log n) | O(1) | ❌ |
| Bubble Sort | O(n²) | O(n²) | O(1) | ✅ |

### Merge Sort Python 實作
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

---

## 🔥 Lecture 4: Hashing

### 雜湊表（Hash Table）
- **核心思想**：透過雜湊函數（Hash Function）直接計算資料儲存位置
- **平均查詢/插入/刪除**：O(1)
- **最壞情況**：O(n)（所有 key 都 collision）

### 雜湊函數設計原則
1. **均勻分佈**：將 key 均勻映射到 slots
2. **確定性**：相同輸入產生相同輸出
3. **快速計算**

### 碰撞處理（Collision Resolution）
1. **Chaining（分離鏈接法）**：用 linked list 儲存碰撞的 key
2. **Open Addressing（開放定址法）**：找下一個空位
   - Linear Probing：`h(k, i) = (h'(k) + i) mod m`
   - Quadratic Probing：`h(k, i) = (h'(k) + c₁i + c₂i²) mod m`

### Python 字典就是 Hash Table
```python
# Python dict 底層就是 Hash Table，幾乎所有操作都是 O(1)
d = {}
d["name"] = "SuMo"       # O(1)
d["age"] = 25             # O(1)
print(d["name"])          # O(1)
```

### 工業實務經驗
```
面試重點：
- 什麼情況下 hash table 會變慢？ → 碰撞多、攻擊者故意構造大量相同 hash
- 如何解決？ → 設計更好的 hash function、使用 bloom filter
```

---

## 🔥 Lecture 5: Linear Sorting（計數排序 / 基數排序）

### 計數排序（Counting Sort）
- **前提**：輸入範圍已知且較小（0 到 k）
- **時間複雜度**：O(n + k)，當 k = O(n) 時為線性 O(n)
- **穩定排序**：是（保持相同元素順序）

```python
def counting_sort(arr, max_val):
    # 統計每個值出現次數
    count = [0] * (max_val + 1)
    for x in arr:
        count[x] += 1
    
    # 計算 prefix sum，確定位置
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    # 由後往前輸出（穩定排序關鍵）
    result = [0] * len(arr)
    for x in reversed(arr):
        result[count[x] - 1] = x
        count[x] -= 1
    
    return result
```

### 基數排序（Radix Sort）
- 按位元（digit）由低到高排序
- 需要穩定的子排序（如 counting sort）
- **複雜度**：O(d · (n + k))，d = 位數，k = 進位制

---

## 🔥 Lecture 6-7: Binary Trees / AVL Trees

### 二元搜尋樹（BST）
- 左子樹所有節點 < 根節點 < 右子樹所有節點
- 搜尋/插入/刪除平均：O(log n)
- **最壞**：O(n)（當 tree 退化為 linked list）

### AVL Tree（高度平衡樹）
- **平衡條件**：左右子樹高度差 ≤ 1
- **旋轉操作**：維護平衡的關鍵
  - **Single Rotation**：適用於 LL 和 RR 失衡
  - **Double Rotation**：適用於 LR 和 RL 失衡
- **高度**：O(log n) → 所有操作 O(log n)

### 旋轉示意
```python
# 單一旋轉（Right Rotation for LL imbalance）
def rotate_right(node):
    new_root = node.left
    node.left = new_root.right
    new_root.right = node
    return new_root

# 單一旋轉（Left Rotation for RR imbalance）
def rotate_left(node):
    new_root = node.right
    node.right = new_root.left
    new_root.left = node
    return new_root
```

---

## 🔥 Lecture 8: Binary Heaps

### 二元堆積（Binary Heap）
- **結構性質**：是完全二元樹（complete binary tree），可用陣列儲存
- **堆積性質**：父節點 >= 子節點（Max Heap）或父節點 <= 子節點（Min Heap）

### 陣列表示法（1-indexed）
```
父節點索引：i → 子節點：2i, 2i+1
子節點索引：i → 父節點：⌊i/2⌋
```

### 核心操作
| 操作 | 複雜度 |
|------|--------|
| build_heap | O(n) |
| find_max | O(1) |
| extract_max | O(log n) |
| insert | O(log n) |
| decrease_key | O(log n) |

### Heap Sort
```python
def heap_sort(arr):
    n = len(arr)
    
    # Max Heapify：從最後一個非葉節點開始
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)
    
    # 逐步取出最大值
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # swap
        _heapify(arr, i, 0)

def _heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)
```

---

## 🔥 Lecture 9-10: BFS & DFS（圖遍歷）

### 圖的表示
```python
# Adjacency List（鄰接表）- 節省空間
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Adjacency Matrix（鄰接矩陣）- O(1) 查詢邊
# 適合密集圖（dense graph）
```

### BFS（廣度優先搜尋）
- **應用**：最短路徑（unweighted graph）、層級遍歷
- **資料結構**：Queue（FIFO）
- **複雜度**：O(V + E)，V = 頂點數，E = 邊數

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result
```

### DFS（深度優先搜尋）
- **應用**：拓撲排序、連通分量、迴圈檢測
- **資料結構**：Stack（LIFO）或遞迴
- **複雜度**：O(V + E)

```python
def dfs_recursive(graph, node, visited, result):
    visited.add(node)
    result.append(node)
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited, result)

def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            result.append(node)
            stack.extend(reversed(graph[node]))  # 維持順序
    
    return result
```

### BFS vs DFS 選擇情境
```
BFS：
  ✅ 最短路徑（unweighted）
  ✅ 找到最近解
  ✅ 層級遍歷

DFS：
  ✅ 拓撲排序
  ✅ 連通分量
  ✅ 路徑枚舉
  ✅ 節省記憶體（只需儲存一條路徑）
```

---

## 🔥 Lecture 11-13: Shortest Paths

### Dijkstra's Algorithm
- **條件**：所有邊權重為非負數
- **複雜度**：
  - Array 實作：O(V²)
  - Min-Heap 實作：O((V+E) log V)
- **不適用**：有負權重邊（會得到錯誤結果）

```python
import heapq

def dijkstra(graph, start):
    dist = {start: 0}
    pq = [(0, start)]
    visited = set()
    
    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        
        for v, weight in graph[u]:
            if v not in dist or dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(pq, (dist[v], v))
    
    return dist
```

### Bellman-Ford Algorithm
- **條件**：可處理負權重邊
- **複雜度**：O(VE)
- **可偵測負環（Negative Cycle）**

### 應用場景
```
Dijkstra：GPS 導航、網路路由（OSPF）
Bellman-Ford：貨幣套利檢測、債務網絡分析
```

---

## 🔥 Lecture 15-18: Dynamic Programming（動態規劃）⭐⭐⭐

### 什麼是 DP？
**將大問題分解為子問題，子問題結果重複利用，避免重複計算**

### DP 的三大條件
1. **Optimal Substructure**：最優解由子問題的最優解組成
2. **Overlapping Subproblems**：子問題會重複出現
3. **Rebuild Solution**：能從子問題重建整體解

###經典例題

#### 1. Fibonacci（最基礎）
```python
# 暴力：O(2^n)
def fib_brutal(n):
    if n <= 1:
        return n
    return fib_brutal(n-1) + fib_brutal(n-2)

# DP Top-Down（Memoization）：O(n)
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n-1, memo) + fib_mono(n-2, memo)
    return memo[n]

# DP Bottom-Up（Tabulation）：O(n)
def fib_dp(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

#### 2. Longest Common Subsequence（LCS）
```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]

# 應用：.diff 工具、DNA序列比對、抄襲偵測
```

#### 3. Longest Increasing Subsequence（LIS）
```python
def lis(nums):
    # O(n log n) 使用 binary search
    import bisect
    dp = []
    for x in nums:
        pos = bisect.bisect_left(dp, x)
        if pos == len(dp):
            dp.append(x)
        else:
            dp[pos] = x
    return len(dp)
```

#### 4. 硬幣找零（Coin Change）
```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for c in coins:
            if i >= c:
                dp[i] = min(dp[i], dp[i - c] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```

### DP 解題模板
```
步驟1：定義子問題（State）
步驟2：建立遞迴關係（Transition）
步驟3：確定起始條件（Base Case）
步驟4：決定計算順序（Top-Down or Bottom-Up）
步驟5：空間優化（如適用）
```

---

## 🔥 Lecture 19: Complexity（P vs NP）

### 复杂度分类
```
P（多項式時間）：
  ✅ 可在多項式時間內解決
  ✅ 例：排序、搜尋、最短路徑

NP（非確定性多項式時間）：
  ✅ 解可以在多項式時間內驗證
  ✅ 例：數獨、哈密頓路徑、集合覆蓋

NP-Complete：
  🔴 最難的 NP 問題
  🔴 所有 NP 問題都能歸約到它
  🔴 目前沒有已知的多項式時間解法

NP-Hard：
  🔴 至少和 NP-Complete 一樣難
  🔴 不要求可在多項式時間驗證
```

### 面試常考問題
```
Q: 什麼是 P vs NP 問題？
A: 如果問題的解可以在多項式時間驗證，
   那麼是否也能在多項式時間內找到？
   這是 CS 最大的 open problem，Clay Mathematics Institute 懸賞 100 萬美元

Q: 枚舉所有組合 vs DP，什麼時候用？
A: 當問題有重疊子結構時用 DP；
   當需要枚舉所有可能性（n! 或 2^n）時用暴力枚舉
```

---

## 💡 工程師的實務心得

### 面試高頻主題排序
```
1. ⭐⭐⭐ 動態規劃（60% 面試題）
2. ⭐⭐⭐ 圖論（BFS/DFS/Dijkstra）  
3. ⭐⭐ 資料結構（Hash Table/Tree/Heap）
4. ⭐⭐ 排序與搜尋（二分搜尋為核心）
5. ⭐ 複雜度分析（Big O）
```

### 實務應用
```
Hash Table：幾乎所有程式語言的 dictionary/set 底層
Heap：優先級佇列、事件模擬、最短路徑
BST/AVL：資料庫索引、檔案系統
Graph：BFS/DFS → 社交網路推薦、路徑規劃
DP：自然語言處理、影像辨識、資源優化
```

### 推薦後續學習
1. **MIT 6.046**（演算法的設計與分析）— 更深入的理論
2. **CS 170**（UC Berkeley 演算法）— 實用導向
3. **系統設計** — 將演算法知識應用於大規模系統

---

*本筆記由工程師蘇茉於 2026-04-05 整理自 MIT 6.006 OCW 課程*

---

## 🔥 Lecture 20: Course Review（課程總複習）

### 四大核心能力目標
1. **解決困難計算問題**（Solve hard computational problems）
2. **證明演算法的正確性**（Argue an algorithm is correct）
3. **證明演算法的效率**（Argue an algorithm is "good"）
4. **有效溝通上述內容**（Effectively communicate the above）

### 知識地圖回顾
```
                    ┌─────────────────────┐
                    │  Divide & Conquer   │
                    │  Merge Sort, Recurr │
                    └─────────┬───────────┘
                              │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌─────────────────┐ ┌───────────────┐ ┌─────────────────────┐
│    Sorting      │ │  Data         │ │    Graph Algos      │
│  Quick/Heap/   │ │  Structures   │ │  BFS/DFS/Dijkstra/  │
│  Counting/Radix│ │  Hash/Tree/   │ │  Bellman-Ford       │
│                 │ │  Heap         │ │                     │
└─────────────────┘ └───────────────┘ └─────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ Dynamic Programming │
                    │  Fibonacci→LCS→LIS │
                    │  Coins→APSP→Rod     │
                    └─────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │     Complexity      │
                    │   P vs NP, NPC     │
                    └─────────────────────┘
```

---

## 🔥 Lecture 21: Algorithms—Next Steps（下一步）

### 這堂課學完後該往哪走？

#### 繼續深入的方向
```
1. 更高階的資料結構
   - 6.851: Advanced Data Structures（MIT）
   - 涵蓋：Fibonacci Heaps、Splay Trees、Van Emde Boas Trees

2. 更深入的演算法設計
   - 6.046: Design and Analysis of Algorithms（MIT）
   - 涵蓋：Randomized Algorithms, Approximation Algorithms

3. 圖論專精
   - CS 170: Algorithms（UC Berkeley）- 實用導向

4. 計算理論
   - Automata Theory、Computability Theory
```

#### 各領域的後續課程推薦
| 領域 | 課程 | 學校 |
|------|------|------|
| 作業系統 | 6.828 | MIT |
| 分散式系統 | 6.824 | MIT |
| 機器學習 | 6.034 / 6.036 | MIT |
| 資料庫 | 6.851 | MIT |
| 密碼學 | 6.875 | MIT |
| 程式語言 | 6.820 | MIT |

---

## 📊 MIT 6.006 完整知識圖譜

### 課程大綱（21堂Lecture）

| Week | 主題 | 核心內容 |
|------|------|----------|
| 1 | 基礎概念 | Big O, Array, Dynamic Array |
| 2 | 集合與排序 | Sorting, Merge Sort, Quick Sort |
| 3 | 雜湊 | Hash Table, Collision Resolution |
| 4 | 線性排序 | Counting Sort, Radix Sort |
| 5 | 二元樹 | BST, AVL Trees, Rotations |
| 6 | 堆積 | Binary Heap, Heap Sort |
| 7 | 圖遍歷 | BFS, DFS |
| 8 | 最短路徑 | Dijkstra, Bellman-Ford, Johnson |
| 9 | 動態規劃 | Fib, LCS, LIS, Coins, Rod, APSP |
| 10 | 複雜度 | P vs NP, NP-Complete |

### 麵試考點熱力圖
```
超重要 ⭐⭐⭐：
  - Dynamic Programming（60% 面試題）
  - BFS/DFS 圖遍歷
  - 二分搜尋 Binary Search
  - Dijkstra's Algorithm

重要 ⭐⭐：
  - Hash Table（觀念題 + 實作題）
  - Merge Sort / Quick Sort
  - BST / AVL 旋轉操作
  - Heap Sort / 優先級佇列
  - Big O 分析

基礎 ⭐：
  - Array / Dynamic Array
  - 計數排序 / 基數排序
  - Bellman-Ford
  - P vs NP 概念
```

---

## 💡 工程師蘇茉的學習心得（2026-04-05 第二次複習）

### 為什麼選 MIT 6.006？
1. **經典中的經典**：MIT 最受歡迎的演算法課
2. **完整體系**：從基礎到進階，循序漸進
3. **工業導向**：幾乎所有科技公司面試內容都涵蓋
4. **免費且高品質**：MIT OCW 免費觀看

### 實務應用場景
```
Hash Table：
  - Python dict / Java HashMap 底層
  - 面試問「如何實現 LRU Cache」

Heap / Priority Queue：
  - Python heapq 模組
  - 行程_scheduler、事件模擬引擎
  - Dijkstra 最短路徑

Graph Algorithms：
  - 社交網路「可能認識的人」推薦
  - GPS 導航最短路徑
  - 網路爬蟲的 URL visited 管理

Dynamic Programming：
  - .diff 工具（LCS）
  - 字串相似度比對
  - 影像辨識、NLU
```

### 下一步學習計畫
```
Q2 2026:
  □ 複習 MIT 6.046（Design & Analysis of Algos）
  □ 完成 CS 170（Berkeley Algorithms）習題
  □ 刷 LeetCode Top 100 面試題

Q3 2026:
  □ 分散式系統（MIT 6.824）
  □ 機器學習基礎（Andrew Ng Coursera）
```

---

## 📅 學習Session記錄

### Session 3（2026-04-05）- Graph Algorithms & Dynamic Programming 深耕

**今日重點：**
- 圖資料結構的兩種表示法（Adjacency List vs Adjacency Matrix）
- BFS：用於最短路徑（無權重圖）、層級遍歷
- DFS：用於拓撲排序、連通分量、迴圈檢測
- 最短路徑三劍客：Bellman-Ford、Dijkstra、Johnson
- DP 經典五題：Fibonacci、LCS、LIS、Coins、Rod Cutting

**新理解：**
- BFS/DFS 核心複雜度皆為 O(V+E)，關鍵差異在於資料結構（Queue vs Stack）
- Dijkstra 不能處理負權邊，Bellman-Ford 可以並能偵測負環
- DP 的本質：重疊子問題 + 最優子結構，用空間換取時間

**工程師實務連結：**
- BFS：用於社交網路「可能認識的人」、Google Crawler URL 追蹤
- Dijkstra：GPS 導航、網路路由（OSPF 協定）
- DP LCS：.diff 工具、DNA 序列比對、文字相似度

---

*本筆記由工程師蘇茉於 2026-04-05 整理自 MIT 6.006 OCW 課程*
*學習次數：第3次（Graph + DP 專題）*

---

# MIT 6.046J - Design and Analysis of Algorithms
## 演算法設計與分析（進階課程）

**學習日期：** 2026-04-05
**課程來源：** https://github.com/Developer-Y/cs-video-courses
**影片連結：** https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/
**前置知識：** MIT 6.006（演算法基礎）

---

## 📚 課程概覽

MIT 6.046J 是 6.006 的進階版本，強調**演算法設計技術**與**複雜度的深入分析**。

**核心Topics：**
- Divide-and-Conquer（分治法）
- Randomized Algorithms（隨機演算法）
- Dynamic Programming（動態規劃）
- Greedy Algorithms（貪心演算法）
- Incremental Improvement（漸進改良）
- Complexity & Cryptography（複雜度與密碼學）

---

## 🔥 Topic 1: Divide and Conquer（分治法）

### 核心思想
```
大問題 → 分割成子問題 → 遞迴解決子問題 → 合併結果
```

### Master Theorem（主定理）
用於分析分治法複雜度的公式：

```
T(n) = a·T(n/b) + f(n)

Case 1: f(n) = O(n^(log_b a - ε))  →  T(n) = Θ(n^(log_b a))
Case 2: f(n) = Θ(n^(log_b a) · log^k n)  →  T(n) = Θ(n^(log_b a) · log^(k+1) n)
Case 3: f(n) = Ω(n^(log_b a + ε))  →  T(n) = Θ(f(n))
```

### 經典例子：矩陣乘法 Strassen Algorithm
- **傳統**：O(n³) — 三層迴圈
- **Strassen**：O(n^2.807) — 7次乘法代替8次

```python
# 2x2 矩陣相乘的分治實現概念
def matrix_multiply(A, B):
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]
    
    # 分割矩陣為 4 個子矩陣
    a, b, c, d = split_matrix(A)
    e, f, g, h = split_matrix(B)
    
    # 7 次乘法（Strassen 核心）
    p1 = matrix_multiply(a, f - h)
    p2 = matrix_multiply(a + b, h)
    p3 = matrix_multiply(c + d, e)
    p4 = matrix_multiply(d, g - e)
    p5 = matrix_multiply(a + d, e + h)
    p6 = matrix_multiply(b - d, g + h)
    p7 = matrix_multiply(a - c, e + f)
    
    # 合併結果
    result = [
        [p5 + p4 - p2 + p6, p1 + p2],
        [p3 + p4, p1 + p5 - p3 - p7]
    ]
    return result
```

---

## 🔥 Topic 2: Randomized Algorithms（隨機演算法）

### 為什麼要用隨機？
- **避免最壞情況**：攻擊者無法構造針對性輸入
- **簡化設計**：很多問題隨機化後更簡單
- **期望分析**：用 Expected Time 代替 Worst-Case

### 重要技術：Randomized Quicksort
**傳統 Quick Sort**：選首元素或尾元素為 pivot → 最壞 O(n²)
**隨機 Quick Sort**：隨機選 pivot → **期望 O(n log n)**

```python
import random

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    # 隨機選 pivot（關鍵！）
    pivot_idx = random.randint(0, len(arr) - 1)
    pivot = arr[pivot_idx]
    
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)
```

### 隨機化應用：Quick Select（找第 k 小的元素）
```python
def quickselect(arr, k):
    if len(arr) == 1:
        return arr[0]
    
    pivot_idx = random.randint(0, len(arr) - 1)
    pivot = arr[pivot_idx]
    
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    if k < len(left):
        return quickselect(left, k)
    elif k < len(left) + len(middle):
        return pivot
    else:
        return quickselect(right, k - len(left) - len(middle))
```

### 隨機雜湊（Universal Hashing）
避免 hash function 被攻擊：
```python
# 通用雜湊函數族
def universal_hash(m, p, a, b, x):
    # h(x) = ((a·x + b) mod p) mod m
    return ((a * x + b) % p) % m

# 選擇隨機的 a, b（從有限域中）
def random_hash_family(m, p):
    a = random.randint(1, p - 1)
    b = random.randint(0, p - 1)
    return lambda x: universal_hash(m, p, a, b, x)
```

---

## 🔥 Topic 3: Greedy Algorithms（貪心演算法）

### 什麼時候貪心有效？
**貪心選擇性質（Greedy Choice Property）**：每一步的最優選擇能導致全域最優解

### 經典問題 1：活動選擇問題（Activity Selection）
```python
def activity_selection(activities):
    # 按結束時間排序（貪心的關鍵！）
    activities.sort(key=lambda x: x[1])
    
    selected = [activities[0]]
    last_end = activities[0][1]
    
    for start, end in activities[1:]:
        if start >= last_end:  # 不重疊
            selected.append((start, end))
            last_end = end
    
    return selected

# 測試
activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14)]
print(activity_selection(activities))
# 輸出最大相容活動集合
```

### 經典問題 2：Huffman Coding（霍夫曼編碼）
```python
import heapq
from collections import Counter

def huffman_coding(text):
    # Step 1: 統計頻率
    freq = Counter(text)
    
    # Step 2: 建立優先級佇列
    heap = [(f, char) for char, f in freq.items()]
    heapq.heapify(heap)
    
    # Step 3: 合併最小頻率的兩個節點
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = (left[0] + right[0], left[1] + right[1], None)
        heapq.heappush(heap, merged)
    
    # Step 4: 產生編碼表
    codes = {}
    def build_codes(node, code=""):
        if node[2] is None:  # 葉節點
            codes[node[1]] = code
        else:
            build_codes(node[1], code + "0")
            build_codes(node[2], code + "1")
    
    root = heap[0]
    build_codes(root)
    return codes

# 應用：檔案壓縮（JPEG、MP3 背後原理）
```

### 經典問題 3：最小生成樹（MST）- Kruskal & Prim

**Kruskal's Algorithm（貪心 + Union-Find）：**
```python
def kruskal_mst(vertices, edges):
    # edges: [(weight, u, v), ...]
    edges.sort()  # 貪心：先選最輕的邊
    parent = {v: v for v in vertices}
    rank = {v: 0 for v in vertices}
    
    def find(v):
        if parent[v] != v:
            parent[v] = find(parent[v])
        return parent[v]
    
    def union(v1, v2):
        r1, r2 = find(v1), find(v2)
        if r1 == r2:
            return False
        if rank[r1] > rank[r2]:
            r1, r2 = r2, r1
        parent[r2] = r1
        if rank[r1] == rank[r2]:
            rank[r1] += 1
        return True
    
    mst = []
    for w, u, v in edges:
        if union(u, v):
            mst.append((w, u, v))
    
    return mst
```

**Prim's Algorithm（貪心 + Min-Heap）：**
```python
def prim_mst(graph, start):
    visited = {start}
    min_edges = [(w, start, v) for v, w in graph[start]]
    heapq.heapify(min_edges)
    mst = []
    
    while min_edges and len(visited) < len(graph):
        w, u, v = heapq.heappop(min_edges)
        if v in visited:
            continue
        visited.add(v)
        mst.append((w, u, v))
        for next_w, next_v in graph[v]:
            if next_v not in visited:
                heapq.heappush(min_edges, (next_w, v, next_v))
    
    return mst
```

---

## 🔥 Topic 4: Dynamic Programming vs Greedy（何時用哪個？）

### 決策樹
```
問題有「選擇」？
  │
  ├─ YES → 這個選擇是否 always lead to optimal solution？
  │           │
  │           ├─ YES → Greedy（快速，O(n) 或 O(n log n)）
  │           └─ NO → 需要比較所有選擇？ → DP
  │
  └─ NO → 問題可分解為子問題？ → DP

最佳策略：
  Greedy：活動選擇、霍夫曼編碼、最小生成樹、零錢貪心（特定coin系統）
  DP：編輯距離、最長公共子序列、背包問題、RNA二級結構
```

### 貪心 vs DP 實戰對比

| 問題 | 貪心 | DP | 原因 |
|------|------|-----|------|
| 活動選擇 | ✅ | ✅ | 貪心最優 |
| 哈夫曼編碼 | ✅ | ❌ | 貪心最優 |
| 0/1 背包 | ❌ | ✅ | 局部貪心不行 |
| 分數背包 | ✅ | ❌ | 貪心最優 |
| LCS | ❌ | ✅ | 沒辦法貪心 |
| 最短路徑 | Dijkstra ✅ | Bellman-Ford ✅ | 依邊權性質 |

---

## 🔥 Topic 5: Approximation Algorithms（近似演算法）

### 為什麼需要近似？
對於 NP-Hard 問題（如 Set Cover、Vertex Cover），我們無法在多項式時間找到最優解，但可以找到「保證接近最優」的近似解。

### 經典例子：Set Cover Problem
```python
def greedy_set_cover(universe, sets):
    """貪心 Set Cover - O(n²)"""
    covered = set()
    result = []
    
    while covered != universe:
        best_set = max(sets, key=lambda s: len(s - covered))
        result.append(best_set)
        covered |= best_set
    
    return result

# 貪心保證：解 ≤ H(n) × 最優解，其中 H(n) = 1 + 1/2 + ... + 1/n ≈ ln(n)
```

### Vertex Cover（點覆蓋）- 近似比 2
```python
def vertex_cover_approx(edges):
    """2-近似演算法"""
    cover = set()
    remaining_edges = edges.copy()
    
    while remaining_edges:
        # 選任意一條邊
        u, v = remaining_edges.pop()
        cover.add(u)
        cover.add(v)
        # 移除所有與 u, v 相連的邊
        remaining_edges = [(x, y) for x, y in remaining_edges 
                          if x not in (u, v) and y not in (u, v)]
    
    return cover
```

---

## 🔥 Topic 6: Complexity - Beyond P vs NP

### P = NP 問題的本質
```
問題的兩面：
  1. 找（Search）：找到一個解
  2. 驗證（Verify）：確認一個解是否正確

P（Polynomial time）：
  找和驗證都可以在多項式時間完成
  例：排序、最短路徑

NP（Non-deterministic Polynomial time）：
  驗證可以在多項式時間完成
  例：數獨（給定解答，驗證很快）
  
P = NP 問題：
  如果「驗證」很快，那「找」也很快嗎？
  （目前仍未解決，懸賞 100 萬美元）
```

### NP-Complete 證明技巧：歸約（Reduction）
```python
# 要證明問題 X 是 NP-Complete：
# 1. 證明 X ∈ NP（能在多項式時間驗證）
# 2. 證明 X 是 NP-Hard（找一個已知的 NPC 問題 Y，Y ∝ X）

# 經典歸約鏈：
# SAT → 3-SAT → Clique → Vertex Cover → Set Cover
```

---

## 💡 工程師蘇茉的 MIT 6.046 學習心得

### 6.006 vs 6.046 核心差異
```
6.006（基礎）：
  重點：「這是什麼演算法」「怎麼實作」
  
6.046（進階）：
  重點：「為什麼這個設計」「何時該用哪個」
  → 更強調設計技術和複雜度分析
```

### 重要新概念
```
新增的設計技巧：
  1. 隨機化演算法（避免最壞情況被攻擊）
  2. 近似演算法（處理 NP-Hard 問題的實務解法）
  3. 更多的複雜度理論（電路複雜度、概率複雜度）
  4. 密碼學基礎（零知識證明、安全計算）
```

### 面試重點（6.046 延伸）
```
除了 6.006 的內容，還要會：
  ✓ 攤銷分析（Amortized Analysis）
  ✓ 隨機 Quick Sort 的期望複雜度證明
  ✓ Greedy 的正確性證明（Exchange Argument）
  ✓ MST 的兩種貪心演算法（Kruskal / Prim）
  ✓ 近似演算法的近似比（Approximation Ratio）
```

### 實務應用場景
```
隨機 Quick Sort：幾乎所有現代程式語言的 sort 底層
Huffman Coding：JPEG、MP3、ZIP 壓縮標準
Kruskal/Prim MST：網路設計、電路板佈線、叢集分析
近似演算法：物流路徑優化、大規模組合最佳化
```

---

## 📅 學習Session記錄

### Session 4（2026-04-05）- MIT 6.046J 進階演算法

**今日重點：**
- Divide-and-Conquer：Master Theorem、Strassen 矩陣乘法
- Randomized Algorithms：Quick Sort、Quick Select、Universal Hashing
- Greedy Algorithms：Activity Selection、Huffman Coding、MST（Kruskal/Prim）
- Approximation Algorithms：Set Cover、Vertex Cover 近似比分析
- 複雜度理論：P vs NP 深入理解

**新理解：**
- Greedy 的正確性需要「貪心選擇性質」+「最優子結構」，不是所有問題都能貪心
- 隨機化是對抗最壞情況輸入（和攻擊者）的有效武器
- 當問題是 NP-Hard 時，近似演算法是務實的出路

**與 6.006 的銜接：**
- 6.006 讓我「會用」演算法
- 6.046 讓我「會選擇」和「會證明」

---

*本筆記由工程師蘇茉於 2026-04-05 整理自 MIT 6.046J OCW 課程*
*學習次數：第4次（進階演算法設計專題）*
# MIT 6.824 / 6.5840 - Distributed Systems（�????系統�?
**學�??��?�?* 2026-04-05
**課�?來�?�?* https://github.com/Developer-Y/cs-video-courses
**官方網�?�?* https://pdos.csail.mit.edu/6.824/
**?��??�本�?* MIT 6.5840 (Spring 2026)

---

## ?? 課�?概覽

MIT 6.824 ??MIT ?�?��??��????系統課�?，核心主題�?
- **Fault Tolerance（容?��?**
- **Replication（�?製�?**
- **Consistency（共識�?**

**?�課形�?�?* 論�??��? + 程�?實�? Lab（使??Go 語�?�?
**?�置?��?�?*
- 6.004（�?算�?組�?�?- 6.033（電?�網路�??��?等學�?- 紮實?��?式�??��?�?
---

## ?�� Topic 1: ?�散式系統�??�戰

### ?��?麼�?要�????系統�?```
?��??�頸�?  - ?�能上�??��??�單機硬�?  - ?��?容�??��?
  - 沒�?硬�??��??��?（Scale-up ?��??��?

?�散式解法�?
  ??水平?��?（Scale-out）�??��??�就?��??��???  ???��??�可?�性�?Fault Tolerance�?  ???�大?�儲存容??
�?���?  ??網路延遲（Network Latency�?  ??網路?�割（Network Partition�?  ??機器?��?（Machine Failure�?  ??Clock Skew（�??��??�步�?```

### ?�散式系統�?8?�失?��?（Fallacies of Distributed Computing�?```
1. 網路?�可?��?（The network is reliable�?2. 延遲?�零（Latency is zero�?3. ?�寬?�無?��?（Bandwidth is infinite�?4. 網路?��??��?（The network is secure�?5. ?�樸不�?變�?Topology doesn't change�?6. ?��?一?�管?�員（There is one administrator�?7. ?�輸?�本?�零（Transport cost is zero�?8. 網路?��?質�?（The network is homogeneous�?```

### 工�?師�?�?```
?�散式系統�??��??�盾�?  ?��??��??�系統�??��?一�??作�?
   但現實是網路?�延?�、�??��??��??��??��?不�??��?
?�?��????系統?�設計�??�是?��?
  Consistency（�??�性�??�Availability（可?�性�???  Partition Tolerance（�??�容忍�?三者�??��???  ??CAP Theorem
```

---

## ?�� Topic 2: MapReduce（�??��????計�?框架�?
### 什麼是 MapReduce�?Google ??2004 年�??��??�散式�??��??�模?��??�於大�?模�??��??�並行�?算�?
### ?��??�想：�??�治之�?Divide and Conquer�?```
Input ??Map（�?射�???Shuffle（�?組�???Reduce（歸納�???Output

Map ?�段�?  - 每�?worker ?��?輸入?��??��?
  - 輸出 (key, value) �?
Shuffle ?�段�?  - 將相??key ??value ?��??��?�?  - 網路?�輸：跨機器?��??��??��?�?
Reduce ?�段�?  - 每�?worker ?��?一??key ?��???value
  - ?��??�終輸??```

### Word Count 範�?（�???MapReduce 程�?�?```go
// Map ?�數：�?算�??�單字出?�次??func mapFun(filename string, content string) []map.KeyValue {
    f := func(r rune) bool { return !unicode.IsLetter(r) }
    words := strings.FieldsFunc(content, f)
    var kvs []map.KeyValue
    for _, w := range words {
        kvs = append(kvs, map.KeyValue{w, "1"})
    }
    return kvs
}

// Reduce ?�數：�??��? key ??count ?��?
func reduceFun(key string, values []string) string {
    return strconv.Itoa(len(values))
}
```

### MapReduce ??Fault Tolerance 設�?
```
Master 追蹤每�?Map/Reduce worker ?��??��?
  - 如�? Map worker 失�?：�??�執行該 task
  - 如�? Reduce worker 失�?：�??�執行該 task

?��?：Map ?�輸?��??�本?��?碟�?Reduce 任�?完�?後就?�除
      ???�援任�??�執行�?不�?要�?複整??job
```

### 工�?師�?�?```
MapReduce ?�貢?��?
  - 讓�??��????系統?�工程師也能寫平行�?�?  - ?��?了網路通�??��?載平衡、失?��???
?�制�?  - ?��??�簡?��? key-value ?��???  - 不適?��?要「跨記�??�?�」�??�迭�?���?任�?
  ???��?�?Spark?�Flink 等更?��??��???```

---

## ?�� Topic 3: RAFT ?��?演�?法�?一?�性核心�?⭐�?�?
### ?��?麼�?要共識�?算�?�?```
?�散式系統�??��??��?�?  - 多個副?��?replica）�?何�??��??��??��?
  - ?��?機器?��??��?如�?繼�??��?�?  - 如�?確�??��?一?�副?�接?�寫?��?

?��?演�?法�?Consensus Algorithm）�??��?�?  讓�?群�??�就?��??�值」�??��??��?決�?

�?��作�?�?  - Paxos�?Leslie Lamport�?998�?  - Raft（Diego Ongaro & John Ousterhout�?014�?```

### RAFT ?�核心設計目�?```
1. Understandability（可?�解?��???Raft ?�主要貢??2. 沒�?歧義?�實??3. ?��???leader election

Raft 將�?題�?�?��三個相對獨立�?子�?題�?
  1. Leader Election（�?導者選?��?
  2. Log Replication（日誌�?製�?
  3. Safety（�??�性�?
```

### RAFT 三種角色
```
1. Follower（追?�者�?�?   - 被�??�收來自 leader ?��?跳�??��?
   - 如�?超�?沒收?��?跳�?轉為 Candidate

2. Candidate（候選?��?�?   - ?�其他伺?�器?�起?�票請�?
   - ?��?多數票�??�為??Leader

3. Leader（�?導者�?�?   - ?��??�?�客?�端請�?
   - ?�送�?跳�??��?導地�?   - 複製?��???followers
```

### Leader Election（�?導者選?��?
```
?��?流�?�?  1. Follower 等�? heartbeat 超�?（通常 150-300ms�?  2. 轉為 Candidate，�???currentTerm
  3. ?�票給自�?  4. ?��??�伺?�器?��?RequestVote RPC
  5. 如�??��?多數票�??�為 Leader

?��?：�??�任?��?Term）�?多只?��???Leader
?��?：�??��?票給?�日誌�??�己?�」�? Candidate
```

### Log Replication（日誌�?製�?
```
Leader ?�職責�?
  1. ?�收客戶端�?求�??�令�?  2. 將命令追?�到?�地?��?
  3. ?��?AppendEntries RPC �?followers
  4. 等�?多數派確�?  5. 套用?�令?��??��?，�??�客?�端

?��?結�?�?  Entry = {term, index, command}
  
  ?��??�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�??  ?? Term  ?? Index  ??       Command            ??  ?��??�?�?�?�?�?�?�?��??�?�?�?�?�?�?�?�?��??�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�??  ??  1    ??   1    ?? SET x = 5                ??  ??  1    ??   2    ?? SET y = 3                ??  ??  2    ??   3    ?? SET x = 7                ?? ??Leader
  ??  2    ??   4    ?? SET z = 2                ??  ?��??�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�??```

### RAFT vs Paxos（工程師比�?�?```
Paxos�?  - ?��??��??�實，�?極難?�解?�實??  - ?��??��?決�?（single-decree Paxos�?  - ?�產實現往往?�離論�?

Raft�?  - 強調?��?�?�?  - ?�解清晰，�??�實??  - 實�?系統?�用�??（etcd, CockroachDB, TiKV, Consul�?
業�??�用 Raft ?�系統�?
  - etcd（Kubernetes ?��???? key-value store�?  - TiKV（TiDB ?�儲存�??��?
  - CockroachDB
  - Consul
```

---

## ?�� Topic 4: Go 語�?併發模�?（�????系統實戰�?
### ?��?麼�????系統??Go�?```
Go ?��?大殺?�鐧�?  1. Goroutine：�??��??��?緒�??��??��??�個�?費�?
  2. Channel：goroutine ?��?安全?��?機制
  3. 簡單?��?法�?�?C++/Java ?�適?�系統�?�?```

### 併發??Word Count（MapReduce 概念�?```go
func MapReduce(
    mapFun func(string, string) []KeyValue,
    reduceFun func(string, []string) string,
) {
    // 讀?��??�輸?��?�?    files := readFiles("input/*")
    
    // 並�??��? Map
    ch := make(chan []KeyValue, len(files))
    for _, file := range files {
        go func(f string) {
            content := readFile(f)
            ch <- mapFun(f, content)
        }(file)
    }
    
    // ?��? Map 結�?
    var kvs []KeyValue
    for range files {
        kvs = append(kvs, <-ch...)
    }
    
    // ?��?（Shuffle�?    groups := make(map[string][]string)
    for _, kv := range kvs {
        groups[kv.Key] = append(groups[kv.Key], kv.Value)
    }
    
    // 並�??��? Reduce
    resultCh := make(chan string)
    for k, vs := range groups {
        go func(key string, values []string) {
            resultCh <- fmt.Sprintf("%s: %s", key, reduceFun(key, values))
        }(k, vs)
    }
    
    // ?��?結�?
    for range groups {
        fmt.Println(<-resultCh)
    }
}
```

### Mutex vs Channel（�??�用?�個�?
```
Mutex�?  - 保護?�享?�「�??��?  - ?��?讀寫�?平衡?�場??  - 例�?：�??�器?�快??
Channel�?  - ?��??��?件傳?�」�??�pipeline??  - ?��??�任?��??��?  - 例�?：工作者�??��??��?消費??```

---

## ?�� Topic 5: 複製?��??�性�?Replication & Consistency�?
### 一?�性模?��?�?```
強�??�性�?Strong Consistency）�?
  - 讀?�總?��??��??��?寫入
  - �?��：�??�差?�可?�性�?
  - 例�?：Strict Serializability

?��?一?�性�?Sequential Consistency）�?
  - ?�?�客?�端?�到?��??��?作�?�?  - 例�?：�??��?緒�?式�?記憶體�?�?
?��?一?�性�?Causal Consistency）�?
  - ?��?證�??��??��??��?作�?�?  - 例�?：社群�?體�??��?覆」�???
?�終�??�性�?Eventual Consistency）�?
  - 不�?證�??��??��??�終�?一??  - �?��：客?�端?�能讀?��??��???  - 例�?：DynamoDB, Cassandra
```

### CAP Theorem（�??�斯定�?�?```
?�散式系統�??�能?��?滿足三者�?
  1. Consistency（�??�性�?
  2. Availability（可?�性�?
  3. Partition Tolerance（�??�容忍�?

?�能?��?滿足?�者�?
  - CA（�??�能存在）�?不放�?P
  - CP（�??��?+ ?�割容�?）�?網路?�割?�犧?�可?��?  - AP（可?��?+ ?�割容�?）�?網路?�割?�犧?��??��?
實�?系統?�選?��?
  - CP：ZooKeeper, etcd, HBase
  - AP：DynamoDB, Cassandra, CouchDB
```

---

## ?�� Topic 6: GFS（Google File System�? 大�?模�?????��?

### GFS ?�設計�?�?```
Google ??2003 年�??��??�散式�?案系統�?
  - 大�? commodity hardware（�??�硬體�?
  - 檔�?很大（GB 等�?�?  - 主�?讀?�模式�?大�??��?讀?��??�隨機�?
  - ?�要�?度容忍硬體�???```

### GFS ?��?
```
                    ?��??�?�?�?�?�?�?�?�?�?�?�?�??                    ??  Master    ?? ???��? Master（�?資�?管�?�?                    ?��??�?�?�?�?�?��??�?�?�?�?�??                           ??              ?��??�?�?�?�?�?�?�?�?�?�?�?��??�?�?�?�?�?�?�?�?�?�?�??              ??           ??           ??         ?��??�?�?�?��??�?�?? ?��??�?�?�?��??�?�?? ?��??�?�?�?��??�?�??         ?�ChunkServer???�ChunkServer???�ChunkServer??         ??  (1)   ?? ??  (2)   ?? ??  (3)   ??         ?��??�?�?�?�?�?�?�?�?? ?��??�?�?�?�?�?�?�?�?? ?��??�?�?�?�?�?�?�?�??
?��?�?  - 每個�?案�??�固定大小�? chunk�?4MB�?  - 每�?chunk ?��???chunkserver 上�?製�??�設 3 份�?
  - Master ?��??��??��?檔�??�稱?�chunk 位置�?```

### GFS ??Fault Tolerance
```
Chunk Server ?��?�?  - Master ?�測?��?跳中??  - ?�其�?chunkserver 上�??��?�?chunks
  - 維�??�設?��?製�?子�?replication factor�?
Master ?��?�?  - ?��??��?（Single Point of Failure）�? GFS ?�主要詬??  - 後�? Colossus（Google ?�部）改?��??��?�?```

---

## ?�� Topic 7: Spanner（全?��????資�?庫�?

### Spanner ?��???```
Google ?�全?��?????�聯式�??�庫�?  - ?�擴展至?�百?�台機器
  - ?��??��?（跨資�?中�??�跨 region�?  - ?��?強�??�性�?外部一?�性�?
  - 使用 TrueTime API 實現跨地?��?�?```

### TrueTime（�??��?步�?
```
?��?：�????系統中�?不�?機器?��??��??��?差�?Clock Skew�?
TrueTime �??�?  - 使用 GPS ?�收??+ ?��???  - 每台伺�??��??�兩種�???  - ?��??��?確�??��??�」�?[earliest, latest]

  ?��??�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�??  ?? TrueTime API�?                   ??  ?? TT.now() ??TTinterval             ??  ?? { earliest: 10:00:00.000,         ??  ??   latest:  10:00:00.200 }         ??  ?��??�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�??
  每個寫?�都?��??�戳：TT.now().latest
  讀?��?等TT.after(commit_ts)確�??��???```

---

## ?�� Topic 8: ZooKeeper（�?????�調?��?�?
### ZooKeeper ?��?麼�?
```
?�散式系統�??�幫?�」�?
  - ?��??�散式�?
  - ?��??�選??  - 組�?管�?
  - ?��??�現

使用?�景�?  - Kafka?��??��?調�?broker ?��???���?  - HBase ?��?導者選??  - YARN ?��?源管??```

---

## ?�� 工�?師�??��?學�?心�?

### ?��?麼選 MIT 6.824�?```
作為軟�?工�?師�??�散式系統是必�??��?�?  - ?�?�大?�網路�??��?Netflix, Google, AWS）都?��????系統
  - ?�試必考�?CAP Theorem?�RAFT?�共識�?�?  - 工�?必用：Kafka?�Redis Cluster?�Kubernetes

MIT 6.824 ?�特?��?
  - 論�?驅�?學�?（而�?純�?論�?
  - ?�實?��? Go 程�? Lab（�??��?上�??��?
  - 涵�??�代?�散式系統�??��??��?```

### ?�散式系�?vs ?��?系統?�核心差??```
?��?系統�?  ??記憶體共享�??�接讀寫共享�??��?
  ??簡單?��??�性模?��??�?�執行�??�到?��??�?��?
  ??失�?模�?簡單（進�?崩潰就直?��??��?

?�散式系統�?
  ??網路延遲?��??��?
  ???��?機器?��?不影?�整�?  ??一?�性模?��??��?要考慮網路?�割�?```

### Lab 實�?建議
```
Lab 1: MapReduce（Word Count 並�??��?
  ???�解?�散式�?算�??�本範�?

Lab 2: Key-Value Server（單機�? Raft KV Store�?  ????Lab 3 ?�身

Lab 3: Raft（共識�?算�?實現�?  ???�是 6.824 ?�??? Lab
  ??實現 Leader Election ?�日誌�?�?  ??建議：�?讀�?Raft Paper 三�??��?�?
Lab 4: Sharded KV Server（�? Raft Group�?  ??�?Raft ?��??�水平擴�?
Lab 5: Sharded Backup Server（�??��?移�?
  ???�入?�伺?�器不影?��???```

### ?�試高頻?��?
```
1. CAP Theorem：解?�並?��?（CP vs AP 系統�?2. RAFT�?   - 三種角色?��???   - Leader Election 流�?
   - Log Replication 流�?
   - 如�??��?網路?�割
3. 一?�性模?��?強�??�性、�?序�??�性、�?終�??��?4. ?�散式�??��?2PC??PL?�Saga
5. Vector Clock：解決�?件�?序�?�?```

### 實�??�用?�景
```
Kafka / RabbitMQ�?  - ?�於?��??��??�系�?  - Partition + Replication

Redis Cluster�?  - ?�散�?Cache
  - Hash slot ?��?

Kubernetes�?  - etcd（RAFT ?��?）儲存叢?��???  - API Server 作為?��??�單一?�相來�?

Cassandra�?  - AP 系統（可?��?+ ?�割容�?�?  - LSM Tree ?��?引�?
```

---

## ?? 學�?Session記�?

### Session 5�?026-04-05�? MIT 6.824 ?�散式系統入?�

**今日?��?�?*
- ?�散式系統�?8大失?��?（Fallacies�?- MapReduce ?�散式�?算�?�?- CAP Theorem（�??�性、可?�性、�??�容忍�?
- RAFT ?��?演�?法�?Leader Election + Log Replication�?- Go 語�?併發模�?（�????系統實�?工具�?- GFS 大�?模�?????��?
- Spanner ?��??�散式�??�庫
- ZooKeeper ?�散式�?調�???
**?��?�??**
- ?�散式系統�??�質?�在?��??�性」�??�可?�性」�??��???- RAFT �?Paxos 複�??�共識�?題�?�?��三個可?�解?�部??- MapReduce ?�貢?��??��??��??�是讓「�??�工程師?��??�寫?�散式�?�?- TrueTime ?�「�??��?確�??��??�」是一?�優?��?工�?�??

**?��??�學習�??�接�?*
- 演�?法知識�?BFS/DFS?�Graph）用?��????系統?��?樸管??- 併發?�制概念（�??��?業系統�??��?�?RAFT ?�基�?
---

## ?�� 後�?學�?計畫

```
Q2 2026:
  ??6.824 Labs（�??��???5 ??Lab�?  ???��?經典論�?（BigTable, Dynamo, Cassandra�?  
Q3 2026:
  ??CMU 15-445 Database Systems（�??�庫系統�?  ??實�?一?�簡?��? Raft KV Store

Q4 2026:
  ???�端?��?（AWM, GCP, Azure 深入�?  ???�散式系統面試�?強�?
```

---

*?��?記由工�?師�??�於 2026-04-05 ?��???MIT 6.824 / 6.5840 OCW 課�?*
*學�?次數：第5次�??�散式系統�?題�?*


# MIT 6.1810 - Operating Systems（作業系統）
**學習日期：** 2026-04-05
**課程來源：** https://github.com/Developer-Y/cs-video-courses
**官方網站：** https://pdos.csail.mit.edu/6.828/2025/
**學習範圍：** Lectures 1-13（Introduction 到 Thread Switching）

---

## 課程概覽

MIT 6.1810 是 MIT 最經典的作業系統課程，前身為 6.828。課程使用 **xv6**（一個用 C 寫的簡化版 Unix）作為教學作業系統，學生需要完成 6 個核心 Labs。

**核心 Topics：**
- OS 設計理念與架構
- 行程管理、系統呼叫
- 分頁表與虛擬記憶體
- 陷阱與中斷
- 鎖與併發
- 檔案系統

---

## Lecture 1: Introduction to Operating Systems

### OS 的兩大職責
1. **Abstract Hardware** - 把複雜硬體封裝成簡單介面（檔案、行程、socket）
2. **Manage Resources** - CPU 排程、記憶體管理、I/O 管理、保護隔離

### xv6 簡介
xv6 是 MIT 教學用的作業系統，程式碼公開於 GitHub (mit-pdos/xv6-riscv)，使用 RISC-V 處理器架構，是一個簡化的 Unix v6 教學版本。

### OS 三大抽象
`
1. 行程（Process）→ 讓每個程式以為自己有整台機器
2. 檔案（File）→ 讓所有 I/O 都像讀寫檔案
3. 位址空間（Address Space）→ 讓每個程式以為自己有連續記憶體
`

---

## Lecture 2: C in xv6

### 為什麼 OS 用 C 寫？
- 可預測的記憶體佈局（連續陣列）
- 指標操作與直接記憶體存取
- 沒有 GC（可預測的效能）
- 直接硬體操作能力

### 記憶體佈局
`
高位址：Stack（向下生長）
        Heap（向上生長，malloc/free 管理）
        BSS / Data（全域變數）
低位址：Text（程式碼，唯讀）
`

---

## Lecture 3: OS Design

### 兩大 OS 設計典範

#### Monolithic Kernel（巨大核心）
- Linux、Unix、xv6 都採用這個模式
- 所有作業系統服務都在核心空間執行
- 優點：效能好；缺點：一個模組 bug 可能崩潰整個系統

#### Microkernel（微核心）
- MINIX、QNX、L4 使用這個模式
- 只把最核心的功能放核心空間（排程、基本 IPC）
- 優點：更穩定；缺點：跨模組 IPC 代價高

---

## Lecture 4: OS Organization

### 隔離原則（Isolation）
`
OS 必須隔離行程，防止一個行程崩潰影響其他行程：
- 空間隔離：每個行程有自己的虛擬記憶體
- 時間隔離：CPU 時間片分配，強制的上下文切換
硬體支援：分頁表、特權模式、使用者模式
`

### 系統呼叫流程
`
使用者呼叫 read()：
1. 使用者空間：呼叫 C library 的 read()
2. 觸發系統呼叫：ecall 指令
3. 切換到核心模式：CPU 跳到 kernel entry point
4. 核心處理：根據系統呼叫號碼分派到 sys_read
5. 返回使用者空間：攜帶回傳值
`

---

## Lecture 5: Page Tables 分頁表（核心！）

### 為什麼需要分頁表？
`
問題：多個行程共享實體記憶體，但每個行程需要自己的虛擬位址空間
解決：分頁表（Page Table）

Process A 的虛擬位址 0x1000 → 實體位址 0x8000
Process B 的虛擬位址 0x1000 → 實體位址 0x9000

好處：隔離、簡化分配、交換、記憶體共享、保護
`

### xv6/RISC-V 三層分頁
`
虛擬位址（39 bits）：
[ VPN[2] | VPN[1] | VPN[0] | offset (12 bits) ]
     │          │         │
     ↓          ↓         ↓
 Level 2    Level 1    Level 0
 分頁目錄    分頁目錄    分頁表
`

### 分頁表條目（PTE）Flags
`
PTE_R = 0x001  // 可讀
PTE_W = 0x010  // 可寫
PTE_X = 0x100  // 可執行
PTE_U = 0x200  // 使用者模式可訪問
PTE_V = 0x400  // 有效（是否映射到實體頁）
`

---

## Lecture 6: System Call Entry/Exit

### RISC-V 三種觸發核心的機制
`
1. 系統呼叫（System Call）：使用者明確請求核心服務（ecall）
2. 例外（Exception）：使用者執行了非法操作（除以零、存取無效記憶體）
3. 中斷（Interrupt）：硬體設備發出的非同步信號（時鐘、磁碟、網路）
`

### 上下文切換代價（面試高頻！）
`
系統呼叫的代價：
1. 觸發軟體中斷（ecall）：約 100-1000 cycles
2. 暫存器保存（save context）：約 50-200 cycles
3. 分頁表切換（如有必要）：約 100-500 cycles
4. 返回使用者空間：約 100-500 cycles
總結：一次 read() 可能需要 1000+ CPU cycles
`

---

## Lecture 7: System Call Interposition

### 什麼是系統呼叫攔截？
讓外部程式監控/控制某行程的系統呼叫行為（strace, dtrace, 沙箱、安全監控）。

strace 原理：ptrace() 系統呼叫可以 attached 到目標行程，每次目標行程執行系統呼叫都會觸發 SIGTRAP。

---

## Lecture 8: Page Faults 分頁錯誤（核心！）

### 分頁錯誤的三種類型
`
1. 硬性分頁錯誤（Hard Page Fault）：
   分頁不在記憶體中（在磁碟 swap 區），需從磁碟讀取，代價極高

2. 軟性分頁錯誤（Soft Page Fault）：
   分頁在記憶體中但尚未映射，只需建立映射，代價低

3. 無效分頁錯誤（Invalid Page Fault）：
   行程存取了不應該存在的虛擬位址，發送 SIGSEGV
`

### Copy-on-Write（寫時複製）
`
傳統 fork()：複製整個父行程的記憶體，代價極高
COW fork()：
- fork() 時不複製記憶體，只共享分頁表，共享分頁標記唯讀
- 當任一行程嘗試寫入時，CPU 觸發分頁錯誤
- OS 處理：複製該分頁、更新分頁表、解除唯讀
優點：fork() 代價極低、延後複製、記憶體效率高
`

### Demand Paging（需求分頁）
`
exec() 只建立分頁表，不複製程式碼/資料
分頁在真正被存取時（page fault）才載入
好處：加速程式啟動、減少記憶體使用、讓程式可執行比記憶體更大的檔案
`

---

## Lecture 9: Super Pages（超大分頁）

### 為什麼需要 Super Pages？
`
問題：4KB 分頁對大型應用來說 TLB miss 太多
解決：Super Pages（2MB、1GB）
- 一個 TLB 條目覆蓋更大記憶體範圍
- 減少 TLB miss
Linux huge pages：echo 10 > /proc/sys/vm/nr_hugepages
`

---

## Lecture 10: Virtual Memory for Applications

### malloc/free 的底層
`
malloc/free 不是系統呼叫，是 C library函數
- 小型配置（<128KB）：調用 brk() 擴展 heap
- 大型配置（>128KB）：調用 mmap() 分配 anonymous pages
常見 allocator：dlmalloc, jemalloc, tcmalloc
`

### mmap 的使用
`c
void *mmap(void *addr, size_t len, int prot, int flags, int fd, off_t offset);
// 將檔案映射到行程的虛擬記憶體
// 讀取 mapped[i] 相當於讀取檔案的第 i 個位元組
`

---

## Lecture 11: Device Drivers

### 中斷驅動 I/O
`
同步讀取（阻塞）：
1. 行程呼叫 read()
2. 驅動啟動磁碟讀取，行程進入睡眠（sleep()）
3. 磁碟完成讀取，發出中斷
4. 驅動處理中斷，將資料複製到使用者空間
5. 喚醒行程（wakeup()）

非同步 I/O（Linux aio）：
行程發出 I/O 請求後立即返回，I/O 完成後通過 signal/epoll 通知
`

---

## Lecture 12: Locking 鎖（核心！）

### 自旋鎖（Spinlock）
`c
while(__sync_lock_test_and_set(&lk->locked, 1)) ;  // 忙等待
// 適用：鎖持有時間極短（<1微秒）
// 缺點：浪費 CPU cycles
`

### 睡眠鎖（Sleep Lock）
`
特色：獲得鎖失敗時，行程進入睡眠狀態
適用：鎖持有時間較長（I/O 操作）
優點：不浪費 CPU
Linux 檔案系統使用睡眠鎖
`

### 死結四個必要條件（面試高頻！）
`
1. 互斥（Mutual Exclusion）：資源每次只能被一個執行緒持有
2. 持有並等待（Hold and Wait）：執行緒持有 A 同時等待 B
3. 不搶奪（No Preemption）：資源不能被強制奪走
4. 循環等待（Circular Wait）：存在執行緒的循環等待鏈
避免策略：破壞任一條件即可（固定順序取得多個鎖）
`

### Mutex vs Semaphore
`
Mutex：一次只有一個執行緒可以持有，有擁有權
Semaphore：計數器可被多執行緒增加/減少，用於 producer-consumer
`

---

## Lecture 13: Thread Switching 執行緒切換（核心！）

### 行程 vs 執行緒
`
行程：獨立位址空間、獨立開啟檔案表、切換代價高
執行緒：共享同一行程的位址空間、共享開啟檔案、切換代價低（10-100倍快）
`

### xv6 的執行緒切換
`c
// 上下文切換的本質：保存和恢復 CPU 暫存器
void scheduler(void) {
  for(;;){
    for(p = proc; p < &proc[NPROC]; p++){
      if(p->state != RUNNABLE) continue;
      c->proc = p;
      p->state = RUNNING;
      swtch(&c->context, p->context);  // 切換上下文
      c->proc = 0;
    }
  }
}
`

### 搶占式排程
`
xv6 採用搶占式排程：
- 時鐘中斷（100Hz）強制 CPU 從當前行程離開
- 即使行程不主動放棄 CPU，也會被強制切換
- 防止一個行程霸佔整個 CPU
`

---

## 工程師蘇茉的學習心得

### 為什麼選作業系統？
`
已完成：
  Session 3: MIT 6.006 演算法基礎
  Session 4: MIT 6.046 進階演算法設計
  Session 5: MIT 6.824 分散式系統

作業系統填補單機資源管理的知識空白：
- 分散式系統的每台機器都是一個作業系統
- 了解行程、鎖、記憶體管理，才能設計好分散式系統
- 面試高頻：行程/執行緒差異、死結、鎖、記憶體管理
`

### OS 核心概念地圖
`
                OS Kernel
        ┌────────┴────────┐
        │                 │
   Process          Memory           I/O
   Management       Management       Management
        │                 │              │
     Scheduling       Page Tables    File System
     Lock/Sync       VM/mmap        Device Driver
`

### 面試高頻 OS 問題
`
Q: 行程 vs 執行緒的核心差異？
A: 行程有獨立位址空間，執行緒共享位址空間

Q: 死結的四個條件？
A: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait

Q: 硬性 vs 軟性分頁錯誤？
A: 前者需要磁碟 I/O，後者只需建立映射

Q: Copy-on-Write 如何優化 fork()？
A: 共享唯讀分頁，只有寫入時才複製
`

### xv6 Labs 實作順序建議
`
Lab 1: Unix Utilities（warm-up）
Lab 2: System Calls（核心）
Lab 3: Page Tables（記憶體管理）
Lab 4: Traps（陷阱機制）
Lab 5: Copy-on-Write Fork（進階）
Lab 6: Network Driver（網路）
`

---

## 後續學習計畫

`
Q2 2026:
  □ 完成 MIT 6.1810 xv6 Labs
  □ 複習 MIT 6.824 Labs
  □ 經典論文（BigTable, Dynamo, Cassandra）

Q3 2026:
  □ CMU 15-445 Database Systems
  □ 實作一個簡單的 Raft KV Store

Q4 2026:
  □ 雲端平台深入（GCP/AWS/Azure）
  □ 分散式系統面試衝刺
`

---

*本筆記由工程師蘇茉於 2026-04-05 整理自 MIT 6.1810 OCW 課程*
*學習次數：第6次（作業系統專題）*

---

# MIT 6.5840 - Distributed Systems（分散式系統）

**學習日期：** 2026-04-05
**課程來源：** https://github.com/Developer-Y/cs-video-courses
**官方網站：** https://pdos.csail.mit.edu/6.824/
**當前學期：** MIT 6.5840 Spring 2026（Formerly 6.824）

---

## 📚 課程概覽

MIT 6.5840 是 MIT 最經典的分散式系統課程，核心主題：
- **Fault Tolerance（容錯）**
- **Replication（複製）**
- **Consistency（共識）**

**授課形式：** 論文閱讀 + 程式實驗 Lab（使用 Go 語言）
**先修知識：** 6.004（計算機組織）+ 6.033（電腦網路）+ 紮實程式設計經驗

---

## 🔥 Topic 1: 分散式系統的8大誤判

### 為什麼需要分散式系統？
```
單機瓶頸：
  - 無法突破單機硬體限制
  - 必須容錯（單機故障等於全系統故障）

分散式解法：
  ✓ 水平擴展（Scale-out）
  ✓ 高可用性（Fault Tolerance）
  ✓ 大規模儲存容量

但是帶來的挑戰：
  ✗ 網路延遲（Network Latency）
  ✗ 網路分割（Network Partition）
  ✗ 機器故障（Machine Failure）
  ✗ Clock Skew（時鐘不同步）
```

### 分散式系統的8大誤判（Fallacies of Distributed Computing）
```
1. 網路是可靠的（The network is reliable）
2. 延遲為零（Latency is zero）
3. 頻寬無限（Bandwidth is infinite）
4. 網路是安全的（The network is secure）
5. 拓撲不改變（Topology doesn't change）
6. 有一個管理者（There is one administrator）
7. 傳輸成本為零（Transport cost is zero）
8. 網路是同質的（The network is homogeneous）
```

### 工程師觀點
```
分散式系統設計的核心矛盾：
  一致性（Consistency）vs 可用性（Availability）vs 分區容忍（Partition Tolerance）
  → CAP Theorem

真實世界的取捨：
  - 強一致性犧牲可用性：銀行轉帳
  - 高可用性犧牲一致性：社群網站貼文
```

---

## 🔥 Topic 2: MapReduce（分歧-合併計算框架）

### 什麼是 MapReduce？
Google 於2004年發表的分散式平行計算框架，用於大規模資料的並行處理。

### 核心思想：分治法（Divide and Conquer）
```
Input → Map（映射）→ Shuffle（分組）→ Reduce（歸納）→ Output

Map 階段：
  - 每個 worker 處理輸入分片
  - 輸出 (key, value) 對
Shuffle 階段：
  - 將相同 key 的 value 集合在一起
  - 網路傳輸：跨機器分配
Reduce 階段：
  - 每個 worker 處理一個 key 的所有 value
  - 輸出最終結果
```

### Word Count 範例（Go MapReduce 程式）
```go
// Map 函數：計算每個單字出現次數
func mapFun(filename string, content string) []map.KeyValue {
    f := func(r rune) bool { return !unicode.IsLetter(r) }
    words := strings.FieldsFunc(content, f)
    var kvs []map.KeyValue
    for _, w := range words {
        kvs = append(kvs, map.KeyValue{w, "1"})
    }
    return kvs
}

// Reduce 函數：對相同 key 的 count 求和
func reduceFun(key string, values []string) string {
    return strconv.Itoa(len(values))
}
```

### MapReduce 的 Fault Tolerance 設計
```
Master 追蹤每個 Map/Reduce worker 狀態：
  - 如果 Map worker 故障：重新執行該 task
  - 如果 Reduce worker 故障：重新執行該 task

關鍵：Map 輸出寫入本地磁碟，Reduce 任務完成後就刪除
      這樣可以重複執行而不需要重複整個 job
```

### 工程師觀點
```
MapReduce 的貢獻：
  - 讓不懂網路的工程師也能寫平行程式
  - 自動處理網路傳輸、負載平衡、故障恢復

限制：
  - 只能處理簡單的 key-value 映射
  - 不適合需要「跨記錄」狀態迭代的任務
  → 後來催生了 Spark、Flink 等更進階框架
```

---

## 🔥 Topic 3: RAFT 共識演算法（一致性核心）⭐⭐⭐

### 為什麼需要共識演算法？
```
分散式系統的核心問題：
  - 多個副本（replica）如何保持一致？
  - 某台機器故障，如何繼續服務？
  - 如何確保所有客戶端寫入都正確同步？

共識演算法（Consensus Algorithm）就是為了解決這個問題：
  讓一群伺服器就「某個值」達成一致決策

兩個代表：
  - Paxos（Leslie Lamport, 1998）
  - Raft（Diego Ongaro & John Ousterhout, 2014）
```

### RAFT 的核心設計目標
```
1. Understandability（可理解性）— Raft 的主要貢獻
2. 沒有歧義的明確規格
3. 簡化 leader election

Raft 將問題分解為三個相對獨立的子問題：
  1. Leader Election（領導者選舉）
  2. Log Replication（日誌複製）
  3. Safety（安全性）
```

### RAFT 三種角色
```
1. Follower（追隨者）：
   - 被動接收來自 leader 的心跳
   - 如果超時沒收到心跳，轉為 Candidate

2. Candidate（候選者）：
   - 向其他伺服器發起投票請求
   - 獲得多數票者成為 Leader

3. Leader（領導者）：
   - 處理客戶端請求
   - 發送心跳維持領導地位
   - 複製日誌到 followers
```

### Leader Election（領導者選舉）
```
選舉流程：
  1. Follower 等候心跳超時（通常 150-300ms）
  2. 轉為 Candidate，增加 currentTerm
  3. 投票給自己
  4. 向所有伺服器發送 RequestVote RPC
  5. 如果獲得多數票，成為 Leader

關鍵：任期（Term）是邏輯時鐘，每個 Term 只會有一個 Leader
關鍵：候選人只投票給「日誌至少和自己一樣新」的 Candidate
```

### Log Replication（日誌複製）
```
Leader 的職責：
  1. 接收客戶端請求（命令）
  2. 將命令追加到本地日誌
  3. 發送 AppendEntries RPC 給 followers
  4. 等候多數派確認
  5. 套用命令到狀態機，返回客戶端

日誌結構：
  Entry = {term, index, command}
  ┌──────┬───────┬─────────────────┐
  │ Term │ Index │    Command      │
  ├──────┼───────┼─────────────────┤
  │  1   │   1   │  SET x = 5      │
  │  1   │   2   │  SET y = 3      │
  │  2   │   3   │  SET x = 7      │ ← Leader
  │  2   │   4   │  SET z = 2      │
  └──────┴───────┴─────────────────┘
```

### RAFT vs Paxos（工程師比較）
```
Paxos：
  - 理論優雅但極難理解和實現
  - 只解決單一決定（single-decree Paxos）
  - 工業實現往往偏離論文

Raft：
  - 強調可理解性
  - 目標清晰，容易實現
  - 工業系統採用多（etcd, CockroachDB, TiKV, Consul）

實際應用 Raft 的系統：
  - etcd（Kubernetes 背後的 key-value store）
  - TiKV（TiDB 的儲存引擎）
  - CockroachDB
  - Consul
```

---

## 🔥 Topic 4: Go 語言併發模型（分散式系統實戰）

### 為什麼分散式系統用Go？
```
Go 的殺手級特性：
  1. Goroutine：輕量級執行緒，創建成本極低
  2. Channel：goroutine間安全通訊機制
  3. 簡單高效的併發語法（比 C++/Java 更適合系統程式）
```

### Goroutine + Channel 範例（並行 MapReduce）
```go
func MapReduce(
    mapFun func(string, string) []KeyValue,
    reduceFun func(string, []string) string,
) {
    // 讀取所有輸入檔案
    files := readFiles("input/*")

    // 並行執行 Map
    ch := make(chan []KeyValue, len(files))
    for _, file := range files {
        go func(f string) {
            content := readFile(f)
            ch <- mapFun(f, content)
        }(file)
    }

    // 收集 Map 結果
    var kvs []KeyValue
    for range files {
        kvs = append(kvs, <-ch...)
    }

    // 分組（Shuffle）
    groups := make(map[string][]string)
    for _, kv := range kvs {
        groups[kv.Key] = append(groups[kv.Key], kv.Value)
    }

    // 並行執行 Reduce
    resultCh := make(chan string)
    for k, vs := range groups {
        go func(key string, values []string) {
            resultCh <- fmt.Sprintf("%s: %s", key, reduceFun(key, values))
        }(k, vs)
    }

    // 收集結果
    for range groups {
        fmt.Println(<-resultCh)
    }
}
```

### Mutex vs Channel（何時用哪個）
```
Mutex：
  - 保護共享資料的「互斥訪問」
  - 適合讀寫平衡的場景
  - 例項：計數器、快取

Channel：
  - 傳遞「工作任務」或「事件」
  - 適合 pipeline、生產者-消費者
  - 例項：工作者池、任務分派
```

---

## 🔥 Topic 5: 複製與一致性（Replication & Consistency）

### 一致性模型層級
```
強一致性（Strong Consistency）：
  - 讀取總是返回最新寫入
  - 代價：犧牲可用性
  - 例項：Strict Serializability

順序一致性（Sequential Consistency）：
  - 所有客戶端看到相同的操作順序
  - 例項：多執行緒程式的記憶體順序

因果一致性（Causal Consistency）：
  - 只保證有因果關係的操作順序
  - 例項：社群媒體「回覆覆」

最終一致性（Eventual Consistency）：
  - 不保證何時，但最終會一致
  - 代價：客戶端可能讀到過時資料
  - 例項：DynamoDB, Cassandra
```

### CAP Theorem（布魯爾定理）
```
分散式系統不可能同時滿足三者：
  1. Consistency（一致性）
  2. Availability（可用性）
  3. Partition Tolerance（分區容忍）

只能滿足兩者：
  - CA（幾乎不可能存在）：不放棄 P
  - CP（一致+分區容忍）：網路分割時犧牲可用性
  - AP（可用+分區容忍）：網路分割時犧牲一致性

實際系統的選擇：
  - CP：ZooKeeper, etcd, HBase
  - AP：DynamoDB, Cassandra, CouchDB
```

---

## 🔥 Topic 6: GFS（Google File System）大規模分散式儲存

### GFS 的設計假設
```
Google 於2003年發表的分散式檔案系統：
  - 大量 commodity hardware（廉價硬體）
  - 檔案巨大（GB 等級）
  - 主要讀取模式：大型連續讀、隨機小讀
  - 需要高度容錯硬體故障
```

### GFS 架構
```
                     ┌─────────────┐
                     │   Master    │ ← 單一 Master（元資料管理）
                     └──────┬──────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
     ┌────────┴───┐ ┌────┴────┐ ┌───────┴───┐
     │ChunkServer │ │ChunkServer│ │ChunkServer│
     │   (1)      │ │   (2)     │ │   (3)     │
     └─────────────┘ └───────────┘ └───────────┘

特點：
  - 每個檔案切成固定大小 chunks（64MB）
  - 每個 chunk 在多個 chunkserver 上複製3份
  - Master 儲存所有元資料（檔案名稱、chunk 位置）
```

### GFS 的 Fault Tolerance
```
Chunk Server 故障：
  - Master 監測心跳中斷
  - 在其他 chunkserver 上重新複製 chunks
  - 維護設定的複製因子（replication factor）

Master 故障：
  - 單一 Master 是主要詬病（Single Point of Failure）
  - 後續 Colossus（Google 內部）改進了這一點
```

---

## 🔥 Topic 7: Spanner（全球分散式關聯式資料庫）

### Spanner 的特色
```
Google 的全球分散式關聯式資料庫：
  - 可擴展至數百台機器
  - 強一致性（跨資料中心、跨 Region）
  - 提供強一致性：外部一致性（External Consistency）
  - 使用 TrueTime API 實現跨地域時間同步
```

### TrueTime（硬體時間同步）
```
問題：分散式系統中不同機器的時鐘有誤差（Clock Skew）

TrueTime 的方案：
  - 使用 GPS 接收器 + 原子鐘
  - 每台伺服器有三個時鐘來源
  - 報告「不確定性範圍」而非精確時間

  API：
  ┌──────────────────────────────────┐
  │  TrueTime API                    │
  │  TT.now() → TTinterval           │
  │  { earliest: 10:00:00.000,       │
  │    latest:  10:00:00.200 }       │
  └──────────────────────────────────┘

每個寫入都附帶時間戳：TT.now().latest
讀取時等 TT.after(commit_ts) 確保時間已過
```

---

## 🔥 Topic 8: ZooKeeper（分散式協調服務）

### ZooKeeper 是什麼？
```
分散式系統的「幫手」：
  - 分散式鎖
  - 領導者選舉
  - 組態管理
  - 服務發現

使用場景：
  - Kafka 用於協調 broker 故障檢測
  - HBase 的領導者選舉
  - YARN 的資源管理
```

---

## 🔥 Topic 9: 分散式交易（2PC / PL / Saga）

### Two-Phase Commit（2PC）
```
Phase 1（Prepare）：
  Coordinator 問所有參與者：「可以提交嗎？」
  參與者回覆 Yes（並鎖住資源）或 No

Phase 2（Commit）：
  如果所有人都說 Yes：發送 Commit
  如果有人說 No：發送 Abort

問題：
  - Coordinator 故障會導致參與者無限期等待（blocking）
  - 不適合需要高可用的系統
```

---

## 🔥 Topic 10: 比特幣與拜占庭容錯（BFT）

### 拜占庭將軍問題
```
問題：一群將軍（其中可能有叛徒）如何達成一致？

實用拜占庭容錯（PBFT, Castro & Liskov, 1999）：
  - 容忍最多 f 個故障節點，需要至少 3f+1 個總節點
  - 適合聯盟鏈、許可制區塊鏈

比特幣的中本聰共識：
  - 用經濟激勵代替拜占庭假設
  - PoW（工作量證明）
  - 機率性地確認交易
```

---

## 🔥 Topic 11: Cache Consistency - Memcached at Facebook

### Facebook 的讀取架構
```
Web Server → Memcached（快取）→ MySQL（資料庫）

問題：如何保持快取和資料庫的一致性？

方案：
  - 寫入時：更新資料庫 + 使快取失效（而非更新快取）
  - 讀取時：快取命中直接返回，快取未命中從 DB 載入

跨 Region 複製：
  - Primary Region 接受寫入
  - 其他 Region 複製過來
  - 代價：寫入延遲高（跨 Region）
```

---

## 🔥 Topic 12: AWS Lambda 與 Serverless

### Lambda 的執行模型
```
傳統：伺服器需要預留、管理的 Serverful 模式
Lambda：事件驅動，無需管理伺服器

執行流程：
  1. 事件觸發（如 API Gateway 請求）
  2. 啟動容器/沙箱
  3. 下載函數程式碼
  4. 執行函數
  5. 返回結果，凍結容器（可能重用）

冷啟動延遲：數百毫秒到數秒
→ 不適合需要低延遲的即時應用
```

---

## 🔥 Topic 13: Ray（分散式強化學習框架）

### Ray 的設計
```
Ray：一個通用分散式執行引擎：
  - 支援強化學習（RLlib）
  - 支援類神經網路（Ray Serve）
  - 任務並行 + 物件存取

核心抽象：
  - ray.remote()：將任何函數變成可分散式執行
  - ray.get() / ray.put()：跨節點存取物件
```

---

## 🔥 Topic 14: Linearizability（線性一致性）

### 什麼是 Linearizability？
```
定義：一個歷史是線性的，如果：
  1. 每個操作在呼叫和回覆之間有某個單一時間點生效
  2. 這個時間點在所有節點看來一致

特性：
  - 可組合（Composable）：系統的每個部分都是線性的，總體也是
  - 與外部時鐘無關：只依賴操作間的順序

測試方法：
  - 使用 Model Checker（如 lin-kernel）
  - 记录所有客戶端操作時間，檢查是否可線性化
```

---

## 📋 2026 Spring 完整課程進度

### Lecture Schedule
```
Week 1-2: Introduction, RPC/Threads, MapReduce
Week 3-4: GFS, Paxos, Go patterns
Week 5-6: Raft (2 lectures + Q&A)
Week 7: Linearizability, ZooKeeper
Week 8: Distributed Transactions, Spanner
Week 9: Chain Replication, FaRM, Verification (IronFleet)
Week 10: Midterm Exam
Week 11-12: Spring Break → Memcached, Lambda
Week 13-14: Ray, Fork Consistency, Bitcoin
Week 15-16: BFT, Project Demos
Week 17: Final Exam
```

### 5個核心 Labs
```
Lab 1: MapReduce
  - 實作分散式 Word Count
  - 處理 worker 故障

Lab 2: Key/Value Server
  - 簡單的 KV 儲存服務

Lab 3: Raft（最核心！）
  - 3A: Leader Election
  - 3B: Log Replication
  - 3C: Persistence
  - 3D: Log Compaction

Lab 4: KV Raft
  - 用 Raft 實現 KV Store

Lab 5: Sharded KV
  - 多個 Raft Group 水平擴展
```

---

## 💡 工程師蘇茉的學習心得

### 為什麼選 MIT 6.5840？
```
作為軟體工程師，分散式系統是必備知識：
  - 所有大型網路服務（Netflix, Google, AWS）都是分散式系統
  - 面試必考：CAP Theorem、RAFT、共識演算法
  - 工作必用：Kafka、Redis Cluster、Kubernetes

MIT 6.5840 的特色：
  - 論文驅動學習（而非純理論）
  - 5個實作 Labs（用 Go 真的實現分散式系統）
  - 涵蓋現代分散式系統的所有核心概念
```

### 分散式系統 vs 單機系統的核心差異
```
單機系統：
  ✓ 記憶體共享，直接讀寫共享狀態
  ✓ 簡單的一致性模型（所有執行緒看到相同記憶體）
  ✓ 故障模式簡單（進程崩潰就直接重啟）

分散式系統：
  ✗ 網路延遲不為零
  ✗ 單一機器故障不影響整體
  ✗ 一致性模型需要考慮網路分割
```

### 面試高頻題目
```
1. CAP Theorem：解釋並舉例（CP vs AP 系統）
2. RAFT：
   - 三種角色及轉換
   - Leader Election 流程
   - Log Replication 流程
   - 如何處理網路分割
3. 一致性模型：強一致性、順序一致性、最終一致性
4. 分散式交易：2PC 的 prepare/commit 階段，缺點
5. Vector Clock：解決事件排序問題
```

### 實務應用場景
```
Kafka / RabbitMQ：
  - 基於 Topic 的訊息系統
  - Partition + Replication

Redis Cluster：
  - 分散式 Cache
  - Hash slot 分片

Kubernetes：
  - etcd（RAFT 共識）儲存叢集狀態
  - API Server 作為控制平面的單一入口

Cassandra：
  - AP 系統（可用性 + 分區容忍）
  - LSM Tree 儲存引擎
```

---

## 📅 學習Session記錄

### Session 7（2026-04-05）- MIT 6.5840 分散式系統深入

**今日重點：**
- 分散式系統的8大誤判（Fallacies）
- MapReduce 分散式計算框架
- CAP Theorem（一致性、可用性、分區容忍）
- RAFT 共識演算法（Leader Election + Log Replication）
- Go 語言併發模型（Goroutine + Channel）
- GFS 大規模分散式檔案系統
- Spanner 全球分散式關聯式資料庫
- TrueTime 硬體時間同步
- ZooKeeper 分散式協調服務
- 分散式交易（2PC）與 BFT
- Facebook Memcached 架構
- AWS Lambda / Serverless
- Ray 分散式執行引擎
- Linearizability 線性一致性

**新理解：**
- 分散式系統的本質：在「一致性」與「可用性」之間取捨
- RAFT 將 Paxos 複雜的共識問題拆解成三個可理解的部分
- MapReduce 的貢獻：讓不懂網路的工程師也能寫分散式程式
- TrueTime 是「承認時鐘不精確」的優雅工程解決方案

**與之前學習的銜接：**
- 演算法知識（如 BFS/DFS、Graph）用於分散式系統的拓撲管理
- 併發控制概念（鎖、訊息傳遞）是 RAFT 的基礎
- OS 的行程通訊（IPC）知識遷移到網路通訊

---

## 📅 後續學習計畫

```
Q2 2026:
  □ 完成 MIT 6.5840 Labs（至少完成 Lab 1-3）
  □ 閱讀經典論文（BigTable, Dynamo, Cassandra）
  □ 實作一個簡單的 Raft KV Store

Q3 2026:
  □ CMU 15-445 Database Systems（資料庫系統）
  □ 研究 etcd/Consul 原始碼
  □ 分散式系統面試題庫

Q4 2026:
  □ 雲端平台深入（GCP/AWS/Azure 分散式服務）
  □ 分散式系統面試衝刺
```

---

*本筆記由工程師蘇茉於 2026-04-05 整理自 MIT 6.5840 OCW 課程*
*學習次數：第7次（分散式系統專題）*
---

# CMU 15-445 / 645 - Database Systems（資料庫系統）
**學習日期：** 2026-04-05
**課程來源：** https://github.com/Developer-Y/cs-video-courses
**官方網站：** https://15445.courses.cs.cmu.edu/
**授課教授：** Andy Pavlo（CMU）
**參考教材：** Database System Concepts, 6th Edition（Silberschatz, Korth, Sudarshan）

---

## 課程概覽

CMU 15-445 是 CMU 最經典的資料庫系統課程，主軸為「如何設計與實作一個 DBMS」。

**核心 Topics（25堂Lecture）：**
- 關係模型與關係代數（Relational Model & Algebra）
- 儲存管理（Storage Management）
- 索引結構（Indexing）
- 查詢執行（Query Execution）
- 查詢優化（Query Optimization）
- 並行控制（Concurrency Control）
- 日誌與恢復（Logging & Recovery）
- 分散式資料庫（Distributed Databases）

**授課形式：**  Lecture + 5個 C++ 專案（使用 BusTub 教學 DBMS）
**先修知識：** C++、作業系統、資料結構

---

## Topic 1: 資料庫系統的動機（Why Database Systems?）

### 平面文件（CSV）的問題
```
問題 1：資料完整性（DATA INTEGRITY）
  - 如何確保 Artist 和 Album 表中的 artist_name 一致？
  - 如果有人修改了藝術家名字，專輯表如何同步？
  → 解決方案：外鍵（Foreign Key）約束

問題 2：實作困難（IMPLEMENTATION）
  - 如何高效找到特定記錄？（10億筆資料遍歷太慢）
  - 如何實現跨應用程式共享資料邏輯？
  - 兩個執行緒同時寫入同一檔案會怎樣？（資料覆蓋！）

問題 3：持久性（DURABILITY）
  - 程式崩潰時，正在更新的記錄狀態如何保證正確？
  - 如何實現多機複製以支援高可用性？
```

### DBMS 的定義
```
DBMS = Database Management System

A DBMS is software that allows applications to store and analyze 
information in a database without having to understand the underlying 
implementation details.

A general-purpose DBMS allows:
  - Definition（定義）
  - Creation（創建）
  - Querying（查詢）
  - Update（更新）
  - Administration（管理）
```

### 關係模型的誕生（Ted Codd, 1970）
```
早期問題：邏輯層與物理層緊密耦合
  - 應用程式必須知道資料如何物理儲存
  - 更換儲存結構需要重寫應用程式

Ted Codd 的突破：關係模型
  1. 將資料儲存為簡單的資料結構（表格）
  2. 透過高階語言（SQL）存取資料
  3. 物理儲存細節對應用程式透明

→ 實現了邏輯層與物理層的完全解耦！
```

---

## Topic 2: 關係模型（Relational Model）

### 資料模型三要素
```
1. Structure（結構）
   - 關係（Relation）= 表格
   - 元組（Tuple）= 表格的列（row）
   - 屬性（Attribute）= 表格的欄位（column）

2. Integrity（完整性約束）
   - 主鍵（Primary Key）：唯一標識元組
   - 外鍵（Foreign Key）：跨表引用
   - NOT NULL / UNIQUE 等約束

3. Manipulation（操作）
   - 關係代數（Relational Algebra）：過程式
   - SQL：宣告式
```

### 主鍵 vs 外鍵
```sql
-- 主鍵：唯一標識一條記錄
CREATE TABLE Artist (
    id INT PRIMARY KEY,        -- 自動生成唯一 ID
    name VARCHAR(100) NOT NULL
);

-- 外鍵：建立表之間的關聯
CREATE TABLE Album (
    album_id INT PRIMARY KEY,
    title VARCHAR(200),
    artist_id INT REFERENCES Artist(id)  -- 外鍵約束
);
```

### DML 的兩種方式
```
1. Procedural（過程式）：關係代數
   - 由資料庫管理系統決定「如何」執行查詢
   - 查詢指定高階策略

2. Non-Procedural（非過程式）：關係演算 / SQL
   - 只宣告「要什麼資料」
   - 不指定如何找到資料
   - SQL 就是宣告式語言的代表
```

---

## Topic 3: 關係代數（Relational Algebra）⭐⭐⭐

### 7種基礎運算子
```
1. SELECT (σ)：選擇滿足條件的元組
   σ_{predicate}(R) → 過濾行

2. PROJECT (π)：只保留指定屬性
   π_{attr1, attr2}(R) → 選擇列

3. UNION (∪)：合併兩個關係
   R ∪ S → 必須同類型

4. INTERSECTION (∩)：取交集
   R ∩ S → 兩個關係的共同元組

5. DIFFERENCE (−)：取差集
   R − S → 在R中但不在S中

6. PRODUCT (×)：笛卡爾積
   R × S → 所有可能的組合

7. JOIN (⋈)：自然連接
   R ⋈ S → 根據共同屬性合併
```

### 進階運算子
```
8. RENAME (ρ)：重新命名屬性或關係
9. DIVISION (÷)：複雜查詢
10. OUTER JOIN：保留空值側的元組
```

### SQL → 關係代數 轉換範例
```sql
SELECT artist_name, year
FROM Artist, Album
WHERE Artist.id = Album.artist_id
  AND artist_name = 'Coldplay'
  AND year > 2010;

-- 轉換為關係代數：
π_{artist_name, year}(
  σ_{artist_name='Coldplay' ∧ year>2010}(
    Artist ⋈ Album
  )
)
```

### 面試重點：Query Optimization 與關係代數
```
為什麼同樣結果不同執行順序效率差很多？

Q: 從 R 和 S 中找出 b_id = 102 的連接元組

方法 1：
  (R ⋈ S) → σ_{b_id=102}()  → 先連接再過濾
  代價：兩個表的笛卡爾積可能超級大！

方法 2：
  σ_{b_id=102}(S) → (R ⋈ filtered_S)  → 先過濾再連接
  代價：過濾後的 S 很小，連接很快！

→ 這就是 Query Optimizer 的核心工作！
```

---

## Topic 4: 資料庫儲存（Database Storage）

### 儲存層級架構
```
┌─────────────────────────────────────────────┐
│              Application Layer              │
├─────────────────────────────────────────────┤
│           DBMS (Software)                   │
│  ┌─────────────────────────────────────┐   │
│  │         Query Execution Engine       │   │
│  ├─────────────────────────────────────┤   │
│  │         Buffer Pool Manager          │   │
│  ├─────────────────────────────────────┤   │
│  │         Storage Manager              │   │
│  │    (File, Page, Buffer Management)   │   │
│  └─────────────────────────────────────┘   │
├─────────────────────────────────────────────┤
│           Disk (NVMe SSD / HDD)             │
└─────────────────────────────────────────────┘
```

### 硬碟特性（Disk-Oriented DBMS）
```
磁碟 vs 記憶體：
  記憶體：位元組可定址，O(1) 隨機存取，斷電後資料丢失
  磁碟：區塊（頁）可定址，順序讀取 >> 隨機讀取，斷電後仍保留

磁碟 I/O 的代價：
  - 一次隨機讀取：~100,000 cycles（CPU閒置）
  - 一次順序讀取：~1,000 cycles（可接受）
  → 設計原則：盡量順序讀取，最小化隨機 I/O！
```

### 頁（Page）的概念
```
硬體頁：4KB（保證原子寫入）
OS 頁：4KB
資料庫頁：通常 4-16KB

三種頁：
  1. 硬體頁（Hardware Page）
  2. OS 頁（OS Page）
  3. 資料庫頁（Database Page）← DBMS 自己定義
```

### 頁內資料組織：Slotted-Page vs Log-Structured

**Slotted-Page（大多數 DBMS 使用）：**
```
┌──────┬──────────────────────────────────────┐
│Header│         Data Area                     │
│      │  ← 元組從後往前增長                   │
│Slots │  ← Slot 陣列從前往後增長              │
└──────┴──────────────────────────────────────┘
  slot[0] → tuple_2
  slot[1] → tuple_1
  slot[2] → tuple_3

優點：支援任意大小元組
缺點：刪除後有內碎片、寫放大（Write Amplification）
```

**Log-Structured：**
```
只寫入操作日誌（PUT, DELETE），不更新現有頁
讀取時：從新到舊掃描日誌，重建元組

優點：寫入極快（順序寫入）、無碎片
缺點：讀取慢（需重建）、內存膨脹
```

### Buffer Pool（緩衝池）
```
為什麼需要 Buffer Pool？
  - 磁碟讀取太慢，必須將常用頁緩衝在記憶體中
  - 程式需要「以為自己在操作記憶體」

Buffer Pool Manager 的職責：
  1. 追蹤哪些頁目前在記憶體中
  2. 維護頁的引用計數（pin count）
  3. 淘汰不常用的頁（頁框替換策略）

頁框替換策略：
  - LRU（Least Recently Used）：最久未使用
  - Clock（近似 LRU，更高效）
  - LRU-K：考慮最近 K 次訪問時間
  - MRU（Most Recently Used）：某些場景更優

問題：Buffer Pool 能否使用 OS 的 mmap()？
  - 不建議！作業系統何時刷盤難以控制
  - 可用：madvise(), mlock(), msync() 輔助控制
```

---

## Topic 5: 索引結構（Indexing）⭐⭐⭐

### 兩種主要索引
```
1. Hash Table（雜湊表）
   - 等值查詢：O(1)
   - 範圍查詢：O(n)（不支援）

2. B+ Tree（對數時間讀取）
   - 等值查詢：O(log n)
   - 範圍查詢：O(log n + k)（支援！）
   - 大多數 DBMS 的預設索引結構
```

### B+ Tree vs B Tree
```
B Tree：每個節點都可能包含資料（keys + data）
B+ Tree：只有葉節點包含資料，內部節點只含 keys

B+ Tree 優點（對資料庫更優）：
  ✓ 內部節點更小，可容納更多分支（更淺）
  ✓ 所有葉節點在同一層，範圍查詢穩定
  ✓ 葉節點互相連接，適合順序掃描
  ✓ 葉節點包含所有 keys，覆蓋索引查詢更高效
```

### B+ Tree 搜尋複雜度
```
高度為 h 的 B+ Tree：
  - 搜尋：O(log_f N) 其中 f = 分支因子（fanout）
  - 典型 fanout：100-500
  - 100 萬筆資料：約 3-4 層
  - 10 億筆資料：約 4-5 層

→ 樹高 4-5 層 = 最多 4-5 次磁碟 I/O（可接受！）
```

### 索引並發控制
```
問題：多執行緒同時讀寫索引，會怎樣？

方案 1：Latch Crabbing / Coupling
  - 從根往下走，持有父節點的鎖，確認子節點安全後釋放父鎖
  - 讀取：只加讀鎖（S Lock）
  - 寫入：加寫鎖（X Lock）

方案 2：Latch-Free（樂觀並發）
  - 使用版本號，讀取不阻塞
  - 寫入衝突時重試
```

---

## Topic 6: 查詢執行（Query Execution）⭐⭐⭐

### 三種處理模型

**1. Iterator Model（Volcano Model，火山模型）：**
```python
# 每個 Operator 實現 open(), next(), close()
class ScanOperator:
    def open(self):
        self.cursor = self.table.first()
    
    def next(self):
        if self.cursor is None:
            return None  # End of data
        row = self.cursor
        self.cursor = self.table.next(self.cursor)
        return row
    
    def close(self):
        pass

# 缺點：函數呼叫開銷大、cache 效率低
# 優點：簡單、支援 pipeline
```

**2. Materialization Model（物化模型）：**
```python
# 每個 Operator 一次處理完所有資料
def sort_operator(input_relation):
    data = input_relation.fetch_all()
    return sorted(data)
# 缺點：記憶體佔用大
# 優點：減少函數呼叫開銷
```

**3. Vectorized / Batch Model（向量化模型）：**
```python
# 每次 next() 返回一批元組（如 1000 筆）
def scan_next(self):
    return self.table.fetch_batch(1000)  # 一次取 1000 筆
# 優點：可使用 SIMD 加速、cache 效率高
# 目前主流（ClickHouse、Vectorized DB 都用這個）
```

### 連接演算法（Join Algorithms）⭐⭐⭐

**1. Nested Loop Join（嵌套迴圈連接）：**
```python
# 暴力法：O(n × m)
for row_r in R:
    for row_s in S:
        if row_r.join_key == row_s.join_key:
            yield combine(row_r, row_s)

# 優化：Block Nested Loop Join
# 將 R 分塊載入記憶體
for block_r in R.chunks(BUFFER_SIZE):
    for row_s in S:
        for row_r in block_r:
            if row_r.key == row_s.key:
                yield ...
# 代價：O(n × m)，大表放內層
```

**2. Sort-Merge Join：**
```python
# 步驟 1：兩個表各自排序
sorted_r = R.sort()
sorted_s = S.sort()

# 步驟 2：雙指標掃描合併
i = j = 0
while i < len(sorted_r) and j < len(sorted_s):
    if sorted_r[i].key < sorted_s[j].key:
        i += 1
    elif sorted_r[i].key > sorted_s[j].key:
        j += 1
    else:
        # 相等：輸出所有匹配
        while i < len(sorted_r) and sorted_r[i].key == sorted_s[j].key:
            while j < len(sorted_s) and sorted_s[j].key == sorted_r[i].key:
                yield combine(sorted_r[i], sorted_s[j])
                j += 1
            i += 1
# 代價：O(n log n + m log m + n + m)
# 適合已排序的資料或需要排序輸出的場景
```

**3. Hash Join（最重要！）：**
```python
# 階段 1：建構雜湊表（Build Phase）
hash_table = {}
for row_r in R:
    hash_table[row_r.key].append(row_r)

# 階段 2：探測（Probe Phase）
for row_s in S:
    for row_r in hash_table.get(row_s.key, []):
        yield combine(row_r, row_s)

# 代價：O(n + m)
# 限制：需要足夠記憶體容納 R（可用 GRACE Hash Join 處理大表）
```

### GRACE Hash Join（磁碟版 Hash Join）
```
問題：Hash Table 無法一次放進記憶體？
解決：GRACE Hash Join（分區雜湊連接）

步驟：
  1. Partition Phase：根據 key hash 將 R 和 S 分區
     - 每個分區寫入獨立檔案
     - 確保相同 key 的元組在同一分區

  2. Build + Probe Phase：
     - 逐一載入 R 的分區，建構 Hash Table
     - 探測 S 的對應分區

代價：2 × (read_R + write_R + read_R + read_S)
磁碟 I/O 仍是主要瓶頸
```

---

## Topic 7: 查詢優化（Query Optimization）

### 為什麼需要 Query Optimizer？
```
SQL 是宣告式語言，只聲明「要什麼」，不說「怎麼找」

同一個 SQL 可能有多種執行方式：
  - 不同的連接順序（R ⋈ S vs S ⋈ R）
  - 不同的連接演算法（Hash vs Sort-Merge vs NL）
  - 不同的存取路徑（全表掃描 vs 索引掃描）

Query Optimizer 的任務：
  → 選擇成本最低的執行計劃
```

### 兩種優化策略
```
1. 基於靜態規則（Rule-Based）
   - 已知哪些策略「通常」更好
   - 快速但無法適應資料分佈

2. 基於成本估算（Cost-Based）
   - 評估每個候選計劃的成本
   - 考慮資料分佈（使用直方圖、採樣）
   - 更精確但計算開銷大
```

### 邏輯 vs 物理執行計劃
```
邏輯計劃（Logical Plan）：
  - SELECT → PROJECT → JOIN → ...
  - 與實際執行無關

物理計劃（Physical Plan）：
  - Hash Join vs NL Join
  - Sequential Scan vs Index Scan
  - 確定「如何」執行
```

### Cost 估算
```python
# 簡化成本模型：
cost = I/O_cost + CPU_cost

I/O_cost = pages_read + pages_written
          = (#tuples / tuples_per_page) × access_pattern_factor

# 成本估算依賴：
# 1. 直方圖（Histogram）：資料分佈統計
# 2. 採樣（Sampling）：估計查詢結果大小
# 3. 頁面統計：每頁平均元組數
```

---

## Topic 8: 並發控制理論（Concurrency Control）⭐⭐⭐

### 交易的四大特性（ACID）

```
A（Atomicity，原子性）：
  - 交易中的所有操作要么全部完成，要么全部不完成
  - 實現方式：Write-Ahead Log（WAL）

C（Consistency，一致性）：
  - 資料必須滿足所有完整性約束
  - 交易開始前和結束後，資料庫都必須是一致的

I（Isolation，隔離性）：
  - 每個交易仿佛在單獨執行
  - 並發執行的結果 == 某種順序執行的結果
  - 實現方式：並發控制機制

D（Durability，持久性）：
  - 已提交的交易影響必須持久保存
  - 實現方式：REDO Log + 磁碟同步
```

### 並發問題

```
1.  Dirty Read（髒讀）：
    - 讀取到另一交易未提交的資料

2.  Non-Repeatable Read（不可重複讀）：
    - 同一交易兩次讀取同一資料，結果不同

3.  Phantom Read（幻讀）：
    - 同一交易兩次查詢，返回了原本不存在的記錄
    - （因為另一交易插入了新資料）

4.  Lost Update（丟失更新）：
    - 兩個交易讀取並更新同一筆資料
    - 後者的更新覆蓋了前者的更新

5.  Write Skew（寫偏斜）：
    - 兩個交易各自讀取一些資料，然後各自更新不同的資料
    - 但更新的依據包含了對方的讀取結果
    - 會導致違反一致性約束
```

### 隔離層級（Isolation Levels）
```
┌────────────────┬─────────┬────────────────┬─────────┐
│ Isolation Level │ Dirty   │ Non-Repeatable │ Phantom │
│                 │ Read    │ Read          │ Read    │
├────────────────┼─────────┼────────────────┼─────────┤
│ READ UNCOMMITED│  可能   │     可能        │  可能   │
│ READ COMMITTED  │  不可能 │     可能        │  可能   │
│ REPEATABLE READ │  不可能 │     不可能      │  可能   │
│ SERIALIZABLE   │  不可能 │     不可能      │  不可能 │
└────────────────┴─────────┴────────────────┴─────────┘

SQL Server：預設 READ COMMITTED
MySQL InnoDB：預設 REPEATABLE READ
PostgreSQL：預設 READ COMMITTED（但使用 MVCC）
```

---

## Topic 9: Two-Phase Locking（兩階段鎖）⭐⭐⭐

### 鎖的類型
```
S Lock（Shared Lock，共享鎖）：
  - 多個交易可以同時持有
  - 讀取操作使用 S Lock

X Lock（Exclusive Lock，排他鎖）：
  - 只有一個交易可以持有
  - 寫入操作使用 X Lock
```

### 兩階段鎖（2PL）的規則
```
第一階段（Growing Phase）：
  - 只獲取鎖，不釋放鎖
  - 交易持續擴張

第二階段（Shrinking Phase）：
  - 只釋放鎖，不獲取新鎖
  - 交易持續收縮

交易在 commit 或 abort 後才釋放鎖（嚴格 2PL）
```

### 嚴格 2PL 的問題
```
問題 1：Cascading Aborts（級聯回滾）
  - T1 回滾後，T2 可能已讀取 T1 的未提交資料
  - T2 也必須回滾

問題 2：死結（Deadlock）
  - T1 持有 A 等 B，T2 持有 B 等 A
  - 兩者永遠等待

解決方案：死結檢測或死結避免
```

### 意向鎖（Intention Locks）
```
目的：支援多粒度鎖定（表鎖 + 行鎖）

IS（Intention Shared）：準備獲取子節點的 S Lock
IX（Intention Exclusive）：準備獲取子節點的 X Lock
SIX（Shared + Intention Exclusive）：讀取整個表 + 更新某些行

相容性矩陣：
         IS    IX    S    SIX    X
IS       ✓     ✓    ✓     ✓     ✗
IX       ✓     ✓    ✗     ✗     ✗
S        ✓     ✗    ✓     ✗     ✗
SIX      ✓     ✗    ✗     ✗     ✗
X        ✗     ✗    ✗     ✗     ✗
```

---

## Topic 10: Timestamp Ordering（時間戳排序）

### 基本 T/O 演算法
```
每個交易分配唯一遞增的時間戳

讀取規則：
  - 如果 W_TS(x) > T：拒絕讀取（資料已被未來交易修改）
  - 否則：允許讀取，更新 R_TS(x) = max(R_TS(x), T)

寫入規則：
  - 如果 R_TS(x) > T 或 W_TS(x) > T：拒絕寫入
  - 否則：允許寫入，更新 W_TS(x) = T

Thomas Write Rule：
  - 如果 W_TS(x) > T：忽略此寫入（已被覆蓋）
```

### 樂觀並發控制（OCC）
```
適用場景：衝突少的交易

階段 1：讀取（Read Phase）
  - 複製所有讀取的資料到本地

階段 2：驗證（Validation Phase）
  - 檢查其他交易的寫入是否衝突

階段 3：寫入（Write Phase）
  - 如果驗證通過，寫入資料
```

---

## Topic 11: MVCC（多版本併發控制）⭐⭐⭐

### MVCC 的核心思想
```
每個元組保存多個版本：
  - 每個版本包含：資料內容 + 建立版本的事務時間戳

讀取時：
  - 根據事務的時間戳，選擇可見的最新版本
  - 讀取不需要加鎖！

寫入時：
  - 建立新版本，標記刪除標記
  - 不覆蓋原有版本

優點：
  ✓ 讀不阻塞寫，寫不阻塞讀
  ✓ 支援 Snapshot Isolation
  ✓ 實現 Time-Travel 查詢
```

### MVCC 實現的關鍵設計
```
1. 版本儲存：
   - Append-Only（追加儲存）：新版本存在同一表空間
   - Time-Travel（時光表）：歷史版本存在獨立表空間
   - Delta（增量儲存）：只儲存修改的欄位

2. 垃圾回收：
   - 刪除不再需要的舊版本
   - 依據：所有活躍事務的最舊時間戳

3. 讀取視圖：
   - 所有活躍事務清單
   - 事務的開始時間戳
```

### Snapshot Isolation（快照隔離）
```
Oracle、PostgreSQL、SQL Server 都使用

事務開始時：
  - 讀取資料庫的「快照」（所有已提交的版本）

寫入時：
  - 檢查是否有其他事務已提交了衝突的寫入
  - 如果有，abort 當前事務

問題：Write Skew 無法防止
  - 只能通過 SERIALIZABLE 等級防止
```

---

## Topic 12: 日誌與恢復（Logging & Recovery）⭐⭐⭐

### Write-Ahead Log（WAL）原則
```
核心原則：
  1. 日誌必須在資料頁寫入磁碟前寫入磁碟
  2. 只有当日誌已刷盤，交易才能提交

日誌內容：
  - Transaction ID
  - Page ID
  - Offset
  - Old Value（Before Image）
  - New Value（After Image）
```

### 日誌類型
```
1. STEAL + NO-FORCE（大多數 DBMS 使用）：
   - 允許贓頁（Steal）寫入磁碟
   - 提交時不強制刷盤（No-Force）
   - 需要 WAL + Checkpoint

2. NO-STEAL + FORCE：
   - 不允許未提交頁寫入磁碟
   - 提交時所有更改已刷盤
   - 恢復簡單但效能差

3. STEAL + FORCE：
   - 效能最差，幾乎不使用
```

### Checkpoint（檢查點）
```
問題：系統崩潰後，重做所有日誌太慢！

解決方案：Checkpoint
  - 定期將 Buffer Pool 中所有已刷盤的頁寫入
  - 記錄此刻所有活躍的交易
  - 恢復時只從最近 Checkpoint 開始

代價：
  - Checkpoint 期間效能下降
  - 需要阻斷或延遲事務
```

### ARIES 恢復演算法
```
IBM 的經典恢復演算法（三階段）：

階段 1：Analysis（分析）
  - 找出崩潰時的 dirty pages 和活躍交易

階段 2：Redo（重做）
  - 從最後一個 Checkpoint 開始重做所有操作
  - 確保所有已寫入日誌的操作都生效

階段 3：Undo（回滾）
  - 回滾所有未提交交易的更改
  - 使用事務日誌的 Compensation Log Records
```

---

## Topic 13: 分散式資料庫（Distributed Databases）

### 分散式 vs 集中式
```
集中式 DBMS：
  - 所有資料在一台機器
  - 所有交易由一個 DBMS 實例處理

分散式 DBMS：
  - 資料分片（Partition/Shard）到多台機器
  - 每台機器有獨立的 DBMS 實例
  - 應用程式視為單一邏輯資料庫
```

### 分散式架構
```
OLTP（線上交易處理）：
  - 高並發、短交易
  - 範例：銀行轉帳、庫存管理
  - 典型系統：Google Spanner、TiDB、CockroachDB

OLAP（線上分析處理）：
  - 低並發、長查詢
  - 範例：資料倉儲、商業智慧
  - 典型系統：ClickHouse、Snowflake、Redshift

HTAP（混合交易分析處理）：
  - 同一系統同時支援 OLTP + OLAP
  - 範例：TiDB、Azure Synapse
```

### 分散式並發控制
```
分散式 2PC（兩階段提交）：
  Coordinator                    Participants
      │                               │
      │── PREPARE ──────────────────→│
      │←── YES/NO ───────────────────│
      │                               │
      ├─ COMMIT ─────────────────────→│
      │←── ACK ──────────────────────│

問題：
  - Coordinator 故障會導致Participants 無限等待（Blocking）
  - 需要日誌持久化來解決
```

### CAP Theorem 再次驗證
```
分散式資料庫系統：
  - C（一致性）：所有節點看到相同的資料
  - A（可用性）：每個請求都得到回覆
  - P（分割容忍）：網路分割時系統仍運行

→ 三者只能滿足兩個

實際取捨：
  - CP（犧牲 A）：ZooKeeper、HBase、BigTable
  - AP（犧牲 C）：DynamoDB、Cassandra
```

---

## Topic 14: 工廠視角 — 從演算法到實際系統

### 關係代數 → Query Execution → 分散式系統
```
之前學習的知識如何串聯：

MIT 6.006（演算法）：
  BFS/DFS → 圖遍歷 → Query Execution 的資料流
  Heap → Buffer Pool 頁替換策略
  Hash Table → 索引結構、Hash Join

MIT 6.1810（OS）：
  頁表 → Buffer Pool 管理
  鎖機制 → 並發控制的基礎
  檔案系統 → 資料庫檔案組織

MIT 6.5840（分散式）：
  Raft → 分散式資料庫的共識機制
  CAP Theorem → 分散式 DBMS 的取捨
  複製 → 資料庫 HA 架構

CMU 15-445（本課）：
  關係代數 → SQL 執行引擎
  B+ Tree → 索引結構
  2PL / MVCC → 交易並發控制
  WAL + ARIES → 故障恢復
```

---

## 💡 工程師蘇茉的 CMU 15-445 學習心得

### 為什麼選資料庫系統？
```
我的 CS 學習路徑：
  Session 3: MIT 6.006 演算法基礎
  Session 4: MIT 6.046 進階演算法設計
  Session 5: MIT 6.5840 分散式系統
  Session 6: MIT 6.1810 作業系統
  Session 7-8: MIT 6.5840 分散式深入

為什麼需要資料庫知識？
  1. 後端工程師每天都和 DBMS 打交道
  2. 面試高頻：索引原理、並發控制、事務隔離
  3. 分散式資料庫（TiDB, CockroachDB）需要兩者兼備
  4. 理解 Query Optimization 才能寫出高效 SQL
```

### 面試高頻題目
```
1. B+ Tree vs Hash Index：何時用哪個？
   → 答案：等值查詢用 Hash，範圍查詢用 B+ Tree

2. 事務隔離級別：髒讀、不可重複讀、幻讀的差異？
   → 答案：取決於鎖的使用方式

3. 兩階段鎖（2PL）的原則？
   → 答案：Growing Phase 只加鎖，Shrinking Phase 只釋放鎖

4. MVCC 的優點？
   → 答案：讀不阻塞寫，寫不阻塞讀

5. MySQL InnoDB 的預設隔離級別？
   → 答案：REPEATABLE READ

6. WAL 的原則？
   → 答案：日誌必須在資料頁寫入磁碟前寫入磁碟

7. Hash Join vs Sort-Merge Join vs NL Join？
   → 答案：Hash Join 最快（需記憶體），Sort-Merge 適合已排序
```

### 實務應用場景
```
SQL 優化：
  - 為經常查詢的欄位建索引
  - 避免 SELECT *，只查需要的欄位
  - 使用 EXPLAIN 分析執行計劃

事務設計：
  - 短事務比長事務更好（減少鎖競爭）
  - 避免大事務拆分成小批次
  - 讀多寫少場景用 REPEATABLE READ

OLTP vs OLAP：
  - 高頻交易：用 OLTP 資料庫（MySQL、TiDB）
  - 分析報表：用 OLAP 資料庫（ClickHouse、Snowflake）
  - 避免在 OLTP 資料庫上跑複雜分析
```

### CMU 15-445 Labs（C++ 實作）
```
Lab 1: C++ Primer（熱身）
Lab 2: Buffer Pool Manager（儲存管理）
Lab 3: B+ Tree Index（索引實作）
Lab 4: Query Execution（查詢執行）
Lab 5: Concurrency Control（並發控制）

→ 用 BusTub 教學 DBMS，程式碼可在 GitHub 找到
```

---

## 📊 完整課程大綱

### 25堂 Lecture 一覽
```
Week 1:  關係模型、Advanced SQL
Week 2:  儲存 I / II（頁結構、磁碟管理）
Week 3:  儲存模型、壓縮、Buffer Pool
Week 4:  Hash Table、Index I / II（B+ Tree）
Week 5:  索引並發控制、排序與聚合
Week 6:  Join 演算法、Query Execution I / II
Week 7:  期中考、Query Planning & Optimization
Week 8:  並發控制理論、2PL
Week 9:  Timestamp Ordering、MVCC
Week 10: 資料庫日誌、恢復
Week 11: 分散式資料庫、OLTP / OLAP
Week 12: Final Review
```

---

## 📅 後續學習計畫

```
Q2 2026:
  □ 完成 CMU 15-445 Labs（Buffer Pool、B+ Tree、Concurrency Control）
  □ 實作一個簡單的 SQLite Clone（基於本課概念）
  □ 閱讀經典論文（ARIES、MVCC、BigTable）

Q3 2026:
  □ MIT 6.854（Advanced Algorithms）— 演算法最終章
  □ CMU 15-721（Advanced DBMS）— 純研究導向
  □ Rust 實作一個 Columnar DB

Q4 2026:
  □ 分散式 SQL 引擎設計
  □ 雲端資料庫深入（GCP Spanner / AWS
---

## ?? Session 8 銝駁?嚗??湔抒?隢ooKeeper?????鈭斗???隤踵???
---

## ? Topic 1: Linearizability嚗??找??湔改????撘頂蝯梁??詨?銝?湔扳?皞?
### 隞暻潭 Linearizability嚗?
**摰儔嚗迤?ｇ?嚗?* 銝?風?脫蝺抒?嚗?????雿??澆??閬????其??銝??摮???嚗閰脫???????銝????????暺?靘??氬?
**摰儔嚗?雿改?嚗?* 霈??摰?餈??餈?甈∪神?亦?蝯???餈?單???摰儔??
### Linearizability vs ?嗡?銝?湔扳芋??
```
?撘????撘梁?銝?湔批惜蝝?

1. Strict Serializability嚗?潛??改?
   - 霈撖急??典???
   - 蝑??澆????
2. Linearizability嚗??找??湔改?潃??祉???嚗?   - 霈????餈神??   - ?舐???composable嚗?
3. Sequential Consistency嚗?摨??湔改?
   - ??銵???詨?????
   - 雿?摨??閬???????
4. Causal Consistency嚗????湔改?
   - ?芯?霅???????雿?摨?   - 靘?蝷曄黎鞎潭???

5. Eventual Consistency嚗?蝯??湔改?
   - ?蝯?摰??雿遙???餃?賭?銝??   - 靘?DynamoDB, Cassandra
```

### Linearizability ??閬?
```
?箔?暻?Linearizability ?臬????蝟餌絞????皞?

1. ?舐??改?Composability嚗?
   憒?蝟餌絞瘥??舐??抒?嚗?頂蝯曹??舐??抒?
   ??璅∠??頂蝯梯身閮??箇?

2. 摰寞??函?嚗?   蝔?閮剛?撣怠隞亙????格?蝟餌絞銝璅??閫?????蝟餌絞
   ??撠勗????雿?典銝???祇?摰?

3. ?甇?Ⅱ?扳?隞塚?
   ?舀葫閰血????蝟餌絞甇?Ⅱ?抒?璅?
   ???舐 model checker嚗? lin-kernel嚗?霅?```

### Linearizability vs Sequential Consistency

```
撌桃嚗?  - Sequential Consistency嚗閬???銵???詨???
  - Linearizability嚗?additionally 閬???摨??單???銝??
靘?嚗?  Thread A: write(x=1)
  Thread B: read(x)  // 餈? 1

  ??Sequential Consistency 銝???嚗閬??銵??? order嚗?  ??Linearizability 銝???嚗???read ??write 摰?敺銵?

  雿??嚗?  Thread A: write(x=1)
  Thread B: read(x)   // 餈? 0嚗???read ??write 摰???憪?

  ??Linearizability 銝???嚗ead ???????潘?
  ??Sequential Consistency 銝??航??嚗?瘙箸?典?憒?摰儔嚗?```

---

## ? Topic 2: ZooKeeper嚗????蝟餌絞???桐葉敹?

### ZooKeeper ?臭?暻潘?

```
ZooKeeper = ?撘頂蝯梁???矽??

???敹鞊∴?
  1. ?撘?嚗istributed Lock嚗?  2. ?????Leader Election嚗?  3. 蝯?蝞∠?嚗onfiguration Management嚗?  4. ???潛嚗ervice Discovery嚗?  5. ?郊撅?嚗arrier嚗?
銝??ZooKeeper ?ａ?嚗nsemble嚗虜 3 ??5 ??暺??? Zab ?降嚗?隡?Raft嚗?霅??湔扼?```

### ZooKeeper ???芋??
```
ZooKeeper 撠???蝜?nodes??撅斗活蝯?嚗?隡潭?獢頂蝯梧?嚗?
/
??? /config              // 蝯?蝞∠?
??? /workers            // 撌乩???????  ??? /workers/worker-1
??  ??? /workers/worker-2
??? /tasks              // 隞餃?雿?
??  ??? /tasks/task-1
??  ??? /tasks/task-2
??? /leader             // ????閮?
瘥?znode ?臭誑?脣?撠?鞈?嚗?1MB嚗? 摮?暺?銵?```

### ZooKeeper ??Watch 璈

```go
// ?? znode 霈??敹芋撘?
// Client 閮 watch ??znode 霈? ??ZooKeeper ? Client

// ?賭誨蝣潘?
zk.get("/config", watch=true)  // 閮餃? watch

// ??/config ?潛?霈?嚗ooKeeper ?潮?隞嗥策 client
onWatchEvent(event):
    newConfig = zk.get("/config", watch=true)  // ?閮餃? watch
    applyConfig(newConfig)
```

### ZooKeeper ?祕???典??
```
Kafka嚗?  - broker 閮餃???ZooKeeper
  - broker ?? ??ZooKeeper ? controller ??? partition leader

HBase嚗?  - 雿輻 ZooKeeper ?貉? active master
  - 蝣箔??芣?銝??master ??????雿?
YARN嚗?  - ResourceManager 雿輻 ZooKeeper ?脰? leader election
  - ?遢 RM ?? active RM ??

Google Chubby嚗ooKeeper ??頨恬?嚗?  - BigTable 雿輻 Chubby ?貉? primary tablet server
```

### ZooKeeper vs etcd vs Consul嚗?憭批?隤踵???頛?

```
ZooKeeper嚗?  - 隤?嚗ava嚗???curator client library for ?嗡?隤?嚗?  - 隞嚗?獢頂蝯梢◢??API
  - ?拙?嚗扔擃??湔折?瘙??帘摰?
etcd嚗?  - 隤?嚗o
  - 隞嚗EST + gRPC + 摰Ｘ蝡?library
  - ?拙?嚗ubernetes ??蝟鳴??身?矽??嚗?  - ?梯?嚗aft

Consul嚗?  - 隤?嚗o
  - 隞嚗NS + HTTP API
  - ?寡嚗撱?service discovery + health checking
  - ?拙?嚗凝???嗆?
```

---

## ? Topic 3: Distributed Transactions嚗????鈭斗?嚗?2PC ??Saga

### ?箔?暻澆????鈭斗?敺???

```
?格?鞈?摨怎?鈭斗?嚗CID嚗隞乩?鞈湛?
  - ??Locks嚗??銝衣??
  - Write-Ahead Log嚗AL嚗????Ｗ儔
  - ?曹澈閮擃????雿???唳???
?撘漱???嚗?  - 憭璈??嚗??圈?航??
  - 蝬脰楝??航撠?典?蝭暺瘜?
  - 瘝??曹澈閮擃??矽?游??```

### Two-Phase Commit嚗?PC嚗??蝬?????鈭斗??降

```
Phase 1嚗repare嚗???畾蛛?
  Coordinator ?潮?Prepare ?唳?????  ???銵漱??雿? Commit嚗?    - ???賊?鞈?
    - 撖?Prepare Log
    - ?? YES ??NO

Phase 2嚗ommit ??Abort嚗捱摰?畾蛛?
  憒???犖?賢?閬?YES嚗?    ??Coordinator ?潮?Commit ?唳?????    ??????迤撘?Commit
    ?????
  憒??遙雿犖霂?NO嚗?頞?嚗?
    ??Coordinator ?潮?Abort ?唳?????    ???????Rollback
    ?????```

```go
// 2PC ??Coordinator ?賭誨蝣?func two_phase_commit(coordinator, participants, transaction):
    // Phase 1: Prepare
    votes = []
    for p in participants:
        response = p.prepare()
        votes.append(response)

    // Phase 2: Decision
    if all(votes, v => v == YES):
        for p in participants:
            p.commit()
    else:
        for p in participants:
            p.abort()
```

### 2PC ??憿?Blocking嚗憛?

```
2PC ??賜撩?瘀?

1. Coordinator ??嚗?   ????嗅 Commit/Abort ???潦?蝣箏????   - 鞈?鋡恍?雿??⊥????嗡?鈭斗?
   - ?芾蝑? Coordinator ?Ｗ儔嚗?蝑?銋?
   ????憛?blocking嚗?
2. 蝬脰楝?嚗?   憒?蝬脰楝?撠?典????蝜思?銝?
   - ??拙?航?銝?瘙箏?
   ????銝?湔?
3. ???嚗?   - ?????閬?閬??賢?瘙箏?
   - 隞颱????嚗?漱?停??```

### Saga Pattern ???拍?潮??鈭斗??隞?獢?
```
Saga ?敹嚗?  銝蝙??ACID ??改?Isolation嚗?  ?撠之鈭????箏???啣?鈭?
  瘥?鈭??撌梁????漱??Compensating Transaction嚗?
?拍?湔嚗?  - 頝冽????瑟??平??蝔?  - 銝?瑟???雿?皞?鈭斗?

靘?????蝟餌絞
  1. ??璈巨嚗aga step 1嚗?  2. ????嚗aga step 2嚗?  3. ??蝘?嚗aga step 3嚗?
  憒?甇仿? 3 憭望?嚗?  ??鋆?鈭斗?嚗?瘨?摨?閮?  ??鋆?鈭斗?嚗?瘨?蟡券?閮?
?拍車?矽?孵?嚗?  1. Choreography嚗?頩?嚗?
     瘥??摰?敺銝?????     ?拙?蝪∪?湔

  2. Orchestration嚗楊?脣?嚗?
     銝剖亢?矽?恣???蝔?     ?拙?銴??湔嚗??2PC嚗?```

---

## ? Topic 4: Chain Replication嚗?撘?鋆踝????虫?蝔桐??湔扳獢?
### Chain Replication ?敹

```
Chain Replication ?臬銝蝔桀祕?曉撥銝?湔抒?銴ˊ?降嚗?
閮剛???嚗?  1. 撖怨?瘙窒?????  2. 霈隢??臭誑?其遙??暺????拍?瑁?嚗?  3. 蝭暺????芷?撅?其耨敺?
?蝯?嚗?  Head ??Node1 ??Node2 ??... ??Tail
     (撖怠)              (霈??

撖怠瘚?嚗?  1. Client ?潮?Write ??Head
  2. Head ??銝血蝯?Node1
  3. Node1 ??銝血蝯?Node2
  ...
  4. Tail ??銝血?閬?Acknowledgement
  5. Tail ?? Client嚗神?交???
霈??蝔?
  1. Client ?潮?Read ??Tail嚗?隞颱?蝭暺?
  2. Tail ?湔餈??砍鞈?嚗?霅??堆?
  嚗???Tail ?舫??怎垢嚗?摰??摰???
```

### Chain Replication vs Raft

```
Chain Replication嚗?  ??霈???賢末嚗ail ?臭誑???????
  ??蝪∪嚗神?交?桀?瘚偌蝺?  ??????撅?典?

Raft嚗?  ??Leader ?貉??芸???
  ??霈?隞亙? Leader ??嚗?暑嚗?  ???游誨瘜?撌交平?∠嚗tcd, TiKV...嚗?
撖阡??∠嚗?  - Chain Replication嚗mazon DynamoDB ??撅方???  - Raft嚗tcd, CockroachDB, TiKV
```

---

## ? Topic 5: FaRM ??Optimistic Concurrency Control + RDMA

### FaRM ?身閮摮?
```
FaRM嚗ast Remote Memory嚗???2015嚗??詨?瘣?嚗?
?蝯勗????鈭斗?憭芣鈭?
 ?銝?冽?閫雿萇?批 + RDMA嚗?蝡舐?亥??園?摮?嚗?????
蝯?嚗?  - ?????喟絞?撘漱?? 10-100 ??  - 撱園???啣凝蝘?
```

### FaRM ?漱??蝔?蝪∪???

```go
// Step 1: Read Phase
//  ??RDMA ?湔霈??蝡航??園?嚗?瑁??雿平蝟餌絞??嚗?for obj_id in needed_objects:
    obj, ver = RDMA_read(obj_id)
    local_reads.append({obj, ver})

// Step 2: Validation Phase
//  撽???????拐辣??臬?寡?
if any(ver_changed(local_reads)):
    abort_and_retry()

// Step 3: Commit Phase嚗 commit ?砍???
for obj_id in local_objects:
    RDMA_write(obj_id, new_value, new_version)
```

### FaRM vs ?喟絞?撘漱???撌桃

```
?喟絞?撘漱??2PC + 蝬脰楝??嚗?
  - 撱園嚗?神蝘?  - ??嚗??蝬脰楝??

FaRM嚗?閫?批 + RDMA嚗?
  - 撱園嚗凝蝘?
  - ??嚗?亥??園?摮?嚗???璆剔頂蝯?
??抒嚗?  - FaRM ?芣?游???single-region嚗漱??  - 頝?Region 隞??喟絞?孵?
```

---

## ? Topic 6: Byzantine Fault Tolerance嚗FT嚗???摨剖捆??
### ??摨剖?頠?憿?
```
?喳?嚗?  - n ??頠????  - ?嗡葉?憭?f ???嚗?賜???荔?
  - 憒?霈?隤?頠????湛?

璇辣嚗?  - ?閬撠?3f+1 ??暺??賢捆敹?f ??Byzantine 蝭暺?  - 撠????⊥????梯?
```

### PBFT嚗ractical Byzantine Fault Tolerance嚗?
```
Castro & Liskov, 1999 閮剛???PBFT嚗?
?詨??嚗?  - 雿輻 View-Stamped Replication嚗?隡?Raft + ??摨哨?
  - Leader ??View 璅?
  - 憒? Leader ??Byzantine嚗韏?View Change

??銴?摨佗?
  - 霈??O(n)
  - 撖怠嚗(n簡) 嚗?閬????暺?嚗?
?嚗?  - 銝?之閬芋蝟餌絞嚗??憭芸之嚗?  - ?虜?冽?舐??迂?臬?憛?
```

### 瘥撟???葉?祈?梯???
```
瘥撟?璉??喟絞 BFT ??閮哨?撘蝬?瞈?蛛?

PoW嚗霅??塚?嚗?  - 銝?閬???芯? Byzantine 蝭暺?  - 隞颱?鈭粹?臭誑??嚗ermissionless嚗?  - ??蝞?蝡嗥瘙箏?隤唳?甈神?憛?
蝻粹?嚗?  - 蝣箄????瘀?6 ??憛???1 撠?嚗?  - ?賣?瘨楊憭?  - ????嚗7 TPS vs Visa ??~65,000 TPS嚗?```

---

## ? Topic 7: Memcached at Facebook ??憭扯?璅∟??瑽?
### Facebook ???瑽?
```
銝惜霈?瑽?
  Web Server ??Memcached ??MySQL

撖怠??
  1. ?湔 MySQL嚗撥銝?湔批神?伐?
  2. 雿踹翰?仃??Delete Cache嚗? Update Cache嚗?  ?箔?暻?Delete ?? Update嚗?    - ?踹?雿萇?? race condition
    - 霈???敺?DB 頛?舀?蝪∪???湔抒???
霈??嚗?  - 敹怠??賭葉?湔餈?
  - 敹怠??芸銝剖? MySQL 頛
```

---

## ? 撌亦?撣怨???Session 8 摮貊?敹?

### 隞?詨??嗥帖

```
?撘頂蝯勗飛蝧?曉嚗歇蝬???

?箇???嚗?  ??CAP Theorem嚗P vs AP 蝟餌絞????  ??銝?湔扳芋??撘瑚??湔????蝯??湔?
?詨??降嚗?  ??MapReduce嚗像銵?蝞???  ??Raft嚗霅?蝞?嚗eader Election + Log Replication嚗?  ??GFS嚗????瑼?蝟餌絞

?脤?銝駁?嚗ession 8 ?啣?嚗?
  ??Linearizability嚗????銝?湔抒?暺?璅?
  ??ZooKeeper嚗?撘?隤踵???  ???撘漱??2PC ??prepare/commit?撩暺? Saga ?蹂誨
  ??Chain Replication嚗銝蝔桀撥銝?湔扳獢?  ??FaRM嚗?閫雿萇?批 + RDMA
  ??BFT嚗??滬摰寥???孵馳?梯?
  ??Memcached嚗之閬芋霈?瑽?```

### ?Ｚ岫擃憿?Session 8 撱嗡撓嚗?
```
1. Linearizability vs Sequential Consistency ?榆?堆?
   ??Linearizability 憿?閬????????
2. 2PC ??blocking ???臭?暻潘?憒?蝺抵圾嚗?   ??Coordinator ??撠?????蝑?
   ???臭誑??3PC ??Saga pattern

3. ZooKeeper ??watch 璈?臭?暻潘?
   ??摰Ｘ蝡航???znode 霈??

4. FaRM 憒??擃??撘漱??
   ??璅?雿萇?批 + RDMA 蝜?雿平蝟餌絞

5. BFT ?閬?撠?暺??賢捆敹?1 ??Byzantine 蝭暺?
   ???喳? 4 ??3f+1 = 4嚗?```

### 撖血????
```
Linearizability ??  ?銵?撣喉?頧董銝摰???甈?+ 摮狡??
ZooKeeper ??  Kafka broker 蝞∠??Base master ?貉?

2PC/Saga ??  瘛窄?漪?梁?閮蝟餌絞?賣?憿撮 Saga ??????
FaRM ??  擃鈭斗?蝟餌絞???漱?像?堆??閬凝蝘?撱園嚗?```

---

## ?? 敺?摮貊?閮嚗?堆?

```
Q2 2026:
  ????撖衣 Raft KV Store嚗 Go嚗?  ??摰? MIT 6.5840 Lab 1-3
  ???梯? Dynamo 隢?嚗P 蝟餌絞隞?”嚗?
Q3 2026:
  ??CMU 15-445 Database Systems
  ???弦 etcd/Consul ??蝣?  ??撖虫? ZooKeeper ?陛?桃???
Q4 2026:
  ???脩垢?撘??楛?伐?GCP Spanner / AWS Aurora嚗?  ???憛??梯?璈瘛勗嚗BFT ??Tendermint ??HotStuff嚗?```

---

*?祉?閮撌亦?撣怨?? 2026-04-05 ?渡???MIT 6.5840 OCW 隤脩?*
*摮貊?甈⊥嚗洵8甈∴??撘頂蝯梢脤?銝駁?嚗??湔抒?隢?隤踵??????鈭斗?嚗?

---

# CMU 15-445 / 645 - Database Systems（資料庫系統）

**學習日期：** 2026-04-05
**課程來源：** https://github.com/Developer-Y/cs-video-courses
**官方網站：** https://15445.courses.cs.cmu.edu/
**授課教授：** Andy Pavlo（CMU）
**參考教材：** Database System Concepts, 6th Edition（Silberschatz, Korth, Sudarshan）

---

## 課程概覽

CMU 15-445 是 CMU 最經典的資料庫系統課程，主軸為「如何設計與實作一個 DBMS」。

**核心 Topics（25堂Lecture）：**
- 關係模型與關係代數（Relational Model & Algebra）
- 儲存管理（Storage Management）
- 索引結構（Indexing）
- 查詢執行（Query Execution）
- 查詢優化（Query Optimization）
- 並行控制（Concurrency Control）
- 日誌與恢復（Logging & Recovery）
- 分散式資料庫（Distributed Databases）

**授課形式：**  Lecture + 5個 C++ 專案（使用 BusTub 教學 DBMS）
**先修知識：** C++、作業系統、資料結構

---

## Topic 1: 資料庫系統的動機（Why Database Systems?）

### 平面文件（CSV）的問題
`
問題 1：資料完整性（DATA INTEGRITY）
  - 如何確保 Artist 和 Album 表中的 artist_name 一致？

問題 2：實作困難（IMPLEMENTATION）
  - 如何高效找到特定記錄？（10億筆資料遍歷太慢）
  - 如何實現跨應用程式共享資料邏輯？

問題 3：持久性（DURABILITY）
  - 程式崩潰時，正在更新的記錄狀態如何保證正確？
`

### 關係模型的誕生（Ted Codd, 1970）
`
早期問題：邏輯層與物理層緊密耦合

Ted Codd 的突破：關係模型
  1. 將資料儲存為簡單的資料結構（表格）
  2. 透過高階語言（SQL）存取資料
  3. 物理儲存細節對應用程式透明

→ 實現了邏輯層與物理層的完全解耦！
`

---

## Topic 2: 關係模型（Relational Model）

### 資料模型三要素
`
1. Structure（結構）：關係、元組、屬性
2. Integrity（完整性約束）：主鍵、外鍵、NOT NULL 等約束
3. Manipulation（操作）：關係代數、SQL
`

### 主鍵 vs 外鍵
`sql
-- 主鍵：唯一標識一條記錄
CREATE TABLE Artist (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- 外鍵：建立表之間的關聯
CREATE TABLE Album (
    album_id INT PRIMARY KEY,
    title VARCHAR(200),
    artist_id INT REFERENCES Artist(id)
);
`

---

## Topic 3: 關係代數（Relational Algebra）⭐⭐⭐

### 7種基礎運算子
`
1. SELECT (σ)：選擇滿足條件的元組
2. PROJECT (π)：只保留指定屬性
3. UNION (∪)：合併兩個關係
4. INTERSECTION (∩)：取交集
5. DIFFERENCE (−)：取差集
6. PRODUCT (×)：笛卡爾積
7. JOIN (⋈)：自然連接
`

### 面試重點：Query Optimization 與關係代數
`
為什麼同樣結果不同執行順序效率差很多？

方法 1：
  (R ⋈ S) → σ_{b_id=102}()  → 先連接再過濾
  代價：兩個表的笛卡爾積可能超級大！

方法 2：
  σ_{b_id=102}(S) → (R ⋈ filtered_S)  → 先過濾再連接
  代價：過濾後的 S 很小，連接很快！

→ 這就是 Query Optimizer 的核心工作！
`

---

## Topic 4: 資料庫儲存（Database Storage）

### Buffer Pool（緩衝池）
`
為什麼需要 Buffer Pool？
  - 磁碟讀取太慢，必須將常用頁緩衝在記憶體中

Buffer Pool Manager 的職責：
  1. 追蹤哪些頁目前在記憶體中
  2. 維護頁的引用計數（pin count）
  3. 淘汰不常用的頁（頁框替換策略）

頁框替換策略：
  - LRU（Least Recently Used）：最久未使用
  - Clock（近似 LRU，更高效）
`

---

## Topic 5: 索引結構（Indexing）⭐⭐⭐

### B+ Tree 搜尋複雜度
`
高度為 h 的 B+ Tree：
  - 搜尋：O(log_f N) 其中 f = 分支因子（fanout）
  - 典型 fanout：100-500
  - 100 萬筆資料：約 3-4 層
  10 億筆資料：約 4-5 層

→ 樹高 4-5 層 = 最多 4-5 次磁碟 I/O（可接受！）
`

---

## Topic 6: 查詢執行（Query Execution）⭐⭐⭐

### 三種處理模型

**1. Iterator Model（Volcano Model，火山模型）：**
`python
# 每個 Operator 實現 open(), next(), close()
class ScanOperator:
    def open(self):
        self.cursor = self.table.first()
    
    def next(self):
        if self.cursor is None:
            return None
        row = self.cursor
        self.cursor = self.table.next(self.cursor)
        return row
`

**3. Vectorized / Batch Model（向量化模型）：**
`python
# 每次 next() 返回一批元組（如 1000 筆）
def scan_next(self):
    return self.table.fetch_batch(1000)
# 優點：可使用 SIMD 加速、cache 效率高
# 目前主流（ClickHouse、Vectorized DB 都用這個）
`

### 連接演算法（Join Algorithms）⭐⭐⭐

**Hash Join（最重要！）：**
`python
# 階段 1：建構雜湊表（Build Phase）
hash_table = {}
for row_r in R:
    hash_table[row_r.key].append(row_r)

# 階段 2：探測（Probe Phase）
for row_s in S:
    for row_r in hash_table.get(row_s.key, []):
        yield combine(row_r, row_s)

# 代價：O(n + m)
`

---

## Topic 7: 並發控制理論（Concurrency Control）⭐⭐⭐

### 交易的四大特性（ACID）

`
A（Atomicity，原子性）：
  - 交易中的所有操作要么全部完成，要么全部不完成
  - 實現方式：Write-Ahead Log（WAL）

I（Isolation，隔離性）：
  - 每個交易仿佛在單獨執行
  - 並發執行的結果 == 某種順序執行的結果
`

### 並發問題

`
1.  Dirty Read（髒讀）：讀取到另一交易未提交的資料
2.  Non-Repeatable Read（不可重複讀）：同一交易兩次讀取同一資料，結果不同
3.  Phantom Read（幻讀）：同一交易兩次查詢，返回了原本不存在的記錄
4.  Lost Update（丟失更新）：兩個交易讀取並更新同一筆資料
5.  Write Skew（寫偏斜）：兩個交易各自讀取一些資料，然後各自更新
`

---

## Topic 8: Two-Phase Locking（兩階段鎖）⭐⭐⭐

### 兩階段鎖（2PL）的規則
`
第一階段（Growing Phase）：
  - 只獲取鎖，不釋放鎖

第二階段（Shrinking Phase）：
  - 只釋放鎖，不獲取新鎖

交易在 commit 或 abort 後才釋放鎖（嚴格 2PL）
`

---

## Topic 9: MVCC（多版本併發控制）⭐⭐⭐

### MVCC 的核心思想
`
每個元組保存多個版本：
  - 每個版本包含：資料內容 + 建立版本的事務時間戳

讀取時：
  - 根據事務的時間戳，選擇可見的最新版本
  - 讀取不需要加鎖！

優點：
  ✓ 讀不阻塞寫，寫不阻塞讀
  ✓ 支援 Snapshot Isolation
  ✓ 實現 Time-Travel 查詢
`

---

## Topic 10: 日誌與恢復（Logging & Recovery）⭐⭐⭐

### Write-Ahead Log（WAL）原則
`
核心原則：
  1. 日誌必須在資料頁寫入磁碟前寫入磁碟
  2. 只有当日誌已刷盤，交易才能提交
`

### ARIES 恢復演算法
`
IBM 的經典恢復演算法（三階段）：

階段 1：Analysis（分析）- 找出崩潰時的 dirty pages 和活躍交易
階段 2：Redo（重做）- 從最後一個 Checkpoint 開始重做所有操作
階段 3：Undo（回滾）- 回滾所有未提交交易的更改
`

---

## Topic 11: 分散式資料庫（Distributed Databases）

### CAP Theorem
`
分散式資料庫系統：
  - C（一致性）：所有節點看到相同的資料
  - A（可用性）：每個請求都得到回覆
  - P（分割容忍）：網路分割時系統仍運行

→ 三者只能滿足兩個

實際取捨：
  - CP（犧牲 A）：ZooKeeper、HBase、BigTable
  - AP（犧牲 C）：DynamoDB、Cassandra
`

---

## 💡 工程師蘇茉的 CMU 15-445 學習心得

### 為什麼選資料庫系統？
`
我的 CS 學習路徑：
  Session 3: MIT 6.006 演算法基礎
  Session 4: MIT 6.046 進階演算法設計
  Session 5: MIT 6.5840 分散式系統
  Session 6: MIT 6.1810 作業系統
  Session 7-8: MIT 6.5840 分散式深入

為什麼需要資料庫知識？
  1. 後端工程師每天都和 DBMS 打交道
  2. 面試高頻：索引原理、並發控制、事務隔離
  3. 分散式資料庫（TiDB, CockroachDB）需要兩者兼備
  4. 理解 Query Optimization 才能寫出高效 SQL
`

### 面試高頻題目
`
1. B+ Tree vs Hash Index：何時用哪個？
   → 答案：等值查詢用 Hash，範圍查詢用 B+ Tree

2. 事務隔離級別：髒讀、不可重複讀、幻讀的差異？
   → 答案：取決於鎖的使用方式

3. 兩階段鎖（2PL）的原則？
   → 答案：Growing Phase 只加鎖，Shrinking Phase 只釋放鎖

4. MVCC 的優點？
   → 答案：讀不阻塞寫，寫不阻塞讀

5. MySQL InnoDB 的預設隔離級別？
   → 答案：REPEATABLE READ

6. WAL 的原則？
   → 答案：日誌必須在資料頁寫入磁碟前寫入磁碟
`

---

## 📅 後續學習計畫

`
Q2 2026:
  □ 完成 CMU 15-445 Labs（Buffer Pool、B+ Tree、Concurrency Control）
  □ 實作一個簡單的 SQLite Clone（基於本課概念）
  □ 閱讀經典論文（ARIES、MVCC、BigTable）

Q3 2026:
  □ MIT 6.854（Advanced Algorithms）— 演算法最終章
  □ CMU 15-721（Advanced DBMS）— 純研究導向
  □ Rust 實作一個 Columnar DB

Q4 2026:
  □ 分散式 SQL 引擎設計
  □ 雲端資料庫深入（GCP Spanner / AWS Aurora）
`

---

*本筆記由工程師蘇茉於 2026-04-05 整理自 CMU 15-445 Database Systems 課程*
*學習次數：第9次（資料庫系統專題）*
# Computer Networks（電腦網路）
**學習日期：** 2026-04-05
**課程來源：** https://github.com/Developer-Y/cs-video-courses
**相關課程：** MIT 6.033（Computer Networking）、Stanford CS144、Kurose & Ross 教科書

---

## 課程概覽

Computer Networks 是軟體工程的基石之一。所有現代網路服務（Web、API、雲端）都建立在網路之上。

**核心 Topics：**
- OSI 7 層模型 vs TCP/IP 4 層模型
- 實體層與資料鏈結層（Ethernet、Wi-Fi）
- 網路層（IP、Router）
- 傳輸層（TCP、UDP）
- 應用層（HTTP、DNS、DHCP）
- 網路安全（TLS、Firewall）
- 路由演算法

---

## Topic 1: OSI 7 層模型 vs TCP/IP 4 層模型

### 為什麼需要分層？
```
網路太複雜，分層後：
  ✓ 每層專心做一件事
  ✓ 層與層之間有標準介面
  ✓ 某一層壞了不影響其他層
  ✓ 方便獨立開發和優化

原則：每一層只知道自己上下相鄰的層
```

### OSI 7 層模型（由上到下）
```
Layer 7：應用層（Application）
  → HTTP、DNS、SMTP、FTP、SSH
  → 負責：網路應用程式之間的溝通

Layer 6：表達層（Presentation）
  → SSL/TLS、JPEG、GIF、ASCII
  → 負責：資料格式轉換、加密解密

Layer 5：會議層（Session）
  → NetBIOS、RPC
  → 負責：建立、管理、終止會話

Layer 4：傳輸層（Transport）
  → TCP、UDP
  → 負責：端到端（end-to-end）傳輸、可靠性

Layer 3：網路層（Network）
  → IP、ICMP、Router
  → 負責：跨網路的路徑選擇（Routing）

Layer 2：資料鏈結層（Data Link）
  → Ethernet、Switch、MAC Address
  → 負責：同一網路內的資料傳輸、錯誤偵測

Layer 1：實體層（Physical）
  → 電纜，光纖、集線器（Hub）
  → 負責：比特的物理傳輸
```

### TCP/IP 4 層模型（實務上更常用）
```
Layer 4：應用層（Application）= OSI L7 + L6 + L5
  → HTTP、HTTPS、SSH、DNS、DHCP、SMTP

Layer 3：傳輸層（Transport）
  → TCP（可靠）、UDP（快速）

Layer 2：網際網路層（Internet）
  → IP（IPv4、IPv6）、ICMP

Layer 1：網路介面層（Link / Network Access）
  → Ethernet、Wi-Fi、ARP
```

### 資料封裝流程
```
應用程式（Data）
    ↓ [HTTP]
應用層（Segment / Message）
    ↓ [TCP Header]
傳輸層（Packet / Datagram）
    ↓ [IP Header]
網路層（Frame）
    ↓ [Ethernet Header + FCS]
資料鏈結層（Bits）
    ↓
實體層（Physical）

接收端從下往上解封裝：
  Bits → Frame → Packet → Segment → Data
```

### 工程師記憶口訣
```
OSI 7 層：All People Seem To Need Data Processing
  A(7) P(6) S(5) T(4) N(3) D(2) P(1)

TCP/IP 4 層：All Dont Need Screaming Penguins
  A(4) D(3) N(2) T(1)
  （或簡單記：應、傳、網、鏈）
```

---

## Topic 2: 實體層與資料鏈結層（Physical & Data Link）

### Ethernet（乙太網路）
```
歷史：
  - 1973：Xerox PARC 發明
  - 1983：IEEE 802.3 標準化
  - 至今：仍是 LAN 主流

速度演進：
  10 Mbps → 100 Mbps → 1 Gbps → 10 Gbps → 40/100 Gbps

乙太網路 Frame 結構：
┌──────────┬──────┬──────┬─────────────┬──────┬─────┬────────┐
│ Preamble │ Dest │ Src  │   Type/Len  │ Data │ PAD │  FCS  │
│  7 bytes │ 6B   │ 6B   │   2 bytes   │      │     │ 4B    │
└──────────┴──────┴──────┴─────────────┴──────┴─────┴────────┘

Preamble：7B同步碼（10101010...）
Dest MAC：目標 MAC 位址
Src MAC：來源 MAC 位址
Type/Length：0x0800 = IPv4，0x0806 = ARP
Data：46-1500 bytes（最小46，若不足需 padding）
FCS：Frame Check Sequence（CRC32，錯誤偵測）
```

### MAC 位址（Media Access Control Address）
```
MAC 位址 = 48 bits = 6 bytes
格式：XX:XX:XX:YY:YY:YY（十六進位）

前半（XX:XX:XX）：OUI，廠商識別碼
後半（YY:YY:YY）：由廠商自行分配

範例：
  CC:46:D6:3C:DE:AB
  ↑ OUI（Intel 廠商）
          ↑ 網卡序號

廣播 MAC：FF:FF:FF:FF:FF:FF
  → 發送到所有設備
```

### Switch（交換機）vs Hub（集線器）
```
Hub（Layer 1）：
  - 純物理層設備
  - 收到什麼就廣播什麼
  - 碰撞域大
  - 已被淘汰

Switch（Layer 2）：
  - 資料鏈結層設備
  - 維護 MAC Address Table（CAM Table）
  - 根據 MAC 位址轉發（一對一）
  - 每個埠都是獨立 Collision Domain

Switch 的 CAM Table：
  MAC Address    Port
  ────────────  ───
  00:1A:2B:...    1
  00:3C:4D:...    5
```

### ARP（Address Resolution Protocol）
```
問題：只知道 IP 位址，如何知道對應的 MAC 位址？
答案：ARP

ARP 流程（同一網域內）：
  1. A 想和 B 通信，但只知道 B 的 IP
  2. A 查自己的 ARP Table → 沒有
  3. A 發送 ARP Request（廣播）：「誰的 IP 是 192.168.1.5？」
  4. B 收到，回覆 ARP Reply（單播）
  5. A 學到 B 的 MAC，存入 ARP Cache（通常 20 分鐘過期）
```

### VLAN（Virtual LAN）
```
為什麼需要 VLAN？
  - 廣播流量太多 → 分割廣播域
  - 安全隔離
  - 方便管理

原理：
  - Switch 上的連接埠分組
  - 同一組屬於同一 VLAN
  - 不同 VLAN 需透過 Router 才能通信

802.1Q Tag：
  VLAN ID：12 bits → 0-4095（實際用 1-4094）
```

---

## Topic 3: 網路層（Network Layer）⭐⭐⭐

### IP 位址（IPv4）
```
IPv4：32 bits，4 bytes
格式：a.b.c.d（0-255）

範例：
  192.168.1.100 = 11000000.10101000.00000001.01100100

IP 位址組成：
  ┌────────────┬────────────┐
  │  Network   │   Host     │
  │   ID       │   ID       │
  └────────────┴────────────┘

  Network ID：辨識網段（類似街道名）
  Host ID：辨識該網段內的設備（類似門牌號）
```

### 子網路遮罩（Subnet Mask）
```
255.255.255.0 = /24
  = 11111111.11111111.11111111.00000000
                Network  |  Host

常用 CIDR：
  /24  = 255.255.255.0   → 254 主機
  /26  = 255.255.255.192 → 62 主機
  /27  = 255.255.255.224 → 30 主機
  /28  = 255.255.255.240 → 14 主機
  /30  = 255.255.255.252 → 2 主機（點對點鏈路用）

計算可用範圍：
  192.168.1.0/24
  Network：192.168.1.0
  Broadcast：192.168.1.255
  可用範圍：192.168.1.1 - 192.168.1.254
```

### CIDR（Classless Inter-Domain Routing）
```
為什麼廢除 Class？
  - Class B（/16）只有 65534 可用 IP，太多浪費
  - Class C（/24）只有 254 可用 IP，不夠用

私有 IP（Private IP，不會出現在網際網路）：
  10.0.0.0/8       → 10.0.0.0 - 10.255.255.255
  172.16.0.0/12    → 172.16.0.0 - 172.31.255.255
  192.168.0.0/16   → 192.168.0.0 - 192.168.255.255

保留 IP：
  127.0.0.1        → localhost（環回介面）
  169.254.0.0/16   → Link-local（DHCP 失敗時自動取得）
```

### NAT（Network Address Translation）
```
為什麼需要 NAT？
  IPv4 位址不夠用（只有 ~42 億個）
  → 多台設備共用一個公共 IP 上網

NAT 原理：
  私有網路（192.168.1.x）→ NAT 設備（公共 IP 1.2.3.4）→ 網際網路

  內部設備發送：
    來源：192.168.1.100:54321 → 目標：8.8.8.8:80
  NAT 轉換後：
    來源：1.2.3.4:54321       → 目標：8.8.8.8:80

NAT 的問題：
  ✗ 外部無法主動連線進來（P2P 應用困難）
  ✗ IP 變動時連線會中斷

類型：
  - 靜態 NAT：一對一映射（用在公開伺服器）
  - 動態 NAT：從公共 IP 池動態分配
  - PAT（NAPT）：多對一（最常用）
```

### IPv6
```
為什麼需要 IPv6？
  IPv4 只有 ~42 億個位址，不夠全球使用
  IPv6 有 340 潤（340 undecillion）個位址

IPv6 格式：
  128 bits = 16 bytes
  2001:0db8:85a3:0000:0000:8a2e:0370:7334
  簡化：2001:db8:85a3::8a2e:370:7334

特點：
  ✓ 位址空間巨大（128 bits）
  ✓ 不需要 NAT（每個設備都能有公共 IP）
  ✓ 內建 IPSec（安全性）
  ✓ 自動設定（Autoconfiguration）
  ✓ 沒有廣播（用多播代替）
```

### IP 封包格式（IPv4 Header）
```
┌────────┬────────┬───────────┬────────────────┬─────────────────────┐
│Version │  IHL   │  ToS/DSCP │     Length     │      Identification  │
│  4b    │  4b    │    8b     │     16b        │         16b           │
├────────┼────────┼───────────┼────────────────┼─────────────────────┤
│ Flags  │ Fragment Offset   │     TTL         │     Protocol         │
│  3b    │      13b          │     8b          │       8b              │
├────────┼────────┼───────────┼────────────────┼─────────────────────┤
│         Header Checksum          │            Source IP              │
│              16b                │              32b                   │
├─────────────────────────────────┼───────────────────────────────────┤
│          Destination IP         │                                   │
│              32b               │           Options (optional)        │
└─────────────────────────────────┴───────────────────────────────────┘

TTL：存活時間（每經過一個 Router -1，避免封包永久循環）
Protocol：
  1 = ICMP
  6 = TCP
  17 = UDP
  47 = GRE
  50 = ESP（IPSec）
```

### ICMP（Internet Control Message Protocol）
```
ICMP 是網路層的輔助協定，用於傳遞錯誤訊息和控制訊息。

常見 ICMP 訊息：
  Type 0：Echo Reply（ping 回應）
  Type 3：Destination Unreachable
  Type 8：Echo Request（ping 請求）
  Type 11：Time Exceeded（TTL 過期）

traceroute 原理：
  - 發送 TTL=1 的 UDP 封包
  - 第一個 Router 回覆 TTL Exceeded（Type 11）
  - 依此類推，直到到達目標
```

### Router（路由器）
```
Router 的職責：
  1. 決定封包轉發路徑（Routing）
  2. 連接不同網段（不同 IP 網路）
  3. NAT（很多路由器內建）
  4. Firewall（簡單防火牆功能）
  5. DHCP Server（很多路由器內建）

路由表（Routing Table）：
  目的地           遮罩          閘道          介面
  ─────────────────────────────────────────────────────────────
  0.0.0.0         0.0.0.0         192.168.1.1       eth0
  192.168.1.0     255.255.255.0    *                 eth0
  192.168.2.0    255.255.255.0    192.168.1.254     eth0

路由決策（Longest Prefix Match）：
  收到目標 IP = 192.168.1.100
  → 匹配 192.168.1.0/24（匹配 24 bits 最長）
```

### 路由演算法

**1. Distance Vector — RIP**
```
原理：
  - 每個 Router 定期（約 30 秒）廣播自己的路由表
  - 收到鄰居的資訊後，評估最佳路徑
  - 只知道到每個網路的「距離」（Hop Count）和方向

限制：
  - 最大 Hop Count = 15（16 = 無限遠）
  - 收斂慢（Convergence Time 長）
  - 可能產生路由迴圈（Routing Loop）
```

**2. Link State — OSPF**
```
原理：
  - 每個 Router 向整個 AS 廣告自己的鏈路狀態
  - 每個 Router 各自計算最短路徑（使用 Dijkstra 演算法）

優點：
  ✓ 收斂快
  ✓ 沒有路由迴圈
  ✓ 支援大規模網路
```

**3. Path Vector — BGP**
```
用途：
  - 連接不同 AS（Autonomous System）
  - 網際網路的骨幹路由協定

特點：
  - 攜帶完整路徑屬性（AS Path）
  - 可做策略路由（Policy-Based Routing）
  - 由 ISP 管理者手動設定

BGP Session：
  eBGP：不同 AS 之間
  iBGP：同一 AS 內部
```

---

## Topic 4: 傳輸層（Transport Layer）⭐⭐⭐

### TCP vs UDP
```
┌──────────────┬────────────────────────────┬────────────────────────────┐
│     特性      │            TCP              │            UDP              │
├──────────────┼────────────────────────────┼────────────────────────────┤
│ 連接導向       │ ✅ 建立連線（3-way          │ ❌ 無連線                   │
│              │    handshake）              │                            │
│ 可靠性        │ ✅ 可靠、有序、錯誤控制       │ ❌ 不可靠、無序             │
│ 流量控制       │ ✅ Sliding Window          │ ❌ 無                       │
│ 擁塞控制       │ ✅（Cubic, BBR, etc.）     │ ❌ 無                       │
│ 速度          │ 較慢（Overhead 多）         │ 快速（Minimal overhead）    │
│ 應用場景       │ HTTP, SSH, SMTP, FTP,     │ DNS, DHCP, VoIP, Video,    │
│              │   MySQL, API (一般)         │   Gaming, QUIC             │
└──────────────┴────────────────────────────┴────────────────────────────┘
```

### TCP 三向交握（Three-Way Handshake）⭐⭐⭐
```
客戶端                              伺服器
   │                                    │
   │ ──────── SYN (seq=x) ───────────→ │ 客戶端發起連線請求
   │                                    │
   │ ←────── SYN-ACK (seq=y, ack=x+1) │ 伺服器回覆同意 + 客戶端序號確認
   │                                    │
   │ ──────── ACK (ack=y+1) ─────────→ │ 客戶端確認
   │                                    │
   │         連線建立完成！               │
```

**為什麼需要 3 次握手，而不是 2 次？**
```
2 次握手的問題：
  - 客戶端發送 SYN（舊的、延遲的）
  - 伺服器回 SYN-ACK
  - 客戶端早已斷線，伺服器卻建立了連線

3 次握手解決了這個問題：
  - 第三次 ACK 攜帶資料，確保客戶端真的活著
  - 雙方都確認對方的接收能力正常
```

### TCP 四向終止（Four-Way Termination）
```
客戶端                              伺服器
   │                                    │
   │ ──────── FIN (seq=u) ───────────→ │ 客戶端說：我發完了
   │                                    │
   │ ←─────── ACK (ack=u+1) ────────── │ 伺服器說：收到
   │     （伺服器還在傳送資料...）        │
   │                                    │
   │ ←─────── FIN (seq=w) ──────────── │ 伺服器說：我也發完了
   │                                    │
   │ ──────── ACK (ack=w+1) ─────────→ │ 客戶端說：收到
   │                                    │
   │     等待 2MSL 後關閉連線            │
```

### TCP 流量控制（Flow Control）
```
Sliding Window（滑動窗口）：
  目的：防止發送方傳太快，接收方緩衝區不夠用

運作方式：
  - 接收方告訴發送方：「你最多還能發多少」（rwnd = receiver window）
  - 發送方根據 rwnd 調整傳送速度
  - ACK 確認時攜帶 rwnd 值
```

### TCP 擁塞控制（Congestion Control）
```
四大演算法：

1. Slow Start（慢啟動）：
   - 初始 cwnd 很小（通常 1 MSS）
   - 每收到一個 ACK，cwnd += 1 MSS
   - 指數成長，直到達到 ssthresh

2. Congestion Avoidance（擁塞避免）：
   - 達到 ssthresh 後進入
   - 每收到一個 ACK，cwnd += 1/cwnd（MSS）
   - 線性成長

3. Fast Retransmit（快速重傳）：
   - 收到 3 個 Duplicated ACK
   - 立即重傳遺失的 Segment
   - 不等 timeout

4. Fast Recovery（快速恢復）：
   - Fast Retransmit 後進入
   - ssthresh = cwnd/2, cwnd = ssthresh + 3
   - 之後線性成長

TCP 演算法變體：
  - TCP Reno（經典）
  - TCP CUBIC（Linux 預設）
  - TCP BBR（Google，基於模型）
```

### 常用 Port Numbers（面試必背）
```
20/21  FTP（檔案傳輸）
22     SSH（安全登入）
23     Telnet（不安全）
25     SMTP（郵件傳送）
53     DNS（名稱解析）
67/68  DHCP（伺服器/客戶端）
80     HTTP
110    POP3（郵件接收）
143     IMAP（郵件同步）
443    HTTPS
465    SMTPS（SSL）
587    SMTP（TLS）
993    IMAPS
995    POP3S
3306   MySQL
5432   PostgreSQL
6379   Redis
27017  MongoDB

範圍：
  0-1023：系統保留（需 root 權限）
  1024-49151：已登記（IANA 註冊）
  49152-65535：動態私有（客戶端隨機端口）
```

---

## Topic 5: 應用層（Application Layer）⭐⭐⭐

### DNS（Domain Name System）
```
為什麼需要 DNS？
  人類記不住 IP，記得住網址（google.com）
  DNS 將網址翻譯成 IP

DNS 層級架構：
  Root DNS Server（.）
      │
      ├── .com TLD Server
      │      ├── google.com
      │      │      ├── www.google.com
      │      │      └── mail.google.com
      └── .tw TLD Server

DNS Record Types：
  A Record：網址 → IPv4
  AAAA Record：網址 → IPv6
  CNAME：網址 → 另一個網址（別名）
  MX：網址 → 郵件伺服器
  NS：網址 → 名稱伺服器
  TXT：SPF、DKIM、DMARC 等驗證
  PTR：IP → 網址（反向查詢）
```

### DNS 查詢流程
```
1. 瀏覽器查快取（Browser DNS Cache）
2. 系統快取（OS DNS Resolver Cache）
3. 查 hosts 檔
4. 本機 DNS Resolver（通常 8.8.8.8 或電路商的 DNS）
5. Root DNS Server（世界上只有 13 組）
6. TLD DNS Server（.com, .org, .tw...）
7. Authoritative DNS Server（目標網域的 DNS）
```

### DHCP（Dynamic Host Configuration Protocol）
```
用途：自動分配 IP 位址

DHCP 分配流程（DORA）：
  1. Discover：客戶端廣播「需要 IP」
  2. Offer：伺服器提供可用 IP
  3. Request：客戶端請求該 IP
  4. Acknowledge：伺服器確認

DHCP 分配的內容：
  ✓ IP 位址
  ✓ Subnet Mask
  ✓ Default Gateway
  ✓ DNS Server
  ✓ Lease Time（通常 24 小時）
```

### HTTP / HTTPS
```
HTTP 1.0：
  - 每個請求建立一個 TCP 連線

HTTP 1.1：
  - 支援 Persistent Connection（Keep-Alive）
  - 缺點：Head-of-Line Blocking（第一個請求卡住後面的）

HTTP 2.0：
  - Multiplexing（多個請求復用一個連線）
  - Header Compression（HPACK）
  - Server Push（伺服器主動推送）
  - 仍然有 Head-of-Line Blocking（Layer 7）

HTTP/3（QUIC）：
  - 基於 UDP（不再有 TCP Head-of-Line Blocking）
  - 整合 TLS 1.3，握手更快
  - 0-RTT（已連線過的客戶端直接傳資料）
  - 行動網路切換時連線不中斷（QUIC Connection Migration）
```

### HTTP 請求結構
```
Request：
  GET /index.html HTTP/1.1\r\n
  Host: www.example.com\r\n
  User-Agent: Mozilla/5.0\r\n
  Accept: text/html\r\n
  \r\n

Response：
  HTTP/1.1 200 OK\r\n
  Date: Sun, 05 Apr 2026 07:18:00 GMT\r\n
  Content-Type: text/html; charset=UTF-8\r\n
  Content-Length: 1234\r\n
  \r\n
  <html>...</html>

Status Codes：
  1xx：資訊（100 Continue）
  2xx：成功（200 OK, 201 Created, 204 No Content）
  3xx：重新導向（301 Moved Permanently, 302 Found, 304 Not Modified）
  4xx：用戶端錯誤（400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found）
  5xx：伺服器錯誤（500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout）
```

### TLS（Transport Layer Security）
```
TLS 的職責：
  ✓ 身份驗證（Certificate）
  ✓ 資料加密（Encryption）
  ✓ 完整性檢查（MAC / HMAC）

TLS 1.2 Handshake（HTTPS）：
  客戶端                              伺服器
     │                                    │
     │ ─────── ClientHello ───────────→ │ 支援的加密套件列表
     │                                    │
     │ ←────── ServerHello ─────────── │ 選擇加密套件 + 伺服器憑證
     │ ←────── Certificate ─────────── │ 伺服器憑證（含公鑰）
     │ ←────── ServerHelloDone ─────── │
     │                                    │
     │ ─────── ClientKeyExchange ─────→ │ 交換 Pre-Master Secret
     │ ─────── ChangeCipherSpec ─────→ │ 告知開始加密
     │ ─────── Finished ─────────────→ │ 加密驗證訊息
     │                                    │
     │ ←────── ChangeCipherSpec ────── │
     │ ←────── Finished ────────────── │
     │                                    │
     │ ═══════════ 加密傳輸 ═══════════ │ HTTP 請求/回應
```

---

## Topic 6: 網路安全基礎

### 對稱加密 vs 非對稱加密
```
對稱加密（Symmetric）：
  - 同一把鑰匙加解密
  - 速度快，適合大量資料
  - 問題：鑰匙如何安全傳遞？
  - 演算法：AES、DES、3DES、ChaCha20

非對稱加密（Asymmetric）：
  - 公鑰加密、私鑰解密
  - 或私鑰加密、公鑰解密（數位簽章）
  - 速度慢，適合少量資料
  - 演算法：RSA、ECC（橢圓曲線）

混合加密（實務做法）：
  1. 用非對稱加密交換「對稱 Session Key」
  2. 用對稱加密傳送實際資料
```

### 數位憑證與 PKI
```
為什麼需要數位憑證？
  → 確認「你就是你」

憑證內容：
  - 主體名稱（example.com）
  - 公鑰
  - 發行者（Certificate Authority，CA）
  - 有效期限
  - 數位簽章（由 CA 的私鑰簽署）

憑證鏈（Certificate Chain）：
  Root CA（受信任的根源）
    ↓（由 Root CA 簽署）
  Intermediate CA（中介憑證）
    ↓（由 Intermediate CA 簽署）
  Server Certificate（伺服器憑證）

瀏覽器驗證流程：
  1. 收到伺服器憑證
  2. 查看是誰簽的（Issuer）
  3. 找到簽署者的憑證
  4. 驗證簽章（用 Issuer 的公鑰）
  5. 重複直到 Root CA
  6. 確認 Root CA 在瀏覽器的信任清單中

知名 CA：
  DigiCert、Let's Encrypt、Comodo、GoDaddy
```

### 防火牆（Firewall）
```
防火牆的職責：根據規則允許或阻擋網路流量

類型：
  1. 網路層防火牆（Packet Filter）
     - 根據 IP、Port、Protocol 過濾
     - 最基本、最快
     - 例：Linux iptables、nftables

  2. 狀態檢測防火牆（Stateful Firewall）
     - 追蹤連線狀態（NEW, ESTABLISHED, RELATED）
     - 只有已建立連線的回程流量才能通過
     - 例：Cisco ASA、Linux iptables --state

  3. 應用層防火牆（Application Firewall）
     - 深度檢查內容（HTTP、HTTPS）
     - 可阻擋特定的 URL、Cookie、Payload
     - 例：WAF（Web Application Firewall）

iptables 範例：
  iptables -A INPUT -p tcp --dport 80 -j ACCEPT   # 允許 HTTP
  iptables -A INPUT -p tcp --dport 443 -j ACCEPT  # 允許 HTTPS
  iptables -A INPUT -p tcp --dport 22 -j ACCEPT   # 允許 SSH
  iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT  # 允許已建立連線
  iptables -A INPUT -j DROP                         # 預設拒絕
```

### VPN（Virtual Private Network）
```
VPN 的用途：
  ✓ 加密傳輸（防止竊聽）
  ✓ 遠端存取（人在外面可以存取公司網路）
  ✓ 隱藏 IP（翻牆）

常見 VPN 協定：
  PPTP（已淘汰，不安全）
  L2TP/IPsec（中等速度，需要預共享金鑰）
  OpenVPN（開源，基於 SSL/TLS）
  WireGuard（現代，效能極佳）
  IPSec（速度最快，設定複雜）
  TLS VPN（如 Cloudflare Access）

WireGuard：
  - 現代 VPN 協定
  - 使用 Curve25519（橢圓曲線密碼學）
  - ChaCha20-Poly1305（認證加密）
  - 程式碼極少（~4000 行），容易稽核
  - 連線速度快
```

---

## Topic 7: 網路程式設計實務

### Socket 程式設計概念
```
Socket = IP Address + Port Number

伺服器端流程：
  1. socket()：建立 socket
  2. bind()：綁定 IP + Port
  3. listen()：監聽連線
  4. accept()：等待客戶端連線（blocking）
  5. read()/write()：讀寫資料
  6. close()：關閉連線

客戶端流程：
  1. socket()：建立 socket
  2. connect()：連線到伺服器
  3. write()/read()：讀寫資料
  4. close()：關閉連線
```

### TCP Socket 範例（Python）
```python
# 伺服器
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8080))
server.listen(5)

while True:
    client, addr = server.accept()  # 阻塞等待
    data = client.recv(1024)
    print(f"收到：{data}")
    client.send(b"Hello from server")
    client.close()

# 客戶端
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))
client.send(b"Hello from client")
response = client.recv(1024)
print(f"收到：{response}")
client.close()
```

### UDP Socket 範例（Python）
```python
# 伺服器
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 8080))

while True:
    data, addr = server.recvfrom(1024)
    print(f"收到：{data} 從 {addr}")
    server.sendto(b"pong", addr)

# 客戶端
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b"ping", ('127.0.0.1', 8080))
response, _ = client.recvfrom(1024)
print(f"收到：{response}")
```

### select / epoll（高併發 IO）
```
傳統同步 IO（blocking）：
  - 每個連線一個執行緒
  - 缺點：連線多了記憶體爆炸

IO Multiplexing：
  select/poll：
    - 用一個執行緒監控多個 FD（file descriptor）
    - 缺點：有 FD 數量限制（select: 1024）
    - 缺點：每次都要把所有 FD 傳入核心

epoll（Linux）：
    - 核心維護紅黑樹，不用每次傳入所有 FD
    - 只返回「準備好的 FD」列表
    - 支援邊緣觸發（Edge Triggered）

常見使用場景：
  - Nginx：epoll（處理高併發）
  - Redis：IO 多工（自己實現）
  - Node.js：libuv（平台無關）
```


---

## 💡 工程師蘇茉的 Computer Networks 學習心得

### 為什麼需要網路知識？
```
作為後端 / 全端工程師，每天都在和網路打交道：
  1. API 開發：HTTP、TCP/IP、TLS
  2. 部署：防火牆規則、Port 配置、DNS
  3. Debug：網路延遲、連線逾時、DNS 解析失敗
  4. 面試：TCP 三向交握、HTTP 演進、CIDR 計算
```

### 面試高頻網路題目
```
1. TCP vs UDP 的差異？何時用哪個？
   → TCP 可靠+有序，UDP 快速無連線

2. TCP 三向交握流程？為什麼需要 3 次？
   → SYN → SYN-ACK → ACK，防止舊封包建立錯誤連線

3. TCP 四次終止？為什麼不是三次？
   → 伺服器可能還有資料要傳，所以先回 ACK，等資料傳完再發 FIN

4. HTTP 1.0 vs 1.1 vs 2.0 vs 3.0 的差異？
   → Keep-Alive、Pipeline、Multiplexing、QUIC

5. TCP 流量控制 vs 擁塞控制的差異？
   → 流量控制：接收方緩衝區夠不夠
   → 擁塞控制：網路是否堵塞

6. 什麼是三次交握延遲（3-way handshake latency）？
   → 每個新 TCP 連線都需要 1.5 個 RTT 才能開始傳資料
   → 這就是 HTTP/2 Multiplexing 和 QUIC 0-RTT 的價值

7. DNS 查詢流程？
   → 瀏覽器快取 → 系統快取 → hosts → DNS Resolver → Root → TLD → Authoritative

8. CIDR 計算：192.168.1.100/26 的網路位址、廣播位址、可用範圍？
   → 網路位址：192.168.1.64
   → 廣播位址：192.168.1.127
   → 可用範圍：192.168.1.65 - 192.168.1.126

9. HTTPS TLS Handshake 流程？
   → ClientHello → ServerHello + Certificate → ClientKeyExchange → ChangeCipherSpec → Finished

10. ARP 的流程？
    → 廣播 ARP Request → 目標回 ARP Reply → 快取 MAC 位址
```

### 實務應用場景
```
API 開發：
  - REST API 通常用 HTTP/JSON over TCP
  - 即時 API 可能用 WebSocket、Server-Sent Events（SSE）或 gRPC
  - 即時金融資料：WebSocket 推送
  - 串流影片：HTTP Live Streaming（HLS）

Socket 程式設計：
  - Python socket 搭配 epoll：高性能網路伺服器
  - 非阻塞 IO：Nginx、Redis 的核心

網路監控與 Debug：
  - Wireshark：封包分析
  - tcpdump：命令列網路監控
  - curl / Postman：HTTP API 測試
  - ping / traceroute / mtr：網路診斷工具
```

---

## 📅 後續學習計畫

```
Q2 2026:
  □ 實作一個簡單的 TCP 伺服器（Python）
  □ 實作一個 HTTP 伺服器（理解 HTTP 協議）
  □ Wireshark 分析 TCP 三向交握

Q3 2026:
  □ 實作 DNS 解析器
  □ 研究 TLS 1.3 握手流程
  □ 實作簡單的 VPN 客戶端

Q4 2026:
  □ 雲端網路深入（GCP VPC / AWS VPC）
  □ 網路安全加固
```

---

*本筆記由工程師蘇茉於 2026-04-05 整理自 Computer Networks 課程*
*學習次數：第9次（電腦網路專題）*

---

# CS61C - Great Ideas in Computer Architecture（電腦結構）
**學習日期：** 2026-04-05
**課程來源：** https://github.com/Developer-Y/cs-video-courses
**官方網站：** https://cs61c.org/
**授課教授：** Lisa Yan（UC Berkeley）— Spring 2026
**參考教材：** Computer Organization and Design RISC-V Edition（Patterson & Hennessy）

---

## 課程概覽

CS61C 是 UC Berkeley 的電腦結構課程，核心理念是「從硬體到軟體的完整理解」。與 MIT 6.004/6.1810 不同，CS61C 更強調「如何用軟體觀點理解硬體」，以及「軟體開發者需要知道的硬體知識」。

**核心 Topics（40堂Lecture）：**
- Number Representation（數字表示）
- C 記憶體管理（C Memory Management）
- RISC-V 指令集架構
- CPU 設計（Single-Cycle、Pipelined）
- 快取（Caches）
- 虛擬記憶體（Virtual Memory）
- 平行運算（Parallelism：SIMD、TLP、MIMD、Concurrency）

**授課特色：**
- 使用 Venus（RISC-V 模擬器）進行實作
- 4個核心專案（snek 語言、CPU、Parallelism）
- 強調「偉大想法（Great Ideas）」：Amdahl's Law、Locality、Pipeline、Dependability

---

## Topic 1: Number Representation（數字表示）⭐⭐⭐

### 二進位基礎
```
位元（Bit）：0 或 1
位元組（Byte）：8 bits
N bits 能表示：2^N 個不同的值

範例：
  1 bit：2 個值（0, 1）
  8 bits：256 個值（0-255 或 -128 到 127）
  32 bits：約 40 億個值
```

### 有號整數：二補數（Two's Complement）
```
為什麼用二補數？
  ✓ 0 只有一種表示（0000）
  ✓ 加法和減法可以用同一個電路
  ✓ 電路簡單、速度快

二補數的表示範圍：
  N bits：-2^(N-1) 到 +2^(N-1) - 1
  8 bits：-128 到 +127
  32 bits：-2,147,483,648 到 +2,147,483,647

二補數快速轉換：
  正數：直接二進位
  負數：取正數的補數（bit flip）+ 1

  例：-5 在 8 bits
  1. 5 = 00000101
  2. 取補數：11111010
  3. +1：11111011  →  -5
```

### 十六進位（Hexadecimal）
```
為什麼用 Hex？
  ✓ 4 bits = 1 hex digit（方便轉換）
  ✓ 比二進位更簡短
  ✓ 記憶體位址常用

轉換：
  Binary: 1111 1010 0101 0011
  Hex:    F    A    5    3
  → 0xFA53

常見 Hex 應用：
  - 記憶體位址：0x7fff0000
  - 顏色代碼：0xFF5733
  - 網路位址：IPv6 用 hex 表示
```

### 浮點數（Floating Point）— IEEE 754⭐⭐⭐
```
浮點數格式：
  ┌────────┬──────────┬───────────────────────────┐
  │  Sign  │ Exponent │       Mantissa            │
  │  1 bit │  8 bits  │        23 bits            │
  └────────┴──────────┴───────────────────────────┘

  (-1)^S × 1.M × 2^(E - 127)

範例：9.0 在 IEEE 754
  9.0 = 1001.0（二進位）
       = 1.001 × 2^3
  Sign = 0（正數）
  Exponent = 3 + 127 = 130 = 10000010
  Mantissa = 001（只取小數部分）

特殊值：
  - +0：全部為 0
  - -0：Sign=1, 其餘 0
  - +∞：Exponent=255, Mantissa=0
  - NaN：Exponent=255, Mantissa≠0

浮點數的問題：
  1. 精確度損失：0.1 + 0.2 ≠ 0.3（！）

  2. 溢位（Overflow）：兩個大浮點數相乘可能變成 ∞

  3. 下溢（Underflow）：非常小的數接近零

  4. 不滿足結合律：
     (1e20 + -1e20) + 3.14 ≠ 1e20 + (-1e20 + 3.14)
```

### 浮點數計算的常見陷阱
```c
// 問題 1：比較浮點數
if (x == 0.3)  // 千萬別這樣寫！
// 正確做法：
if (fabs(x - 0.3) < 1e-9)

// 問題 2：大數吃小數
double x = 1e10;
double y = 1e-10;
double z = x + y;
// z 的值等於 x！y 被吃掉了

// 問題 3：累積誤差
double sum = 0;
for (int i = 0; i < 1000000; i++)
    sum += 0.000001;
// sum ≠ 1.0（累積誤差不斷擴大）
```

---

## Topic 2: C for Computer Scientists（C 記憶體管理）⭐⭐⭐

### C vs Python 的關鍵差異
```
Python：
  - 自動記憶體管理（Garbage Collection）
  - 沒有指標概念
  - 陣列大小自動調整

C：
  - 手動記憶體管理（malloc/free）
  - 指標（Pointer）是核心概念
  - 陣列大小固定
  - 沒有邊界檢查
```

### C 指標（Pointer）
```c
// 指標的基本概念
int x = 42;
int *p = &x;  // p 儲存 x 的位址

printf("%d
", *p);  // 輸出：42（dereference）

// 常見指標操作
int arr[5] = {1, 2, 3, 4, 5};
int *p = arr;      // p 指向 arr[0]
p++;               // p 指向 arr[1]
printf("%d
", *p);  // 輸出：2

// 指標算術
// p + n 表示記憶體位址前進 n 個元素大小
char *pc = (char *)p;  // 轉型為 char*，每次前進 1 byte
```

### C 記憶體佈局
```
高位址：
┌─────────────────┐
│     Stack       │ ← 本地變數、函數參數（向下生長）
├─────────────────┤
│      ↓          │
│                  │
│      ↑          │
├─────────────────┤
│      Heap       │ ← malloc/free 管理（向上生長）
├─────────────────┤
│  Uninitialized  │ ← BSS（未初始化全域變數）
├─────────────────┤
│   Initialized    │ ← Data（初始化全域變數）
├─────────────────┤
│     Text         │ ← 程式碼（唯讀）
└─────────────────┘
低位址
```

### malloc 和 free
```c
#include <stdlib.h>

// 動態配置記憶體
int *arr = (int *)malloc(10 * sizeof(int));  // 配置 10 個 int
if (arr == NULL) {
    // 配置失敗處理
}

// 使用陣列
for (int i = 0; i < 10; i++) {
    arr[i] = i * i;
}

// 釋放記憶體
free(arr);
arr = NULL;  // 避免 use-after-free

// 常見錯誤：
// 1. 忘記 free（記憶體洩漏）
// 2. free 後繼續使用（use-after-free）
// 3. 雙重 free（double free）
// 4. 只釋放部分（記憶體碎片）

// calloc：配置並初始化為零
int *arr2 = (int *)calloc(10, sizeof(int));

// realloc：調整已配置記憶體大小
int *arr3 = (int *)realloc(arr2, 20 * sizeof(int));
```

---

## Topic 3: RISC-V 指令集架構 ⭐⭐⭐

### 為什麼學 RISC-V？
```
RISC-V 的優點：
  ✓ 開放原始碼（無授權費用）
  ✓ 簡單整潔（比 ARM、x86 簡單得多）
  ✓ 模組化設計（可擴展）
  ✓ 現代化設計（沒有歷史包袱）
  ✓ 越來越多硬體支援（蘋果、高通、西部數据）

RISC-V vs ARM：
  - ARM 需要授權費
  - RISC-V 完全免費
  - 兩者都是 RISC（精簡指令集）
```

### RISC-V 核心指令

**1. 算術指令（R-type）：**
```c
// 加法
add x5, x6, x7    // x5 = x6 + x7
addi x5, x6, 10    // x5 = x6 + 10（立即數）

// 減法
sub x5, x6, x7    // x5 = x6 - x7

// 乘法/除法需要 M 擴展
mul x5, x6, x7    // x5 = x6 * x7
div x5, x6, x7    // x5 = x6 / x7
```

**2. 載入/儲存指令（I-type / S-type）：**
```c
// 載入（記憶體 → 暫存器）
lw x5, 0(x6)      // x5 = Mem[x6 + 0]
lbu x5, 0(x6)     // x5 = Mem[x6 + 0]（unsigned byte）

// 儲存（暫存器 → 記憶體）
sw x5, 0(x6)      // Mem[x6 + 0] = x5
sb x5, 0(x6)      // Mem[x6 + 0] = x5（byte）
```

**3. 分支指令（SB-type）：**
```c
// 條件分支
beq x5, x6, label   // if (x5 == x6) goto label
bne x5, x6, label   // if (x5 != x6) goto label
blt x5, x6, label   // if (x5 < x6) goto label（signed）
bltu x5, x6, label  // if (x5 < x6) goto label（unsigned）
bge x5, x6, label   // if (x5 >= x6) goto label

// 無條件跳躍
jal x1, label       // x1 = PC + 4; goto label（跳並返回）
jalr x1, 0(x2)      // x1 = PC + 4; goto x2（跳至暫存器位址）
```

**4. 邏輯指令：**
```c
and x5, x6, x7      // x5 = x6 & x7
andi x5, x6, 0xFF   // x5 = x6 & 0xFF
or  x5, x6, x7      // x5 = x6 | x7
xor x5, x6, x7      // x5 = x6 ^ x7

// 移位
sll x5, x6, 2       // x5 = x6 << 2（邏輯左移）
srl x5, x6, 2       // x5 = x6 >> 2（邏輯右移）
sra x5, x6, 2       // x5 = x6 >> 2（算術右移，保留符號）
```

### Venus（RISC-V 模擬器）
```
Venus 是 CS61C 使用的線上 RISC-V 模擬器：
  https://venus.cs61c.org/

功能：
  - 逐行執行 RISC-V 指令
  - 顯示暫存器值
  - 顯示記憶體內容
  - 視覺化電路
```

---

## Topic 4: RISC-V 5-Stage Pipeline（管線化）⭐⭐⭐

### 為什麼需要管線化？
```
不使用管線（單一週期）：
  指令 1：|---IF---|---ID---|---EX---|---MEM---|---WB---|--->
  指令 2：          |---IF---|---ID---|---EX---|---MEM---|---WB---|--->
  總時脈數（N 指令）：5N 週期

使用管線：
  指令 1：|---IF---|---ID---|---EX---|---MEM---|---WB---|--->
  指令 2：       |---IF---|---ID---|---EX---|---MEM---|---WB---|--->
  指令 3：              |---IF---|---ID---|---EX---|---MEM---|---WB---|--->
  總時脈數（N 指令）：5 + N 週期 ≈ N 週期

加速比：理想狀況下提升約 5 倍！
```

### 5 個管線階段
```
Stage 1: IF（Instruction Fetch）
  - 從指令記憶體讀取指令
  - 更新 PC

Stage 2: ID（Instruction Decode）
  - 讀取暫存器
  - 解碼指令
  - 產生立即數

Stage 3: EX（Execute）
  - ALU 執行
  - 位址計算
  - 分支判斷

Stage 4: MEM（Memory Access）
  - 資料記憶體讀寫（僅 lw/sw）

Stage 5: WB（Write Back）
  - 結果寫回暫存器檔案
```

### 管線冒險（Hazards）

**1. 結構冒險（Structural Hazard）：**
```
問題：兩個指令同時需要同一個硬體資源
解決：分開指令記憶體和資料記憶體（Harvard Architecture）
```

**2. 資料冒險（Data Hazard）：**
```
問題：一個指令需要前一個指令的結果，但尚未寫回

三種解決方案：
  a. 轉發（Forwarding / Bypassing）：
     從 EX/MEM 或 MEM/WB 流水準直接轉給需要的地方

  b. 載入延遲槽（Load Delay Slot）：
     lw 後的指令不能使用 lw 的結果（需要 1 個 NOP）

  c. 程式碼排序（Scheduling）：
     編譯器重排指令，避免依賴
```

**3. 控制冒險（Control Hazard）：**
```
問題：分支指令在 ID 階段才知道是否跳躍

解決方案：
  a. 假設不跳躍（Assume not taken）：
     預測錯誤時清除管線（3 個指令被丟棄）

  b. 延遲分支（Delayed Branch）：
     在分支後執行一個不影響結果的指令

  c. 動態分支預測（Dynamic Branch Prediction）：
     使用 BHT（Branch History Table）
     2-bit predictor 準確率 > 90%
```

---

## Topic 5: Caches（快取）⭐⭐⭐

### 為什麼需要快取？
```
問題：CPU 和記憶體速度差距極大
  - CPU 指令：~1 ns
  - DRAM 存取：~100 ns
  - 差距：100 倍！

解決方案：加入快取（Cache）
  - SRAM：比 DRAM 快但貴（用在 L1/L2/L3 快取）
  - L1 快取：~1 ns，幾 KB
  - L2 快取：~5 ns，幾百 KB
  - L3 快取：~10 ns，幾 MB
```

### 快取查詢流程
```
CPU 要讀取位址 0x1234 的資料：

Step 1：計算 Index 和 Tag
  假設：
    Offset bits = 6（64-byte blocks）
    Index bits = 4（16 cache lines）
    Tag bits = 22

  Index = 0011（3）
  Offset = 010100（20）

Step 2：查詢快取
  - 讀取 cache line 3
  - 檢查 Valid bit
  - 比較 Tag
  - 如果匹配，讀取 Offset 位置

Step 3：命中（Hit）或 未命中（Miss）
  Hit：直接返回（~1 ns）
  Miss：從主記憶體讀取（~100 ns）並寫入快取
```

### 快取未命中（Cache Miss）

**三種類型：**
```
1. Compulsory Miss（強制未命中）：
   - 第一次存取某個 block

2. Capacity Miss（容量未命中）：
   - 快取容量不足以容納所有存取的 blocks

3. Conflict Miss（衝突未命中）：
   - 直接映射快取中，多個 blocks 競爭同一個位置
```

### 快取效能分析
```
平均記憶體存取時間（AMAT）：
  AMAT = Hit Time + Miss Rate × Miss Penalty

範例：
  L1 Hit Time = 1 cycle
  L1 Miss Rate = 5%
  L2 Miss Penalty = 10 cycles
  L2 Miss Rate = 20%

  L1 AMAT = 1 + 0.05 × 10 = 1.5 cycles

  如果 L2：
  AMAT = 1 + 0.05 × (10 + 0.2 × 100)
       = 1 + 0.05 × 30
       = 2.5 cycles
```

### 快取友好程式設計
```
好：順序走訪陣列
```c
// 快取友好（Sequential）
for (int i = 0; i < N; i++)
    sum += arr[i];  // 每次讀取下一個元素（空間局部性）
```

壞：跳躍式存取
```c
// 快取不友好（Strided）
for (int i = 0; i < N; i++)
    sum += arr[i * stride];  // stride > 1 時效率差
```

範例：矩陣乘法（Blocking 技巧）
```c
// 慢版本
for (int i = 0; i < N; i++)
    for (int j = 0; j < N; j++)
        for (int k = 0; k < N; k++)
            C[i][j] += A[i][k] * B[k][j];

// 快版本（block optimization）
for (int i = 0; i < N; i += BLOCK)
    for (int j = 0; j < N; j += BLOCK)
        for (int k = 0; k < N; k += BLOCK)
            // 小區塊操作，充分利用快取
```

Blocking 技巧：
  - 將大矩陣分成小區塊
  - 每個區塊大小 ≈ L1 快取大小
  - 大量減少 cache miss
```

---

## Topic 6: Virtual Memory（虛擬記憶體）⭐⭐⭐

### 虛擬記憶體的概念
```
問題：
  1. 多個程式共享記憶體，如何隔離？
  2. 程式需要比實際記憶體更大的空間？
  3. 如何保護程式不被其他程式影響？

虛擬記憶體解決方案：
  - 每個程式有自己的虛擬位址空間
  - 硬體（MMU）將虛擬位址翻譯為實體位址
  - 作業系統負責管理頁表

虛擬位址的好處：
  ✓ 隔離：每個程式看不到其他程式的記憶體
  ✓ 簡化：程式可以使用連續的虛擬位址
  ✓ 保護：無法存取未授權的頁
  ✓ 可擴展：可用比實體記憶體更大的虛擬空間
```

### 分頁（Paging）
```
虛擬位址格式（32-bit，4KB 頁）：
  ┌────────────────────┬──────────┐
  │  Virtual Page #     │ Offset  │
  │      20 bits        │  12 bits │
  └────────────────────┴──────────┘

頁表（Page Table）：
  - 每個程式有自己的頁表
  - 映射：Virtual Page Number → Physical Page Number
  - 額外資訊：Valid bit, Protection bits, Dirty bit
```

### TLB（Translation Lookaside Buffer）
```
TLB 查找流程：
  1. 用 VPN 查 TLB
  2. 如果命中：直接得到 PFN，存取記憶體
  3. 如果未命中：查頁表，更新 TLB

TLB 效能：
  - TLB Hit Rate：通常 > 95%
  - TLB Miss Penalty：10-100 cycles
```

### 分頁替換策略
```
LRU（Least Recently Used）：
  - 移除最久未使用的條目

Clock Algorithm（時鐘演算法）：
  - 近

似 LRU
  - 每個條目有一個 reference bit
  - 掃描：如果 bit=1，清除；找到第一個 bit=0，替換
```

### 置換代價與 Thrashing
```
一次 Page Fault 的代價：
  - 磁碟 I/O：~10ms = 10,000,000 cycles（極慢！）

工作集模型（Working Set）：
  - 每個程式有一段時間內會頻繁存取的頁集合
  - 如果工作集能放入實體記憶體，幾乎不會有 Page Fault
  - 否則會不斷置換（Thrashing）
```

### Segmentation Fault
```
Segmentation Fault 的原因：
  1. 存取未映射的虛擬位址
  2. 存取沒有權限的頁（唯讀頁寫入）
  3. 無效的指標（NULL 指標、已釋放記憶體）
```

---

## Topic 7: Parallelism（平行運算）⭐⭐⭐

### 平行的四個層次
```
1. Bit-Level Parallelism（位元層平行）
   - 增加 CPU 位元寬度（8→16→32→64）

2. Instruction-Level Parallelism（ILP）
   - 管線化（Pipeline）
   - 超純量（Superscalar）
   - 亂序執行（Out-of-Order Execution）

3. Data-Level Parallelism（DLP）
   - SIMD（Single Instruction Multiple Data）
   - 向量化（Vectorization）

4. Thread-Level Parallelism（TLP）
   - 多執行緒
   - 多核心
   - 多處理器
```

### SIMD（單一指令多資料）
```
範例：向量加法
  Without SIMD：
    for (int i = 0; i < N; i++)
        C[i] = A[i] + B[i];  // N 次加法

  With SIMD（128-bit AVX，一次 4 個 32-bit）：
    for (int i = 0; i < N; i += 4)
        C[i:i+3] = A[i:i+3] + B[i:i+3];  // N/4 次加法

SIMD Extensions：
  - SSE：128-bit（4 × 32-bit floats）
  - AVX：256-bit（8 × 32-bit floats）
  - AVX-512：512-bit（16 × 32-bit floats）
  - NEON：ARM 的 SIMD（64/128-bit）
```

### Amdahl's Law（阿姆達爾定律）
```
Speedup = 1 / (S + (1-S)/N)

其中：
  S = 不可平行化的部分比例
  N = 核心數

範例：
  如果 10% 的程式無法平行化（S=0.1）：
    N=1:  Speedup = 1.0
    N=2:  Speedup = 1.82
    N=4:  Speedup = 3.08
    N=8:  Speedup = 4.71
    N=∞:  Speedup = 10（最大）

結論：
  不可平行化的部分越大，平行化的收益越小
```

---

## Topic 8: 多執行緒並行
```
pthread 範例：
```c
#include <pthread.h>

void *worker(void *arg) {
    int id = *(int *)arg;
    printf("Thread %d
", id);
    return NULL;
}

int main() {
    pthread_t threads[4];
    int ids[4] = {0, 1, 2, 3};

    for (int i = 0; i < 4; i++)
        pthread_create(&threads[i], NULL, worker, &ids[i]);

    for (int i = 0; i < 4; i++)
        pthread_join(threads[i], NULL);

    return 0;
}
```

並行的問題：
  1. 競爭條件（Race Condition）→ 需要互斥鎖（Mutex）
  2. 死結（Deadlock）→ 避免循環等待
  3. 假的共享（False Sharing）
     → 不同執行緒修改同一快取行的不同變數
```

---

## 💡 工程師蘇茉的 CS61C 學習心得

### 為什麼選電腦結構？
```
已完成：
  Session 3: MIT 6.006 演算法基礎
  Session 4: MIT 6.046 進階演算法設計
  Session 5: MIT 6.5840 分散式系統
  Session 6: MIT 6.1810 作業系統
  Session 7-8: MIT 6.5840 分散式深入
  Session 9: Computer Networks

為什麼需要電腦結構知識？
  1. 理解程式的執行底層：為什麼這個程式慢？
  2. 效能優化：快取命中 vs 未命中的差異可以達到 100 倍
  3. 嵌入式系統：物聯網、微控制器直接操作硬體
  4. 面試高頻：虛擬記憶體、管線衝突、快取置換
  5. 理解現代電腦的局限：為什麼多執行緒不一定更快？
```

### 面試高頻 CS61C 問題
```
1. 什麼是 cache miss？有哪些類型？
   → Compulsory / Capacity / Conflict Miss

2. Cache 的 write-through 和 write-back 的差異？
   → 前者同步寫記憶體，後者延遲寫入

3. 虛擬記憶體和快取的區別？
   → VM 是 OS/硬體支持的位址翻譯，Cache 是硬體加速

4. TLB 的作用？如何減少 TLB miss？
   → Translation Lookaside Buffer，硬體快取翻譯結果

5. 什麼是 Amdahl's Law？
   → 平行化加速比的上限由不可平行部分決定

6. 單一週期 vs 管線化 CPU 的差異？
   → 前者每指令 1 個時脈，後者多指令同時執行

7. 為什麼需要 pipeline hazard？如何解決？
   → 結構/資料/控制冒險，轉發/停頓/預測

8. 什麼是 false sharing？如何避免？
   → 不同執行緒修改同一快取行，padding 或 thread-local
```

### 實務應用場景
```
高效能計算（HPC）：
  - 理解 SIMD 才能寫出高效的數值計算
  - 理解記憶體階層才能減少 cache miss

嵌入式系統：
  - RISC-V 是物聯網裝置的未來
  - 理解 interrupt、memory-mapped I/O

資料庫系統（與 CMU 15-445 連結）：
  - Buffer Pool 管理就是大號的快取
  - O_DIRECT 繞過 OS 快取，直接 I/O
  - 理解虛擬記憶體才能理解記憶體映射檔

分散式系統（與 MIT 6.5840 連結）：
  - NUMA（Non-Uniform Memory Access）
  - 快取一致性（Cache Coherence）協定
  - RDMA（Remote Direct Memory Access）
```

### CS61C vs MIT 6.004/6.1810
```
MIT 6.004（計算機結構）：
  - 理論導向：數位邏輯、狀態機、組合電路

MIT 6.1810（作業系統）：
  - 系統程式：行程管理、記憶體管理、檔案系統

CS61C（電腦結構）：
  - 軟體視角：理解硬體如何影響軟體效能
  - RISC-V：開放原始碼的現代 ISA
  - 實作導向：Venus 模擬器、Logisim CPU 設計

三者互補：
  CS61C 告訴你「硬體是什麼」
  6.1810 告訴你「作業系統如何管理硬體」
  兩者合在一起才能設計高效系統
```

---

## 📅 後續學習計畫

```
Q2 2026:
  □ 完成 CS61C Labs（Venus RISC-V 程式設計）
  □ 用 Logisim 設計一個簡單的 5-stage pipeline CPU
  □ 實作矩陣乘法的 SIMD 向量化優化

Q3 2026:
  □ 研究 RISC-V 生態系（SiFive、阿里平頭哥）
  □ 研究 GPU 架構（CUDA vs OpenCL）
  □ 理解 NUMA 和 Cache Coherence（MESI 協定）

Q4 2026:
  □ 硬體加速器設計（FPGA、HLS）
  □ 量子計算機的基礎（Qubit vs Bit）
```

---

*本筆記由工程師蘇茉於 2026-04-05 整理自 CS61C Spring 2026 UC Berkeley 課程*
*學習次數：第10次（電腦結構 / RISC-V 專題）*
