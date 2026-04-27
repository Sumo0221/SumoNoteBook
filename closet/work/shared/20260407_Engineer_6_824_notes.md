# MIT 6.824 / 6.5840 - Distributed Systems（分散式系統）

**學習日期：** 2026-04-05
**課程來源：** https://github.com/Developer-Y/cs-video-courses
**官方網站：** https://pdos.csail.mit.edu/6.824/
**當前版本：** MIT 6.5840 (Spring 2026)

---

## 📚 課程概覽

MIT 6.824 是 MIT 最著名的分散式系統課程，核心主題：
- **Fault Tolerance（容錯）**
- **Replication（複製）**
- **Consistency（共識）**

**授課形式：** 論文閱讀 + 程式實驗 Lab（使用 Go 語言）

**前置知識：**
- 6.004（計算機組成）
- 6.033（電腦網路）或同等學歷
- 紮實的程式開發經驗

---

## 🔥 Topic 1: 分散式系統的挑戰

### 為什麼需要分散式系統？
```
單機瓶頸：
  - 效能上限受限於單機硬體
  - 儲存容量有限
  - 沒有硬碟擴展能力（Scale-up 有上限）

分散式解法：
  ✓ 水平擴展（Scale-out）：加機器就能提升效能
  ✓ 更高的可用性（Fault Tolerance）
  ✓ 更大的儲存容量

代價：
  ✗ 網路延遲（Network Latency）
  ✗ 網路分割（Network Partition）
  ✗ 機器故障（Machine Failure）
  ✗ Clock Skew（時鐘不同步）
```

### 分散式系統的8個失敗點（Fallacies of Distributed Computing）
```
1. 網路是可靠的（The network is reliable）
2. 延遲為零（Latency is zero）
3. 頻寬是無限的（Bandwidth is infinite）
4. 網路是安全的（The network is secure）
5. 拓樸不會變（Topology doesn't change）
6. 只有一個管理員（There is one administrator）
7. 傳輸成本為零（Transport cost is zero）
8. 網路是同質的（The network is homogeneous）
```

### 工程師心法
```
分散式系統的核心矛盾：
  「我們希望系統像單機一樣運作，
   但現實是網路會延遲、機器會當機、資料會不一致」

所有分散式系統的設計，都是在：
  Consistency（一致性）、Availability（可用性）、
  Partition Tolerance（分割容忍）三者之間取捨
  → CAP Theorem
```

---

## 🔥 Topic 2: MapReduce（經典分散式計算框架）

### 什麼是 MapReduce？
Google 在 2004 年提出的分散式資料處理模型，用於大規模資料集的並行計算。

### 核心思想：分而治之（Divide and Conquer）
```
Input → Map（映射）→ Shuffle（分組）→ Reduce（歸納）→ Output

Map 階段：
  - 每個 worker 處理輸入的一部分
  - 輸出 (key, value) 對

Shuffle 階段：
  - 將相同 key 的 value 聚合在一起
  - 網路傳輸：跨機器的資料重新分組

Reduce 階段：
  - 每個 worker 處理一個 key 的所有 value
  - 產生最終輸出
```

### Word Count 範例（經典 MapReduce 程式）
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

// Reduce 函數：將相同 key 的 count 相加
func reduceFun(key string, values []string) string {
    return strconv.Itoa(len(values))
}
```

### MapReduce 的 Fault Tolerance 設計
```
Master 追蹤每個 Map/Reduce worker 的狀態：
  - 如果 Map worker 失敗：重新執行該 task
  - 如果 Reduce worker 失敗：重新執行該 task

重要：Map 的輸出存在本地磁碟，Reduce 任務完成後就刪除
      → 支援任務重執行，不需要重複整個 job
```

### 工程師觀點
```
MapReduce 的貢獻：
  - 讓不懂分散式系統的工程師也能寫平行運算
  - 隱藏了網路通訊、負載平衡、失敗處理

限制：
  - 適合「簡單的 key-value 聚合」
  - 不適合需要「跨記錄狀態」或「迭代」的任務
  → 催生了 Spark、Flink 等更進階的引擎
