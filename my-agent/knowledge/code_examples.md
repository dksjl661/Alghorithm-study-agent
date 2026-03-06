# Code Examples - JavaScript and Python for All Topics

This file contains JavaScript and Python code examples for data structures and algorithms. Each topic has both language implementations.

## Linked List Reversal

```python
def reverse_list(head):
    prev = None
    while head:
        nxt = head.next
        head.next = prev
        prev = head
        head = nxt
    return prev
```

```javascript
function reverseList(head) {
  let prev = null;
  while (head) {
    const nxt = head.next;
    head.next = prev;
    prev = head;
    head = nxt;
  }
  return prev;
}
```

## Linked List Cycle Detection (Floyd)

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow == fast:
            return True
    return False
```

```javascript
function hasCycle(head) {
  let slow = head, fast = head;
  while (fast && fast.next) {
    slow = slow.next; fast = fast.next.next;
    if (slow === fast) return true;
  }
  return false;
}
```

## Stack

```python
class Stack:
    def __init__(self):
        self.stack = []
    def push(self, x): self.stack.append(x)
    def pop(self): return self.stack.pop() if self.stack else None
    def peek(self): return self.stack[-1] if self.stack else None
```

```javascript
class Stack {
  constructor() { this.stack = []; }
  push(x) { this.stack.push(x); }
  pop() { return this.stack.pop(); }
  peek() { return this.stack[this.stack.length - 1]; }
}
```

## Queue

```python
from collections import deque
class Queue:
    def __init__(self): self.q = deque()
    def enqueue(self, x): self.q.append(x)
    def dequeue(self): return self.q.popleft() if self.q else None
```

```javascript
class Queue {
  constructor() { this.q = []; }
  enqueue(x) { this.q.push(x); }
  dequeue() { return this.q.shift(); }
}
```

## Trie

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self): self.root = TrieNode()
    def insert(self, word):
        node = self.root
        for c in word:
            node = node.children.setdefault(c, TrieNode())
        node.is_end = True
    def search(self, word):
        node = self.root
        for c in word:
            if c not in node.children: return False
            node = node.children[c]
        return node.is_end
```

```javascript
class TrieNode {
  constructor() { this.children = {}; this.isEnd = false; }
}
class Trie {
  constructor() { this.root = new TrieNode(); }
  insert(word) {
    let node = this.root;
    for (const c of word) {
      if (!node.children[c]) node.children[c] = new TrieNode();
      node = node.children[c];
    }
    node.isEnd = true;
  }
  search(word) {
    let node = this.root;
    for (const c of word) {
      if (!node.children[c]) return false;
      node = node.children[c];
    }
    return node.isEnd;
  }
}
```

## LRU Cache

```python
from collections import OrderedDict
class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = OrderedDict()
    def get(self, key):
        if key not in self.cache: return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    def put(self, key, value):
        if key in self.cache: self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap: self.cache.popitem(last=False)
```

```javascript
class LRUCache {
  constructor(capacity) {
    this.cap = capacity;
    this.cache = new Map();
  }
  get(key) {
    if (!this.cache.has(key)) return -1;
    const v = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, v);
    return v;
  }
  put(key, value) {
    if (this.cache.has(key)) this.cache.delete(key);
    this.cache.set(key, value);
    if (this.cache.size > this.cap) this.cache.delete(this.cache.keys().next().value);
  }
}
```

## Two Sum

```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
```

```javascript
function twoSum(nums, target) {
  const seen = new Map();
  for (let i = 0; i < nums.length; i++) {
    if (seen.has(target - nums[i])) return [seen.get(target - nums[i]), i];
    seen.set(nums[i], i);
  }
}
```

## Valid Parentheses

```python
def is_valid(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for c in s:
        if c in pairs:
            if not stack or stack.pop() != pairs[c]: return False
        else:
            stack.append(c)
    return len(stack) == 0
```

```javascript
function isValid(s) {
  const stack = [];
  const pairs = { ')': '(', ']': '[', '}': '{' };
  for (const c of s) {
    if (c in pairs) {
      if (!stack.length || stack.pop() !== pairs[c]) return false;
    } else stack.push(c);
  }
  return stack.length === 0;
}
```

## Merge Two Sorted Lists

```python
def merge_two_lists(l1, l2):
    dummy = ListNode()
    cur = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            cur.next, l1 = l1, l1.next
        else:
            cur.next, l2 = l2, l2.next
        cur = cur.next
    cur.next = l1 or l2
    return dummy.next
```

```javascript
function mergeTwoLists(l1, l2) {
  const dummy = new ListNode();
  let cur = dummy;
  while (l1 && l2) {
    if (l1.val <= l2.val) cur.next = l1, l1 = l1.next;
    else cur.next = l2, l2 = l2.next;
    cur = cur.next;
  }
  cur.next = l1 || l2;
  return dummy.next;
}
```

