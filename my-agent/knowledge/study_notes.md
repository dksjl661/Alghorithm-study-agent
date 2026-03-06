# Data Structures and Algorithms - Complete Knowledge Base

## Recursion

Recursion is a fundamental problem-solving technique where a function calls itself with a smaller or simpler input until it reaches a base case. Every recursive solution requires two key components: a base case (termination condition) and a recursive case (the function calling itself with reduced input). Recursion is particularly elegant for problems that have natural recursive structure, such as tree traversals, divide-and-conquer algorithms, and backtracking.

Recursion matters because it simplifies complex problems by breaking them into smaller, identical subproblems. The call stack implicitly maintains state, eliminating the need for explicit stacks in many algorithms. Time complexity of recursive algorithms is often analyzed using recurrence relations. Space complexity includes the call stack depth, which can be O(n) in the worst case for linear recursion.

```python
# Python - factorial recursion
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

```javascript
// JavaScript - factorial recursion
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}
```

## Recursion in Linked Lists

Recursion matters in linked lists for several important reasons. First, linked lists have a natural recursive structure: a linked list is either empty (base case) or consists of a node pointing to another linked list (recursive case). This structure makes recursion an elegant way to traverse, reverse, or transform linked lists without explicit iteration.

Why recursion matters in linked list: Many operations like reverse, merge, and flatten become simpler and more intuitive when expressed recursively. For example, reversing a linked list recursively: reverse the rest of the list, then make the next node point back to current. The recursive approach often produces cleaner code than iterative solutions with multiple pointers.

Recursion in linked lists also helps with problems like palindrome checking (compare first and last, recurse on middle), finding middle node, and merging two sorted lists. The key insight is that each recursive call operates on a "smaller" list (the remainder), naturally progressing toward the base case of an empty or single-node list.

```python
# Python - recursive linked list reverse
def reverse_list(head):
    if not head or not head.next:
        return head
    new_head = reverse_list(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

```javascript
// JavaScript - recursive linked list reverse
function reverseList(head) {
  if (!head || !head.next) return head;
  const newHead = reverseList(head.next);
  head.next.next = head;
  head.next = null;
  return newHead;
}
```

## Linked List

A linked list is a linear data structure where each element (node) contains a value and a pointer to the next node. Unlike arrays, linked lists do not require contiguous memory; nodes can be scattered. Singly linked lists have one pointer per node; doubly linked lists have prev and next pointers. Circular linked lists connect the last node back to the first.

Operations: Insertion at head O(1), at tail O(n) without tail pointer or O(1) with tail. Deletion O(n) for search plus O(1) for removal. Access by index O(n). Linked lists excel when insertions and deletions are frequent at the beginning, or when the size is unknown and dynamic allocation is needed.

```python
# Python - linked list node and insert at head
class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def insert_head(head, val):
    return Node(val, head)
```

```javascript
// JavaScript - linked list node and insert at head
class Node {
  constructor(val, next = null) {
    this.val = val;
    this.next = next;
  }
}
function insertHead(head, val) {
  return new Node(val, head);
}
```

## Doubly Linked List

A doubly linked list extends the singly linked list by storing both a next and a prev pointer in each node. This allows traversal in both directions and O(1) deletion of a node when you have a reference to it (since you can update both neighbors). Doubly linked lists are used to implement LRU caches, browser history (back/forward), and certain data structures like deque.

```python
# Python - doubly linked list node
class DNode:
    def __init__(self, val, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

def delete_node(node):
    node.prev.next = node.next
    node.next.prev = node.prev
```

```javascript
// JavaScript - doubly linked list node
class DNode {
  constructor(val, prev = null, next = null) {
    this.val = val;
    this.prev = prev;
    this.next = next;
  }
}
function deleteNode(node) {
  node.prev.next = node.next;
  node.next.prev = node.prev;
}
```

## Array

Arrays are contiguous blocks of memory storing elements of the same type. Access by index is O(1). Insertion and deletion in the middle require shifting elements, O(n). Arrays support random access and cache-friendly sequential access. Dynamic arrays (like Python list, C++ vector) resize automatically when capacity is exceeded, with amortized O(1) append.

```python
# Python - array access and operations
arr = [1, 2, 3, 4, 5]
print(arr[2])           # O(1) access
arr.append(6)           # O(1) amortized
arr.insert(0, 0)         # O(n) shift
```

```javascript
// JavaScript - array access and operations
const arr = [1, 2, 3, 4, 5];
console.log(arr[2]);     // O(1) access
arr.push(6);            // O(1) amortized
arr.unshift(0);          // O(n) shift
```

## Stack

A stack is a LIFO (Last In, First Out) data structure. Operations: push (add to top), pop (remove from top), peek (view top), all O(1). Stacks are used for function call management, expression parsing (parentheses matching, infix to postfix), DFS, backtracking, and undo mechanisms. Implement with array or linked list.

```python
# Python - stack with list
stack = []
stack.append(1)         # push
stack.append(2)
top = stack[-1]         # peek
x = stack.pop()         # pop
```

```javascript
// JavaScript - stack with array
const stack = [];
stack.push(1);          // push
stack.push(2);
const top = stack[stack.length - 1];  // peek
const x = stack.pop();   // pop
```

## Queue

A queue is a FIFO (First In, First Out) data structure. Operations: enqueue (add to rear), dequeue (remove from front), both O(1) with proper implementation. Implement with circular array or linked list. Double-ended queue (deque) allows O(1) add/remove from both ends. Queues are used in BFS, task scheduling, and buffering.

```python
# Python - queue with collections.deque
from collections import deque
q = deque()
q.append(1)              # enqueue
q.append(2)
x = q.popleft()          # dequeue
```

```javascript
// JavaScript - queue with array
const queue = [];
queue.push(1);           // enqueue
queue.push(2);
const x = queue.shift(); // dequeue
```

## Hash Table

A hash table maps keys to values using a hash function to compute an index. Average case: O(1) insert, delete, lookup. Worst case: O(n) when many collisions. Collision resolution: chaining (linked list at each bucket) or open addressing (linear probing, quadratic probing). Load factor = n/m affects performance; typically resize when load factor exceeds 0.7.

```python
# Python - dict (hash table)
d = {}
d["a"] = 1              # O(1) insert
d["b"] = 2
x = d.get("a")          # O(1) lookup
del d["a"]              # O(1) delete
```

```javascript
// JavaScript - Map (hash table)
const map = new Map();
map.set("a", 1);        // O(1) insert
map.set("b", 2);
const x = map.get("a"); // O(1) lookup
map.delete("a");        // O(1) delete
```

## Binary Tree

A binary tree has at most two children per node: left and right. Full binary tree: every node has 0 or 2 children. Complete binary tree: all levels fully filled except possibly the last, filled left to right. Height of a tree with n nodes: minimum floor(log2 n)+1, maximum n (skewed). Tree traversal: inorder (left, root, right), preorder (root, left, right), postorder (left, right, root).

```python
# Python - binary tree inorder traversal
def inorder(root):
    if not root:
        return
    inorder(root.left)
    print(root.val)
    inorder(root.right)
```

```javascript
// JavaScript - binary tree inorder traversal
function inorder(root) {
  if (!root) return;
  inorder(root.left);
  console.log(root.val);
  inorder(root.right);
}
```

## Binary Search Tree (BST)

A BST is a binary tree where for every node, left subtree contains smaller keys and right subtree contains larger keys. Inorder traversal yields sorted order. Search, insert, delete: O(h) where h is height. Balanced BST (AVL, Red-Black) keeps h = O(log n), giving O(log n) operations. BST supports predecessor, successor, range queries efficiently.

```python
# Python - BST search
def bst_search(root, key):
    if not root or root.val == key:
        return root
    return bst_search(root.right, key) if key > root.val else bst_search(root.left, key)
```

```javascript
// JavaScript - BST search
function bstSearch(root, key) {
  if (!root || root.val === key) return root;
  return key > root.val ? bstSearch(root.right, key) : bstSearch(root.left, key);
}
```

## AVL Tree

AVL tree is a self-balancing BST where the heights of left and right subtrees of every node differ by at most 1. After insert or delete, rotations (single or double) restore balance. Four rotation cases: LL, RR, LR, RL. Guarantees O(log n) for all operations. Balance factor = height(left) - height(right); must be -1, 0, or 1.

```python
# Python - AVL balance factor
def height(node):
    return 0 if not node else 1 + max(height(node.left), height(node.right))

def balance_factor(node):
    return height(node.left) - height(node.right) if node else 0
```

```javascript
// JavaScript - AVL balance factor
function height(node) {
  return !node ? 0 : 1 + Math.max(height(node.left), height(node.right));
}
function balanceFactor(node) {
  return node ? height(node.left) - height(node.right) : 0;
}
```

## Red-Black Tree

Red-black tree is another self-balancing BST with colored nodes (red or black). Properties: root is black; red nodes have black children; every path from node to null has same number of black nodes. Insertion and deletion use recoloring and rotations. Slightly less strict than AVL, fewer rotations, commonly used in std::map, TreeMap.

```python
# Python - use sortedcontainers or bisect for red-black like behavior
import bisect
arr = []
bisect.insort(arr, 5)
bisect.insort(arr, 3)
idx = bisect.bisect_left(arr, 4)
```

```javascript
// JavaScript - TreeMap equivalent (use library or implement)
// Native: no built-in. Use Map for insertion order or implement RB tree
const map = new Map();
map.set(5, "five");
map.set(3, "three");
```

## Heap

A heap is a complete binary tree satisfying the heap property: parent is >= children (max-heap) or <= children (min-heap). Used for priority queue, heap sort. Insert: O(log n), add at end then bubble up. Extract max/min: O(log n), replace root with last, bubble down. Build heap from array: O(n) with bottom-up approach. Heapify: O(log n) per node.

```python
# Python - min-heap with heapq
import heapq
h = []
heapq.heappush(h, 3)
heapq.heappush(h, 1)
heapq.heappush(h, 2)
x = heapq.heappop(h)   # 1
```

```javascript
// JavaScript - min-heap (no built-in, use array)
// Manual: parent at i, children at 2i+1, 2i+2
const heap = [];
function push(h, x) {
  h.push(x);
  let i = h.length - 1;
  while (i > 0 && h[Math.floor((i-1)/2)] > h[i]) {
    [h[i], h[(i-1)>>1]] = [h[(i-1)>>1], h[i]];
    i = (i-1) >> 1;
  }
}
```

## Min-Heap and Max-Heap

Min-heap: root is minimum, parent <= children. Max-heap: root is maximum, parent >= children. Array representation: for node at index i, left child at 2i+1, right at 2i+2, parent at (i-1)/2. Heaps support find-min/max in O(1), insert and extract in O(log n). Used for Dijkstra, scheduling, merge k sorted lists.

```python
# Python - heap array indices
def left(i): return 2*i + 1
def right(i): return 2*i + 2
def parent(i): return (i - 1) // 2
# min at heap[0]
```

```javascript
// JavaScript - heap array indices
const left = i => 2*i + 1;
const right = i => 2*i + 2;
const parent = i => (i - 1) >> 1;
// min at heap[0]
```

## Graph

A graph G = (V, E) consists of vertices and edges. Directed vs undirected. Weighted vs unweighted. Representation: adjacency list (O(V+E) space, good for sparse) or adjacency matrix (O(V^2) space, O(1) edge lookup). Graph algorithms: BFS, DFS, shortest path (Dijkstra, Bellman-Ford), minimum spanning tree (Prim, Kruskal), topological sort.

```python
# Python - adjacency list
graph = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
# or: graph = defaultdict(list)
```

```javascript
// JavaScript - adjacency list
const graph = { 0: [1, 2], 1: [0, 2], 2: [0, 1] };
// or: const graph = Array(n).fill(null).map(() => []);
```

## BFS (Breadth-First Search)

BFS explores level by level using a queue. Start from source, enqueue neighbors, process in FIFO order. Finds shortest path in unweighted graphs. Time O(V+E), space O(V). Applications: shortest path in unweighted graph, level-order tree traversal, finding connected components, bipartite checking.

```python
# Python - BFS
from collections import deque
def bfs(graph, start):
    visited, q = set(), deque([start])
    while q:
        u = q.popleft()
        if u in visited: continue
        visited.add(u)
        for v in graph[u]:
            q.append(v)
```

```javascript
// JavaScript - BFS
function bfs(graph, start) {
  const visited = new Set(), q = [start];
  while (q.length) {
    const u = q.shift();
    if (visited.has(u)) continue;
    visited.add(u);
    for (const v of graph[u]) q.push(v);
  }
}
```

## DFS (Depth-First Search)

DFS goes deep before wide, using a stack (or recursion). Visit node, recurse on unvisited neighbors. Time O(V+E). Applications: cycle detection, topological sort, finding strongly connected components, path finding, backtracking. Can be implemented iteratively with explicit stack.

```python
# Python - DFS recursive
def dfs(graph, u, visited=None):
    visited = visited or set()
    visited.add(u)
    for v in graph[u]:
        if v not in visited:
            dfs(graph, v, visited)
```

```javascript
// JavaScript - DFS recursive
function dfs(graph, u, visited = new Set()) {
  visited.add(u);
  for (const v of graph[u]) {
    if (!visited.has(v)) dfs(graph, v, visited);
  }
}
```

## Dijkstra's Algorithm

Dijkstra finds shortest path from source to all vertices in a graph with non-negative edge weights. Uses a priority queue (min-heap). Greedy: always relax the vertex with smallest tentative distance. Time O((V+E) log V) with binary heap, O(V^2) with array. Does not work with negative weights; use Bellman-Ford for that.

```python
# Python - Dijkstra with heapq
import heapq
def dijkstra(graph, start):
    dist = {v: float('inf') for v in graph}
    dist[start], pq = 0, [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist
```

```javascript
// JavaScript - Dijkstra with min-heap
function dijkstra(graph, start) {
  const dist = {};
  for (const v in graph) dist[v] = Infinity;
  dist[start] = 0;
  const pq = [[0, start]];
  while (pq.length) {
    const [d, u] = pq.shift();
    if (d > dist[u]) continue;
    for (const [v, w] of graph[u]) {
      if (dist[u] + w < dist[v]) {
        dist[v] = dist[u] + w;
        pq.push([dist[v], v]);
        pq.sort((a, b) => a[0] - b[0]);
      }
    }
  }
  return dist;
}
```

## Dynamic Programming

Dynamic programming solves problems by combining solutions to overlapping subproblems. Two approaches: top-down (memoization, recursive with cache) and bottom-up (iterative, fill table). Key steps: define subproblems, write recurrence, identify base cases, determine computation order. Classic problems: Fibonacci, knapsack, LCS, LIS, edit distance, matrix chain multiplication.

```python
# Python - Fibonacci DP
def fib(n):
    if n <= 1: return n
    dp = [0, 1]
    for i in range(2, n + 1):
        dp.append(dp[i-1] + dp[i-2])
    return dp[n]
```

```javascript
// JavaScript - Fibonacci DP
function fib(n) {
  if (n <= 1) return n;
  const dp = [0, 1];
  for (let i = 2; i <= n; i++) dp.push(dp[i-1] + dp[i-2]);
  return dp[n];
}
```

## Greedy Algorithms

Greedy algorithms make locally optimal choices at each step, hoping for global optimum. Works when problem has optimal substructure and greedy choice property. Examples: activity selection, Huffman coding, fractional knapsack, Dijkstra, Prim, Kruskal. Not always optimal (e.g., 0-1 knapsack); proof of correctness often uses exchange argument.

```python
# Python - fractional knapsack greedy
def fractional_knapsack(items, capacity):
    items.sort(key=lambda x: x[1]/x[0], reverse=True)
    total = 0
    for w, v in items:
        take = min(w, capacity)
        total += take * (v / w)
        capacity -= take
    return total
```

```javascript
// JavaScript - fractional knapsack greedy
function fractionalKnapsack(items, capacity) {
  items.sort((a, b) => b[1]/b[0] - a[1]/a[0]);
  let total = 0;
  for (const [w, v] of items) {
    const take = Math.min(w, capacity);
    total += take * (v / w);
    capacity -= take;
  }
  return total;
}
```

## Divide and Conquer

Divide and conquer splits problem into smaller subproblems, solves them recursively, and combines results. Recurrence: T(n) = aT(n/b) + f(n). Master theorem gives closed form for many cases. Examples: merge sort, quick sort, binary search, Strassen matrix multiplication, closest pair of points.

```python
# Python - merge sort (divide and conquer)
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))

def merge(a, b):
    i, j, out = 0, 0, []
    while i < len(a) and j < len(b):
        out.append(a[i] if a[i] <= b[j] else b[j])
        (i if a[i] <= b[j] else j) += 1
    return out + a[i:] + b[j:]
```

```javascript
// JavaScript - merge sort (divide and conquer)
function mergeSort(arr) {
  if (arr.length <= 1) return arr;
  const mid = arr.length >> 1;
  return merge(mergeSort(arr.slice(0, mid)), mergeSort(arr.slice(mid)));
}
function merge(a, b) {
  const out = [];
  let i = 0, j = 0;
  while (i < a.length && j < b.length)
    out.push(a[i] <= b[j] ? a[i++] : b[j++]);
  return out.concat(a.slice(i), b.slice(j));
}
```

## Backtracking

Backtracking builds solutions incrementally, abandons partial solutions (backtracks) when they cannot lead to valid complete solution. Used for constraint satisfaction: N-Queens, Sudoku, subset sum, permutation generation. Template: choose, recurse, unchoose. Pruning reduces search space.

```python
# Python - permutations backtracking
def permute(nums):
    def backtrack(path, remaining):
        if not remaining: res.append(path[:])
        for i, x in enumerate(remaining):
            path.append(x)
            backtrack(path, remaining[:i] + remaining[i+1:])
            path.pop()
    res = []
    backtrack([], nums)
    return res
```

```javascript
// JavaScript - permutations backtracking
function permute(nums) {
  const res = [];
  function backtrack(path, remaining) {
    if (!remaining.length) res.push([...path]);
    for (let i = 0; i < remaining.length; i++) {
      path.push(remaining[i]);
      backtrack(path, [...remaining.slice(0,i), ...remaining.slice(i+1)]);
      path.pop();
    }
  }
  backtrack([], nums);
  return res;
}
```

## Merge Sort

Merge sort is a divide-and-conquer sorting algorithm. It recursively splits a list into halves until sublists are size one, then merges sorted sublists into a final sorted list. Stable sort. Time complexity O(n log n) in best, average, and worst cases. Space O(n) for merge. Recursion depth O(log n).

```python
# Python - merge sort
def merge_sort(arr):
    if len(arr) <= 1: return arr
    m = len(arr) // 2
    L, R = merge_sort(arr[:m]), merge_sort(arr[m:])
    i = j = 0
    out = []
    while i < len(L) and j < len(R):
        out.append(L[i] if L[i] <= R[j] else R[j])
        (i, j) = (i+1, j) if L[i] <= R[j] else (i, j+1)
    return out + L[i:] + R[j:]
```

```javascript
// JavaScript - merge sort
function mergeSort(arr) {
  if (arr.length <= 1) return arr;
  const m = arr.length >> 1;
  const L = mergeSort(arr.slice(0, m)), R = mergeSort(arr.slice(m));
  let i = 0, j = 0, out = [];
  while (i < L.length && j < R.length)
    out.push(L[i] <= R[j] ? L[i++] : R[j++]);
  return out.concat(L.slice(i), R.slice(j));
}
```

## Quick Sort

Quick sort picks a pivot, partitions array so smaller elements are left, larger right, then recurses on both parts. Average O(n log n), worst O(n^2) when pivot is always min/max. In-place with Lomuto or Hoare partition. Randomized pivot gives expected O(n log n). Not stable. Often faster than merge sort in practice due to cache locality.

```python
# Python - quicksort
def quicksort(arr, lo=0, hi=None):
    hi = hi or len(arr) - 1
    if lo >= hi: return
    p = partition(arr, lo, hi)
    quicksort(arr, lo, p - 1)
    quicksort(arr, p + 1, hi)

def partition(arr, lo, hi):
    pivot, i = arr[hi], lo
    for j in range(lo, hi):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i
```

```javascript
// JavaScript - quicksort
function quicksort(arr, lo = 0, hi = arr.length - 1) {
  if (lo >= hi) return;
  const p = partition(arr, lo, hi);
  quicksort(arr, lo, p - 1);
  quicksort(arr, p + 1, hi);
}
function partition(arr, lo, hi) {
  const pivot = arr[hi];
  let i = lo;
  for (let j = lo; j < hi; j++)
    if (arr[j] <= pivot) [arr[i], arr[j]] = [arr[j], arr[i]], i++;
  [arr[i], arr[hi]] = [arr[hi], arr[i]];
  return i;
}
```

## Heap Sort

Heap sort builds a max-heap from array, repeatedly extracts max and places at end. In-place, O(n log n) for all cases. Not stable. Build heap: O(n). Each of n extract-max: O(log n). Total O(n log n).

```python
# Python - heap sort
import heapq
def heap_sort(arr):
    heapq.heapify(arr)
    return [heapq.heappop(arr) for _ in range(len(arr))]
# or manual: build max-heap, for i from n-1 down to 1: swap arr[0], arr[i], heapify(0)
```

```javascript
// JavaScript - heap sort
function heapSort(arr) {
  const n = arr.length;
  for (let i = Math.floor(n/2)-1; i >= 0; i--) heapify(arr, n, i);
  for (let i = n-1; i > 0; i--) {
    [arr[0], arr[i]] = [arr[i], arr[0]];
    heapify(arr, i, 0);
  }
}
function heapify(arr, n, i) {
  let largest = i, l = 2*i+1, r = 2*i+2;
  if (l < n && arr[l] > arr[largest]) largest = l;
  if (r < n && arr[r] > arr[largest]) largest = r;
  if (largest !== i) [arr[i], arr[largest]] = [arr[largest], arr[i]], heapify(arr, n, largest);
}
```

## Binary Search

Binary search works on sorted arrays by repeatedly halving the search interval. Compare target with middle element; if equal, found; if less, search left half; if greater, search right half. Time O(log n). Variants: lower_bound, upper_bound, search in rotated array, search in 2D matrix.

```python
# Python - binary search
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target: return mid
        if arr[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1
```

```javascript
// JavaScript - binary search
function binarySearch(arr, target) {
  let lo = 0, hi = arr.length - 1;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (arr[mid] === target) return mid;
    arr[mid] < target ? lo = mid + 1 : hi = mid - 1;
  }
  return -1;
}
```

## Bubble Sort

Bubble sort repeatedly swaps adjacent elements if they are in wrong order. Pass through array until no swaps needed. Time O(n^2), space O(1). Stable. Rarely used; mainly educational.

## Insertion Sort

Insertion sort builds sorted array one element at a time by inserting each new element into its correct position in the sorted portion. Time O(n^2) worst, O(n) best when nearly sorted. In-place, stable. Good for small arrays or nearly sorted data.

## Selection Sort

Selection sort repeatedly selects minimum from unsorted portion and swaps to front. Time O(n^2) always. In-place, not stable. Makes minimum number of swaps (at most n-1).

## Counting Sort

Counting sort assumes input is integers in range [0, k]. Count occurrences, compute cumulative counts, place elements in output. Time O(n + k), space O(k). Stable when implemented carefully. Used when k is small relative to n.

## Radix Sort

Radix sort sorts integers by processing digits from least to most significant (or vice versa). Uses stable sort (e.g., counting sort) per digit. Time O(d * (n + k)) where d is number of digits. Good for fixed-length integers or strings.

## Topological Sort

Topological sort orders vertices in a DAG so that for every edge (u,v), u comes before v. Applications: task scheduling, build order. Algorithms: DFS (post-order reverse), Kahn's (BFS with in-degree zero). Not unique. Only possible for DAG; cycle detection fails topological sort.

## Trie (Prefix Tree)

A trie stores strings with common prefixes sharing nodes. Each node has up to 26 (or 256) children. Root to node path spells a prefix. Insert, search, delete: O(m) where m is string length. Applications: autocomplete, spell check, IP routing, word games.

## Segment Tree

Segment tree supports range queries and point updates in O(log n). Each leaf is an element; internal nodes store aggregate (sum, min, max) of their segment. Build O(n), query O(log n), update O(log n). Used for range sum, range min/max, lazy propagation for range updates.

## Binary Indexed Tree (Fenwick Tree)

Fenwick tree supports prefix sum queries and point updates in O(log n). Uses less memory than segment tree. Based on binary representation: each node stores sum of a range. Update: add to node and ancestors. Query: sum of prefix by traversing indices.

## Union-Find (Disjoint Set)

Union-Find maintains disjoint sets with operations: Find (which set does element belong to), Union (merge two sets). Optimizations: path compression (Find), union by rank (Union). Amortized O(α(n)) ≈ O(1) per operation. Used for cycle detection in graphs, Kruskal's MST, connected components.

## Sliding Window

Sliding window technique maintains a "window" of elements and slides it across the array. Used for subarray/substring problems with constraints (max sum of k elements, longest substring with k distinct chars). Two pointers: expand window until constraint violated, then shrink from left. Time often O(n).

## Two Pointers

Two pointers technique uses two indices moving through the array, often from opposite ends or same direction. Applications: two sum in sorted array, remove duplicates, palindrome check, merge two sorted arrays. Reduces time from O(n^2) to O(n) in many cases.

## Prefix Sum

Prefix sum precomputes cumulative sums: prefix[i] = sum of arr[0..i]. Range sum query [l,r] = prefix[r] - prefix[l-1] in O(1). Handles multiple queries efficiently. 2D prefix sum for matrix range queries.

## Bit Manipulation

Bit manipulation uses bitwise operations: AND, OR, XOR, NOT, left/right shift. XOR properties: a^a=0, a^0=a; useful for finding single duplicate. Check if power of 2: n & (n-1) == 0. Get/set/clear/toggle bit at position i. Count set bits: Brian Kernighan or lookup table.

## String Matching

String matching finds pattern in text. Naive: O(n*m). KMP: O(n+m) with failure function. Rabin-Karp: rolling hash O(n+m) average. Boyer-Moore: often sublinear. Applications: search, plagiarism detection, bioinformatics.

## KMP Algorithm

KMP preprocesses pattern to build longest proper prefix which is also suffix (LPS) array. When mismatch, shift by LPS value instead of one. Avoids rechecking known matches. Time O(n + m). LPS construction: O(m).

## Longest Common Subsequence (LCS)

LCS finds longest subsequence (order preserved, not necessarily contiguous) common to two strings. DP: dp[i][j] = LCS of s1[0..i] and s2[0..j]. Recurrence: if s1[i]==s2[j], dp[i][j]=1+dp[i-1][j-1]; else dp[i][j]=max(dp[i-1][j], dp[i][j-1]). Time O(m*n), space O(m*n) or O(min(m,n)) optimized.

## Longest Increasing Subsequence (LIS)

LIS finds longest strictly increasing subsequence. DP: O(n^2) with dp[i] = length of LIS ending at i. Binary search: O(n log n) by maintaining active list and using lower_bound. Patience sorting approach.

## Knapsack Problem

0-1 knapsack: each item once, maximize value with weight limit. DP: dp[i][w] = max value using first i items with capacity w. Recurrence: include item or exclude. Space can be optimized to O(W). Fractional knapsack: greedy, take by value/weight ratio.

## Matrix Chain Multiplication

Given matrices A1, A2, ..., An with dimensions, find optimal parenthesization to minimize scalar multiplications. DP: m[i][j] = min multiplications for Ai...Aj. Recurrence: try all split points k. Time O(n^3).

## Floyd-Warshall

Floyd-Warshall finds all-pairs shortest paths in O(V^3). Handles negative weights (no negative cycles). dp[k][i][j] = shortest path from i to j using only vertices 0..k. Space can be O(V^2) by reusing matrix.

## Bellman-Ford

Bellman-Ford finds shortest path from source with negative weights. Relax all edges V-1 times. Detects negative cycles: if V-th relaxation still improves, negative cycle exists. Time O(V*E). Slower than Dijkstra but handles negative edges.

## Prim's Algorithm

Prim's finds minimum spanning tree by growing a single tree. Start from any vertex, add minimum weight edge connecting tree to outside vertex. Use min-heap for efficiency. Time O(E log V) with heap. Produces MST.

## Kruskal's Algorithm

Kruskal's finds MST by sorting edges and adding in order if they don't form cycle. Use Union-Find for cycle detection. Time O(E log E) for sort. Greedy: each step adds minimum weight edge that doesn't create cycle.

## Strongly Connected Components (SCC)

SCC: maximal subgraph where every vertex reachable from every other. Kosaraju: two DFS passes. Tarjan: single DFS with low-link values. Applications: dependency analysis, 2-SAT.

## Cycle Detection

In directed graph: DFS with recursion stack (back edge). In undirected: DFS, cycle if neighbor is visited and not parent. Floyd cycle detection (tortoise-hare) for linked list: O(1) space.

## Recursion vs Iteration

Recursion uses call stack; iteration uses explicit loop. Recursion can be converted to iteration with explicit stack. Tail recursion can be optimized to iteration by compiler. Choose recursion for natural recursive structure (trees, divide-conquer); iteration when stack depth is concern or for simple loops.

## Time Complexity

Big O: upper bound, worst case. Big Omega: lower bound. Big Theta: tight bound. Common: O(1), O(log n), O(n), O(n log n), O(n^2), O(2^n), O(n!). Amortized: average over sequence of operations. Master theorem for divide-conquer recurrences.

## Space Complexity

Space includes input, auxiliary space (extra variables, stack). Recursion depth counts. In-place: O(1) extra space. Be mindful of recursion depth for large inputs; may need iterative or tail-recursive solution.

## Hash Functions

Good hash function: uniform distribution, minimize collisions. Division method: h(k) = k mod m. Multiplication: h(k) = floor(m * frac(k * A)). Universal hashing: random hash from family. Cryptographic: SHA, MD5. For hash tables: fast to compute, good avalanche effect.

## Cache Replacement Policies

LRU: least recently used. LFU: least frequently used. FIFO: first in first out. Random: random replacement. Optimal: Belady's MIN (clairvoyant). LRU is k-competitive for cache size k.

## Bloom Filter

Bloom filter: probabilistic set membership. k hash functions, m bits. Add: set k bits. Query: all k bits set means probably in set. No false negatives. False positive rate: (1 - e^(-kn/m))^k. Cannot delete without counting variant.

## Disjoint Set Union

Union-Find: MakeSet, Find, Union. Path compression: Find makes nodes point to root. Union by rank: attach smaller under larger. Amortized O(α(n)) per operation. α is inverse Ackermann, effectively constant.

## Tail Recursion

Tail recursion: recursive call is last operation. Can be optimized to iteration by compiler. No stack growth. Convert by accumulating result in parameter. Example: factorial tail recursive with accumulator.

## Invariant and Loop Invariant

Invariant: property that holds throughout. Loop invariant: true before each iteration, after initialization, maintained by iteration, gives correctness when loop terminates. Used to prove algorithm correctness.

## Stable Sort

Stable sort preserves relative order of equal elements. Merge sort stable; quicksort not. Important for multi-key sorting. Insertion sort, bubble sort, counting sort are stable. Heap sort, selection sort typically not stable.

## In-Place Algorithm

In-place: O(1) extra space beyond input. Quicksort in-place with Lomuto or Hoare partition. Merge sort typically not in-place (needs O(n) for merge). Heapsort in-place.

## Comparison-Based Sort Lower Bound

Decision tree model: each comparison branches. n! leaves for n elements. Height at least log2(n!) = Ω(n log n). No comparison sort beats O(n log n). Radix and counting sort use more information.

## Randomized Algorithm

Randomized: use random numbers. Las Vegas: always correct, random time. Monte Carlo: may err, fixed time. Quicksort random pivot: O(n log n) expected. Randomized selection: O(n) expected. Often simpler than deterministic.

## Divide and Conquer Recurrence

T(n) = aT(n/b) + f(n). a subproblems, each n/b size. Merge sort: T(n) = 2T(n/2) + O(n) = O(n log n). Master theorem gives solution. Recursion tree: sum levels.

## Optimal Substructure

Optimal substructure: optimal solution contains optimal solutions to subproblems. Required for DP and greedy. LCS: LCS of prefixes. Shortest path: shortest path to intermediate + edge from intermediate.

## Overlapping Subproblems

Overlapping subproblems: same subproblems solved repeatedly. Fibonacci: fib(n-2) computed multiple times. DP stores results. Memoization or tabulation. Distinguishes DP from divide and conquer.

## Greedy Exchange Argument

Exchange argument: show greedy choice is in some optimal solution. Replace part of optimal with greedy choice; show not worse. Or show optimal can be transformed to include greedy. Standard proof technique.

## Backtracking Pruning

Pruning: skip branches that cannot lead to solution. Constraint propagation. Early termination. Reduces search space dramatically. N-Queens: skip column if same column/diagonal has queen.

## Memoization vs Tabulation

Memoization: top-down, recursive. Check cache before compute. Tabulation: bottom-up, iterative. Fill table in order. Memoization: easier to write, may compute only needed. Tabulation: no stack overflow, often faster.

## Graph Traversal Applications

BFS: shortest path unweighted, level order. DFS: cycle detection, topological sort, path finding, SCC. Both: connectivity, bipartite. Preorder, postorder, inorder for trees.

## Tree Traversal Orders

Preorder: root, left, right. Inorder: left, root, right (BST gives sorted). Postorder: left, right, root. Level order: BFS. Morris: O(1) space inorder. Uses threaded pointers.

## Binary Search Variants

Lower bound: first >= target. Upper bound: first > target. Search in rotated array. Search in 2D matrix. Search in unknown size. Search in answer space.

## Sliding Window Technique

Two pointers. Expand: add until constraint violated. Shrink: remove from left until valid. Maintain invariant. O(n) for many substring problems. Fixed or variable size window.

## Prefix Sum

Prefix[i] = sum of arr[0..i]. Range sum [l,r] = prefix[r] - prefix[l-1]. O(1) query after O(n) preprocess. 2D prefix for matrix. Difference array for range updates.

## Two Pointers Technique

Two indices, same or opposite direction. Sorted array two sum. Remove duplicates. Merge sorted arrays. Palindrome check. Often reduces O(n^2) to O(n).

## Bit Manipulation Tricks

XOR: a^a=0, a^0=a. Swap: a^=b^=a^=b. Power of 2: n & (n-1) == 0. Set bit i: n | (1<<i). Clear bit i: n & ~(1<<i). Toggle: n ^ (1<<i). Count set bits: Brian Kernighan n &= n-1.

## Recursion Call Stack

Each recursive call pushes frame. Frame: parameters, return address, local variables. Stack overflow: too deep. Tail call optimization: reuse frame for tail call. Convert to iteration with explicit stack.

## Linked List Dummy Node

Dummy node: head = dummy, return dummy.next. Simplifies edge cases (empty list, single node). No special case for head. Used in merge, remove, reverse.

## Tree Recursion Pattern

Recurse on left and right. Base case: null. Combine results. Return value or modify in place. Postorder: process after children. Preorder: process before children.

## DP State Definition

State: what we need to remember. Transition: how states relate. Base case: initial state. Order: fill dependencies first. Space optimization: reuse rows if only previous needed.

## Graph Representation Choice

Adjacency list: sparse, O(V+E) space. Adjacency matrix: dense, O(1) edge lookup. Edge list: for Kruskal. Incidence: special cases. Choose based on operations needed.