```

---

## 🔥 Topic 3: RAFT 共識演算法（一致性核心）⭐⭐⭐

### 為什麼需要共識演算法？
```
分散式系統的核心問題：
  - 多個副本（replica）如何保持資料一致？
  - 當有機器故障時，如何繼續運作？
  - 如何確保只有一個副本接受寫入？

共識演算法（Consensus Algorithm）的目標：
  讓一群機器就「某個值」達成一致的決定

代表作品：
  - Paxos（ Leslie Lamport，1998）
  - Raft（Diego Ongaro & John Ousterhout，2014）
```

### RAFT 的核心設計目標
```
1. Understandability（可理解性）← Raft 的主要貢獻
2. 沒有歧義的實現
3. 有效的 leader election

Raft 將問題分解為三個相對獨立的子問題：
  1. Leader Election（領導者選舉）
  2. Log Replication（日誌複製）
  3. Safety（安全性）
```

### RAFT 三種角色
```
1. Follower（追隨者）：
   - 被動接收來自 leader 的心跳和日誌
   - 如果超時沒收到心跳，轉為 Candidate

2. Candidate（候選者）：
   - 向其他伺服器發起投票請求
   - 獲得多數票則成為新 Leader

3. Leader（領導者）：
   - 處理所有客戶端請求
   - 發送心跳保持領導地位
   - 複製日誌到 followers
```

### Leader Election（領導者選舉）
```
選舉流程：
  1. Follower 等待 heartbeat 超時（通常 150-300ms）
  2. 轉為 Candidate，增加 currentTerm
  3. 投票給自己
  4. 向所有伺服器發送 RequestVote RPC
  5. 如果獲得多數票，成為 Leader

重要：每個任期（Term）最多只有一個 Leader
重要：機器投票給「日誌比自己新」的 Candidate
```

### Log Replication（日誌複製）
```
Leader 的職責：
  1. 接收客戶端請求（命令）
  2. 將命令追加到本地日誌
  3. 發送 AppendEntries RPC 給 followers
  4. 等待多數派確認
  5. 套用命令到狀態機，返回客戶端

日誌結構：
  Entry = {term, index, command}
  
  ┌─────────────────────────────────────────────┐
  │  Term  │  Index  │        Command            │
  ├────────┼─────────┼───────────────────────────┤
  │   1    │    1    │  SET x = 5                │
  │   1    │    2    │  SET y = 3                │
  │   2    │    3    │  SET x = 7                │  ← Leader
  │   2    │    4    │  SET z = 2                │
  └─────────────────────────────────────────────┘
```

### RAFT vs Paxos（工程師比較）
```
Paxos：
  - 理論基礎扎實，但極難理解和實現
  - 只有單一決策（single-decree Paxos）
  - 生產實現往往偏離論文

Raft：
  - 強調可理解性
  - 分解清晰，易於實現
  - 實際系統採用廣泛（etcd, CockroachDB, TiKV, Consul）

業界採用 Raft 的系統：
  - etcd（Kubernetes 的分散式 key-value store）
  - TiKV（TiDB 的儲存引擎）
  - CockroachDB
  - Consul
```

---

## 🔥 Topic 4: Go 語言併發模式（分散式系統實戰）

### 為什麼分散式系統用 Go？
```
Go 的三大殺手鐧：
  1. Goroutine：輕量級執行緒，開啟數十萬個不費力
  2. Channel：goroutine 間的安全通訊機制
  3. 簡單的語法：比 C++/Java 更適合系統程式
```

### 併發版 Word Count（MapReduce 概念）
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
  - 保護共享的「狀態」
  - 適合讀寫不平衡的場景
  - 例子：計數器、快取

Channel：
  - 適合「事件傳遞」或「pipeline」
  - 適合「任務分發」
  - 例子：工作者池、生產者-消費者
```

---

## 🔥 Topic 5: 複製與一致性（Replication & Consistency）

