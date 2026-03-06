# Advanced Data Structures

## Splay Tree

Splay tree is a self-adjusting BST. After access (search, insert), the node is moved to root via splay operation. Zig, zig-zig, zig-zag rotations. Amortized O(log n) per operation. No explicit balance info stored. Locality: frequently accessed nodes stay near root. Used in caches, Windows NT virtual memory.

## Treap (Tree + Heap)

Treap combines BST (by key) and heap (by random priority). Each node has key and priority. Insert: add at leaf, rotate up to satisfy heap. Expected O(log n) height. No rotations for balance; randomness provides balance. Supports split and merge in O(log n). Used when random insertions.

## B+ Tree

B+ tree is B-tree variant for databases. All data in leaves; internal nodes are indexes. Leaves linked for range scans. Order m: internal nodes have m children, m-1 keys. Used in MySQL, PostgreSQL, file systems. Excellent for disk: few disk reads, high fanout.

## B* Tree

B* tree variant with 2/3 full minimum instead of 1/2. Reduces splits by redistributing to siblings first. Better space utilization. Used in some file systems.

## R-Tree

R-tree indexes spatial data (rectangles, polygons). Nodes have minimum bounding rectangles (MBR). Insert: find leaf with minimum area increase. Split when full. Used for geographic data, CAD, GIS. Variants: R+ tree, R* tree.

## k-d Tree

k-d tree partitions k-dimensional space. Each level splits on one dimension. Build: O(n log n). Range query: O(sqrt(n) + k) for k results. Nearest neighbor: O(log n) average. Used for spatial indexing, nearest neighbor search.

## Interval Tree

Interval tree stores intervals, supports overlap query. Each node stores interval and max endpoint in subtree. Query overlapping interval: O(log n + k). Used for scheduling, computational geometry.

## Segment Tree with Lazy Propagation

Lazy propagation defers range updates. Store pending update in node; apply when querying or splitting. Range add: O(log n). Range sum query: O(log n). Must push lazy values to children when needed. Used for range update, range query problems.

## Fenwick Tree (Binary Indexed Tree)

Fenwick tree supports prefix sum and point update in O(log n). Uses binary representation: each index stores sum of range. Less memory than segment tree. Update: add to index and its "parents". Query: sum from 1 to index. Cannot do range update directly (use difference array).

## Cuckoo Hashing

Cuckoo hashing uses two hash tables and two hash functions. Insert: if slot occupied, evict and reinsert evicted item. May need rehashing if cycle. Lookup: O(1) worst case. Delete: O(1). No clustering. Used when worst-case lookup matters.

## Cuckoo Filter

Cuckoo filter is Bloom filter alternative. Supports deletion. Uses cuckoo hashing with compact fingerprints. False positive rate tunable. Space efficient. Used in databases, caches.

## Count-Min Sketch

Count-Min Sketch estimates frequency counts. Uses d hash functions and w counters. Add: increment d counters. Query: return minimum of d counters. Overestimates; never underestimates. Used for heavy hitters, approximate counting.

## HyperLogLog

HyperLogLog estimates cardinality (unique count) of huge sets. Uses O(log log n) memory. Based on maximum leading zeros in hashed values. Standard error about 0.81%. Used in Redis, analytics.

## Suffix Array

Suffix array: sorted array of all suffixes. Build: O(n log n) with doubling. Search: O(m log n) with binary search. LCP array: longest common prefix between adjacent suffixes. Used for pattern matching, genomics.

## Suffix Tree

Suffix tree: compressed trie of all suffixes. Build: O(n) with Ukkonen's algorithm. Search: O(m). Space: O(n). Supports many string queries. Used in bioinformatics, text indexing.

## Suffix Automaton

Suffix automaton (DAWG): minimal automaton accepting all suffixes. Linear size. Build: O(n). Applications: substring count, longest common substring. Alternative to suffix tree.

## Cartesian Tree

Cartesian tree: binary tree from array. Root is min (or max) in range. Left subtree from left subarray, right from right. Build: O(n) with stack. Used for range minimum query, convert to treap.

## Pairing Heap

Pairing heap: simple heap with amortized O(1) insert, merge, decrease-key. Extract-min: O(log n) amortized. Simpler than Fibonacci heap. Used in practice for some graph algorithms.

## Fibonacci Heap

Fibonacci heap: heap with O(1) amortized insert, merge, decrease-key. O(log n) amortized extract-min. Lazy consolidation. Used in theoretical Dijkstra. Complex to implement.

## Van Emde Boas Tree

Van Emde Boas tree supports integer operations in O(log log M) where M is universe size. Insert, delete, search, predecessor, successor. Requires M to be known. Used for small integer universes.

## Scapegoat Tree

Scapegoat tree: balanced BST with no rotations during insert. When imbalance exceeds threshold, rebuild subtree. O(log n) amortized. Simpler than red-black. Self-balancing through rebuilding.

## Weight-Balanced Tree (BB Tree)

BB tree maintains balance through weight (subtree size) ratio. Alpha: 0.25 to 0.5. Rebalance when weight ratio exceeds threshold. Used in functional programming (Data.Set in Haskell).

## 2-3 Tree

2-3 tree: each node has 2 or 3 children. All leaves at same level. Insert: add to leaf, split if 4 children. Delete: merge or borrow. O(log n) operations. Precursor to B-tree.

## 2-3-4 Tree

2-3-4 tree: nodes have 2, 3, or 4 children. Simpler than red-black; red-black is equivalent. Used in some textbooks.

## Radix Tree

Radix tree (compact prefix tree): compressed trie where nodes with single child are merged. Saves space. Used in IP routing, memory management.

## Crit-bit Tree

Crit-bit tree: binary radix tree. Each node stores critical bit position. O(k) operations where k is key length. Used in routing tables.

## Hash Array Mapped Trie (HAMT)

HAMT: persistent hash trie. Each level uses 32-bit bitmap and array. O(log n) depth for n elements. Used in Clojure, Scala for immutable maps.

## Rope

Rope: tree for large strings. Leaves are short strings. Concatenate: O(1). Insert: O(log n). Avoids copying for large strings. Used in text editors.

## Skip List

Skip list: probabilistic multi-level linked list. Level 0: all elements. Level i: random subset. Search: O(log n) expected. Insert: O(log n) expected. Simple alternative to balanced trees. Used in Redis.

## Unrolled Linked List

Unrolled linked list: each node stores multiple elements. Reduces pointer overhead. Cache-friendly. Trade-off between array and linked list.

## XOR Linked List

XOR linked list: each node stores XOR of prev and next addresses. Doubly linked list in half the space. Traversal requires knowing previous or next. Rarely used.

## Circular Buffer

Circular buffer: fixed-size array with head and tail pointers. Wrap-around indexing. O(1) enqueue, dequeue. Used for streaming, producer-consumer.

## Disjoint Set Union (DSU)

DSU with path compression and union by rank: O(α(n)) amortized. α is inverse Ackermann, effectively constant. Used for connectivity, graph algorithms.

## Persistent Data Structures

Persistent structures: retain previous versions. Copy-on-write. Path copying for trees. Used in functional programming, version control.

## Implicit Data Structure

Implicit structure: stored in array without explicit pointers. Implicit heap: array indices encode parent-child. Saves space.