## Kadane Maximum Subarray

```python
def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best
```

```javascript
function maxSubarray(nums) {
  let best = cur = nums[0];
  for (let i = 1; i < nums.length; i++) {
    cur = Math.max(nums[i], cur + nums[i]);
    best = Math.max(best, cur);
  }
  return best;
}
```

## Union-Find

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return
        if self.rank[px] < self.rank[py]: px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]: self.rank[px] += 1
```

```javascript
class UnionFind {
  constructor(n) {
    this.parent = Array.from({ length: n }, (_, i) => i);
    this.rank = Array(n).fill(0);
  }
  find(x) {
    if (this.parent[x] !== x) this.parent[x] = this.find(this.parent[x]);
    return this.parent[x];
  }
  union(x, y) {
    const px = this.find(x), py = this.find(y);
    if (px === py) return;
    if (this.rank[px] < this.rank[py]) [px, py] = [py, px];
    this.parent[py] = px;
    if (this.rank[px] === this.rank[py]) this.rank[px]++;
  }
}
```

## KMP Preprocessing

```python
def kmp_prefix(s):
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        pi[i] = j + 1 if s[i] == s[j] else j
    return pi
```

```javascript
function kmpPrefix(s) {
  const n = s.length, pi = Array(n).fill(0);
  for (let i = 1; i < n; i++) {
    let j = pi[i - 1];
    while (j > 0 && s[i] !== s[j]) j = pi[j - 1];
    pi[i] = s[i] === s[j] ? j + 1 : j;
  }
  return pi;
}
```

## Binary Search Lower Bound

```python
def lower_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target: lo = mid + 1
        else: hi = mid
    return lo
```

```javascript
function lowerBound(arr, target) {
  let lo = 0, hi = arr.length;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    arr[mid] < target ? lo = mid + 1 : hi = mid;
  }
  return lo;
}
```

## Sliding Window Max (Deque)

```python
from collections import deque
def max_sliding_window(nums, k):
    dq = deque()
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] < x: dq.pop()
        dq.append(i)
        if dq[0] <= i - k: dq.popleft()
        if i >= k - 1: out.append(nums[dq[0]])
    return out
```

```javascript
function maxSlidingWindow(nums, k) {
  const dq = [], out = [];
  for (let i = 0; i < nums.length; i++) {
    while (dq.length && nums[dq[dq.length-1]] < nums[i]) dq.pop();
    dq.push(i);
    if (dq[0] <= i - k) dq.shift();
    if (i >= k - 1) out.push(nums[dq[0]]);
  }
  return out;
}
```

## Topological Sort (DFS)

```python
def topological_sort(graph):
    visited, order = set(), []
    def dfs(u):
        visited.add(u)
        for v in graph.get(u, []):
            if v not in visited: dfs(v)
        order.append(u)
    for u in graph:
        if u not in visited: dfs(u)
    return order[::-1]
```

```javascript
function topologicalSort(graph) {
  const visited = new Set(), order = [];
  function dfs(u) {
    visited.add(u);
    for (const v of graph[u] || []) {
      if (!visited.has(v)) dfs(v);
    }
    order.push(u);
  }
  for (const u of Object.keys(graph)) {
    if (!visited.has(u)) dfs(u);
  }
  return order.reverse();
}
```

## LCS (Longest Common Subsequence)

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
```

```javascript
function lcs(s1, s2) {
  const m = s1.length, n = s2.length;
  const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = s1[i-1] === s2[j-1] ? dp[i-1][j-1] + 1 : Math.max(dp[i-1][j], dp[i][j-1]);
    }
  }
  return dp[m][n];
}
```

## Edit Distance

```python
def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
    return dp[m][n]
```

```javascript
function editDistance(s1, s2) {
  const m = s1.length, n = s2.length;
  const dp = Array(m + 1).fill(null).map((_, i) => Array(n + 1).fill(0).map((_, j) => i + j));
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      const cost = s1[i-1] === s2[j-1] ? 0 : 1;
      dp[i][j] = Math.min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost);
    }
  }
  return dp[m][n];
}
```

## Fenwick Tree (Binary Indexed Tree)

```python
class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    def update(self, i, delta):
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i
    def query(self, i):
        i += 1
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s
```

```javascript
class FenwickTree {
  constructor(n) {
    this.n = n;
    this.tree = Array(n + 1).fill(0);
  }
  update(i, delta) {
    i++;
    while (i <= this.n) {
      this.tree[i] += delta;
      i += i & -i;
    }
  }
  query(i) {
    i++;
    let s = 0;
    while (i > 0) {
      s += this.tree[i];
      i -= i & -i;
    }
    return s;
  }
}
```