### 一致性模型光譜
```
強一致性（Strong Consistency）：
  - 讀取總是看到最新的寫入
  - 代價：效能差、可用性低
  - 例子：Strict Serializability

順序一致性（Sequential Consistency）：
  - 所有客戶端看到相同的操作順序
  - 例子：多執行緒程式的記憶體順序

因果一致性（Causal Consistency）：
  - 只保證有因果關係的操作順序
  - 例子：社群媒體的「回覆」功能

最終一致性（Eventual Consistency）：
  - 不保證何時一致，最終會一致
  - 代價：客戶端可能讀到過期資料
  - 例子：DynamoDB, Cassandra
```

### CAP Theorem（布爾斯定理）
```
分散式系統不可能同時滿足三者：
  1. Consistency（一致性）
  2. Availability（可用性）
  3. Partition Tolerance（分割容忍）

只能同時滿足兩者：
  - CA（不可能存在）：不放棄 P
  - CP（一致性 + 分割容忍）：網路分割時犧牲可用性
  - AP（可用性 + 分割容忍）：網路分割時犧牲一致性

實際系統的選擇：
  - CP：ZooKeeper, etcd, HBase
  - AP：DynamoDB, Cassandra, CouchDB
```

---

## 🔥 Topic 6: GFS（Google File System）- 大規模分散式儲存

### GFS 的設計假設
```
Google 在 2003 年提出的分散式檔案系統：
  - 大量 commodity hardware（低價硬體）
  - 檔案很大（GB 等級）
  - 主要讀取模式：大量順序讀、少量隨機讀
  - 需要高度容忍硬體故障
```

### GFS 架構
```
                    ┌─────────────┐
                    │   Master    │  ← 單一 Master（元資料管理）
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
         ┌────▼───┐  ┌────▼───┐  ┌────▼───┐
         │ChunkServer│ │ChunkServer│ │ChunkServer│
         │   (1)   │  │   (2)   │  │   (3)   │
         └─────────┘  └─────────┘  └─────────┘

特點：
  - 每個檔案切成固定大小的 chunk（64MB）
  - 每個 chunk 在多個 chunkserver 上複製（預設 3 份）
  - Master 儲存元資料（檔案名稱、chunk 位置）
```

### GFS 的 Fault Tolerance
```
Chunk Server 故障：
  - Master 偵測到心跳中斷
  - 在其他 chunkserver 上重新複製 chunks
  - 維持預設的複製因子（replication factor）

Master 故障：
  - 單點故障（Single Point of Failure）← GFS 的主要詬病
  - 後續 Colossus（Google 內部）改進了這一點
```

---

## 🔥 Topic 7: Spanner（全球分散式資料庫）

### Spanner 的突破
```
Google 的全球分散式關聯式資料庫：
  - 可擴展至數百萬台機器
  - 全球分布（跨資料中心、跨 region）
  - 提供強一致性（外部一致性）
  - 使用 TrueTime API 實現跨地域同步
```

### TrueTime（時鐘同步）
```
問題：分散式系統中，不同機器的時鐘會有偏差（Clock Skew）

TrueTime 解法：
  - 使用 GPS 接收器 + 原子鐘
  - 每台伺服器裝備兩種時鐘
  - 提供「不確定性區間」：[earliest, latest]

  ┌─────────────────────────────────────┐
  │  TrueTime API：                    │
  │  TT.now() → TTinterval             │
  │  { earliest: 10:00:00.000,         │
  │    latest:  10:00:00.200 }         │
  └─────────────────────────────────────┘

  每個寫入都有時間戳：TT.now().latest
  讀取時等TT.after(commit_ts)確保可見性
```

---

## 🔥 Topic 8: ZooKeeper（分散式協調服務）

### ZooKeeper 是什麼？
```
分散式系統的「幫手」：
  - 提供分散式鎖
  - 領導者選舉
  - 組態管理
  - 服務發現

使用場景：
  - Kafka叢集的協調（broker 故障監測）
  - HBase 的領導者選舉
  - YARN 的資源管理
```

---

## 💡 工程師蘇茉的學習心得

