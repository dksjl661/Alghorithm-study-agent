# Data Structures Reference

## Array Operations

Array provides O(1) random access by index. Insertion at end: O(1) amortized for dynamic array. Insertion at beginning or middle: O(n) due to shifting. Deletion: O(n) for shifting. Search unsorted: O(n). Search sorted: O(log n) with binary search. Arrays are cache-friendly due to contiguous memory layout.

```python
# Python - array ops
arr = [1, 2, 3]
arr[1]  # O(1) access
arr.append(4)  # O(1) amortized
arr.insert(0, 0)  # O(n)
```

```javascript
// JavaScript - array ops
const arr = [1, 2, 3];
arr[1];  // O(1) access
arr.push(4);  // O(1) amortized
arr.unshift(0);  // O(n)
```

## Linked List Operations

Singly linked list: Insert at head O(1), insert at tail O(1) with tail pointer else O(n). Delete: O(n) to find node, O(1) to remove if we have predecessor. Search: O(n). No random access. Doubly linked list allows O(1) deletion when node reference is known. Circular linked list: last node points to head.

```python
# Python - linked list insert head
def insert_head(head, val):
    return Node(val, head)
```

```javascript
// JavaScript - linked list insert head
function insertHead(head, val) {
  return new Node(val, head);
}
```

## Linked List Reversal

Reverse linked list iteratively: use three pointers (prev, curr, next), traverse and flip next pointers. Reverse recursively: base case empty or single node; recursively reverse rest, then set rest's next to current, current's next to null. Both O(n) time, O(1) iterative space, O(n) recursive stack space.

```python
# Python - iterative reverse
def reverse(head):
    prev = None
    while head:
        nxt = head.next
        head.next = prev
        prev, head = head, nxt
    return prev
```

```javascript
// JavaScript - iterative reverse
function reverse(head) {
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

## Linked List Cycle Detection

Floyd's cycle detection (tortoise and hare): slow pointer moves 1 step, fast moves 2. If they meet, cycle exists. To find cycle start: after meeting, move one to head, both move 1 step until they meet. O(n) time, O(1) space.

## Stack Implementation

Stack can be implemented with array (push = append, pop = remove last) or linked list (push = insert at head, pop = remove from head). Array implementation may need to resize. All operations O(1) amortized. Stack overflow: recursion too deep; stack underflow: pop from empty stack.

## Queue Implementation

Queue with array: use circular buffer with front and rear indices. Enqueue: increment rear, add element. Dequeue: increment front, return element. Resize when full. Queue with linked list: enqueue at tail, dequeue from head. Need to maintain head and tail pointers for O(1) both operations.

## Hash Table Collision

Chaining: each bucket holds linked list of entries. Load factor n/m. Average chain length = load factor. Open addressing: probe for empty slot. Linear probing: (h(k) + i) mod m. Quadratic: (h(k) + c1*i + c2*i^2) mod m. Double hashing: (h1(k) + i*h2(k)) mod m. Clustering affects performance.

## Binary Tree Traversal

Inorder (LNR): left, node, right. For BST gives sorted order. Preorder (NLR): node, left, right. Useful for copying tree, prefix expression. Postorder (LRN): left, right, node. Useful for deletion, postfix expression. Level order: BFS with queue. All O(n) time.

## BST Operations

Search: compare with root, go left if smaller, right if larger. O(h). Insert: find position as in search, add new node. O(h). Delete: three cases - no child (remove), one child (replace with child), two children (replace with inorder successor, then delete successor). O(h).

## Heap Operations

Insert: add at end, sift up (compare with parent, swap if violates heap property). O(log n). Extract: swap root with last, remove last, sift down root. O(log n). Decrease key: update value, sift up. Increase key: update value, sift down. Used in priority queue, Dijkstra.

## Graph Representations

Adjacency list: array of lists, each list has neighbors of vertex. Space O(V+E). Good for sparse graphs. Adjacency matrix: V×V matrix, entry [i][j] = 1 if edge exists. Space O(V^2). O(1) edge lookup. For weighted: store weights instead of 1. Incidence matrix: V×E for bipartite matching.

## Trie Operations

Insert: traverse/create path for each character. O(m). Search: traverse path, check if word ends at node. O(m). Delete: traverse, remove nodes if no other words use them. O(m). Prefix search: traverse to prefix node, DFS for all words. Autocomplete, spell check applications.

## Segment Tree Operations

Build: recursively build left and right, combine. O(n). Query [l,r]: traverse, if segment fully in range return value, else recurse and combine. O(log n). Update: find leaf, update, propagate up. O(log n). Lazy propagation: defer range updates to children when needed.

## Union-Find Operations

MakeSet(x): create singleton set. Find(x): return root of set, with path compression. Union(x,y): merge sets containing x and y, by rank. Path compression: during Find, make each node point to root. Union by rank: attach smaller tree under larger. Amortized O(α(n)).

## Deque (Double-Ended Queue)

Deque allows O(1) add and remove from both front and back. Implement with doubly linked list or circular array. Applications: sliding window max/min, BFS with level tracking, palindrome checker (compare front and back while removing).

## Priority Queue

Priority queue supports insert and extract-min/max in O(log n). Implement with binary heap. Can use max-heap for max priority or min-heap for min. Applications: Dijkstra, Huffman coding, merge k sorted lists, task scheduling. STL priority_queue, Python heapq.

## Skip List

Skip list is probabilistic alternative to balanced trees. Multiple levels of linked lists; higher levels skip more elements. Search: start at top level, go right until too far, drop down. Expected O(log n) search, insert, delete. Used in Redis sorted sets.

## B-Tree

B-tree is self-balancing tree for disk. Each node has many keys and children (order m). All leaves at same level. Used in databases and file systems. Height O(log_m n). Insert and delete maintain balance by splitting and merging nodes.

## Bloom Filter

Bloom filter is space-efficient probabilistic structure for set membership. No false negatives; may have false positives. Uses k hash functions and bit array. Add: set k bits. Query: check k bits, all set means probably in set. Cannot delete. Used for cache, spell check, duplicate detection.