### 為什麼選 MIT 6.824？
```
作為軟體工程師，分散式系統是必備知識：
  - 所有大型網路服務（Netflix, Google, AWS）都是分散式系統
  - 面試必考：CAP Theorem、RAFT、共識算法
  - 工作必用：Kafka、Redis Cluster、Kubernetes

MIT 6.824 的特色：
  - 論文驅動學習（而非純理論）
  - 有實際的 Go 程式 Lab（不是紙上談兵）
  - 涵蓋現代分散式系統的核心技術
```

### 分散式系統 vs 單機系統的核心差異
```
單機系統：
  ✓ 記憶體共享（直接讀寫共享狀態）
  ✓ 簡單的一致性模型（所有執行緒看到相同狀態）
  ✓ 失敗模式簡單（進程崩潰就直接重啟）

分散式系統：
  ✗ 網路延遲和不可靠
  ✗ 部分機器故障不影響整體
  ✗ 一致性模型複雜（要考慮網路分割）
```

### Lab 實作建議
```
Lab 1: MapReduce（Word Count 並行化）
  → 理解分散式計算的基本範式

Lab 2: Key-Value Server（單機版 Raft KV Store）
  → 為 Lab 3 暖身

Lab 3: Raft（共識演算法實現）
  → 這是 6.824 最難的 Lab
  → 實現 Leader Election 和日誌複製
  → 建議：先讀完 Raft Paper 三遍再開始

Lab 4: Sharded KV Server（多 Raft Group）
  → 將 Raft 擴展到水平擴展

Lab 5: Sharded Backup Server（故障轉移）
  → 加入新伺服器不影響服務
```

### 面試高頻考點
```
1. CAP Theorem：解釋並舉例（CP vs AP 系統）
2. RAFT：
   - 三種角色和轉換
   - Leader Election 流程
   - Log Replication 流程
   - 如何處理網路分割
3. 一致性模型：強一致性、順序一致性、最終一致性
4. 分散式事務：2PC、2PL、Saga
5. Vector Clock：解決事件排序問題
```

### 實務應用場景
```
Kafka / RabbitMQ：
  - 基於日誌的訊息系統
  - Partition + Replication

Redis Cluster：
  - 分散式 Cache
  - Hash slot 分配

Kubernetes：
  - etcd（RAFT 共識）儲存叢集狀態
  - API Server 作為叢集的單一真相來源

Cassandra：
  - AP 系統（可用性 + 分割容忍）
  - LSM Tree 儲存引擎
```

---

## 📅 學習Session記錄

### Session 5（2026-04-05）- MIT 6.824 分散式系統入門

**今日重點：**
- 分散式系統的8大失敗點（Fallacies）
- MapReduce 分散式計算範式
- CAP Theorem（一致性、可用性、分割容忍）
- RAFT 共識演算法（Leader Election + Log Replication）
- Go 語言併發模式（分散式系統實作工具）
- GFS 大規模分散式儲存
- Spanner 全球分散式資料庫
- ZooKeeper 分散式協調服務

**新理解：**
- 分散式系統的本質是在「一致性」和「可用性」之間取捨
- RAFT 將 Paxos 複雜的共識問題分解為三個可理解的部分
- MapReduce 的貢獻不是效能，而是讓「一般工程師」也能寫分散式程式
- TrueTime 的「時鐘不確定性區間」是一個優雅的工程解法

**與之前學習的銜接：**
- 演算法知識（BFS/DFS、Graph）用於分散式系統的拓樸管理
- 併發控制概念（來自作業系統）是理解 RAFT 的基礎

---

## 🔥 後續學習計畫

```
Q2 2026:
  □ 6.824 Labs（完成所有 5 個 Lab）
  □ 閱讀經典論文（BigTable, Dynamo, Cassandra）
  
Q3 2026:
  □ CMU 15-445 Database Systems（資料庫系統）
  □ 實作一個簡單的 Raft KV Store

Q4 2026:
  □ 雲端架構（AWM, GCP, Azure 深入）
  □ 分散式系統面試題強化
```

---

*本筆記由工程師蘇茉於 2026-04-05 整理自 MIT 6.824 / 6.5840 OCW 課程*
*學習次數：第5次（分散式系統專題）*
