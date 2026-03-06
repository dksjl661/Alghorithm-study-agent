# Classic Problems and Patterns

## Two Sum

Two sum: find two numbers that add to target. Hash map: O(n) - store complement. Sort + two pointers: O(n log n). Variants: three sum, four sum, k sum.

## Three Sum

Three sum: find triplets summing to zero. Sort, fix one, two pointers for rest. O(n^2). Avoid duplicates by skipping same values. Generalizes to k-sum with recursion.

## Valid Parentheses

Valid parentheses: stack - push open, pop and match on close. O(n). Must handle empty stack. Variants: multiple bracket types, valid with minimum removals.

## Merge Two Sorted Lists

Merge: two pointers, compare and add smaller. O(n+m). Recursive: compare heads, recurse. Used in merge sort.

## Merge K Sorted Lists

Merge k lists: min-heap of size k. O(N log k) for N total elements. Divide and conquer: O(N log k). Used in external sorting.

## Reverse Linked List

Reverse: iterative, three pointers. Recursive: reverse rest, wire current. O(n). Reverse in groups of k: reverse each group, connect.

## Detect Cycle in Linked List

Floyd cycle detection: slow and fast pointers. O(n) time, O(1) space. Find cycle start: after meeting, one to head, both step 1.

## Remove Nth Node From End

Two pointers: first advances n steps, then both advance. When first reaches end, second is at node to remove. O(n).

## Add Two Numbers (Linked List)

Add digit by digit, carry. Handle different lengths. Dummy head for cleaner code. O(max(m,n)).

## LRU Cache

LRU: least recently used eviction. Hash map + doubly linked list. Map: key to node. List: order by access. Get: move to front. Put: add/update, evict last if full. O(1) get and put.

## Implement Trie

Trie: insert, search, startsWith. Each node: children map, is_end flag. O(m) per operation.

## Word Search (Backtracking)

Word search: find word in 2D grid. Backtracking: try each cell, DFS with visited. O(m*n*4^len). Prune when prefix not in trie.

## Number of Islands

Islands: connected 1s in 2D grid. DFS or BFS from each unvisited 1. O(m*n). Union-Find: O(m*n) with path compression.

## Clone Graph

Clone: BFS or DFS, map old to new nodes. Handle cycles. O(V+E). Copy node and neighbors recursively.

## Course Schedule

Course schedule: topological sort of prerequisites. DFS: detect cycle, return reverse postorder. Kahn: process in-degree zero. O(V+E).

## Implement Queue Using Stacks

Two stacks: push to one, pop from other (reverse when empty). Amortized O(1). Alternative: push O(n), pop O(1).

## Min Stack

Min stack: push, pop, getMin in O(1). Store (value, min_so_far) pairs. Or use auxiliary stack for mins.

## Valid Anagram

Anagram: same character count. Sort and compare: O(n log n). Count array: O(n). Hash map: O(n).

## Group Anagrams

Group by sorted string as key. O(n * k log k) for n strings, max length k. Or use character count tuple as key.

## Top K Frequent Elements

Bucket sort: array of lists by frequency. O(n). Heap: O(n log k). Quickselect: O(n) average.

## Product of Array Except Self

Two passes: left products, then right products. O(n) time, O(1) space (output excluded). No division.

## Maximum Subarray

Kadane: max_ending_here = max(arr[i], max_ending_here + arr[i]). O(n). Track start and end indices if needed.

## Maximum Product Subarray

Track max and min (negative can become max). Max = max(arr[i], max*arr[i], min*arr[i]). O(n).

## Find Minimum in Rotated Sorted Array

Binary search: compare mid with right. If mid < right, min in left half. Else in right half. O(log n).

## Search in Rotated Sorted Array

Binary search: determine which half is sorted. If target in sorted range, search there. Else other half. O(log n).

## Container With Most Water

Two pointers: start and end. Move pointer with smaller height. O(n). Greedy: always move toward potentially larger area.

## Trapping Rain Water

Two pointers or stack. Left/right max arrays: water at i = min(left_max[i], right_max[i]) - height[i]. O(n).

## Longest Substring Without Repeating

Sliding window: expand until duplicate, shrink from left. Hash set for characters in window. O(n).

## Longest Substring with At Most K Distinct

Sliding window with hash map for counts. Expand, shrink when distinct > k. O(n).

## Sliding Window Maximum

Deque: maintain decreasing order. Front is max. Remove when index outside window. O(n).

## Minimum Window Substring

Sliding window: expand until all chars found, shrink from left. Track count of each char needed. O(n).

## Substring with Concatenation

Find all starting indices of concatenation of words. Sliding window: check each position. O(n * m * k).

## Palindrome Partitioning

Backtracking: try each cut. DP: dp[i] = min cuts for prefix. O(n^2). Manacher for precomputation.

## Word Break

DP: dp[i] = can form prefix of length i. dp[i] = any dp[j] and s[j:i] in dict. O(n^2).

## House Robber

DP: dp[i] = max money for first i houses. dp[i] = max(dp[i-1], dp[i-2] + nums[i]). O(n).

## House Robber III (Tree)

Tree DP: return (rob_this, not_rob_this). rob_this = node + sum(not_rob children). not_rob = sum(max(rob, not_rob) of children).

## Coin Change

DP: dp[i] = min coins for amount i. dp[i] = min(dp[i-c] + 1). O(amount * coins). Variant: number of ways.

## Longest Increasing Subsequence

DP: dp[i] = LIS ending at i. O(n^2). Binary search: maintain active list. O(n log n).

## Maximum Length of Repeated Subarray

DP: dp[i][j] = longest common suffix. dp[i][j] = dp[i-1][j-1] + 1 if match. O(m*n).

## Edit Distance

DP: dp[i][j] = min cost to convert s1[:i] to s2[:j]. Insert, delete, replace. O(m*n).

## Wildcard Matching

DP: dp[i][j] = s[:i] matches p[:j]. ? matches one, * matches any. O(m*n).

## Regular Expression Matching

DP: dp[i][j] = s[:i] matches p[:j]. Handle * (zero or more of preceding). O(m*n).

## N-Queens

Backtracking: place queen in each row, check column and diagonal. O(n!). Pruning: isValid before placing.

## Sudoku Solver

Backtracking: try 1-9 for empty cell. Check row, column, box. O(9^m) for m empty cells.

## Generate Parentheses

Backtracking: add ( when open < n, add ) when close < open. O(4^n / sqrt(n)) Catalan.

## Combination Sum

Backtracking: try each candidate, recurse with remaining sum. Allow reuse: same index. No reuse: next index.

## Permutations

Backtracking: swap each element to front, recurse. O(n!). Alternative: build permutation with used set.

## Subsets

Backtracking: include or exclude each element. O(2^n). Bitwise: each bit = include or not. O(n * 2^n).

## Partition Equal Subset Sum

Subset sum: can we partition into two equal sums? DP: dp[i][j] = can form sum j with first i elements. O(n * sum).

## Target Sum

Add + or - to each number to get target. DP: dp[i][j] = ways to get j with first i elements. O(n * range).

## Binary Tree Maximum Path Sum

Tree DP: max path through node = node + max(0, left) + max(0, right). Return max(path through node, max(single branch)). O(n).

## Serialize and Deserialize Binary Tree

BFS or preorder with null markers. O(n). Reconstruct from preorder with null markers.

## Lowest Common Ancestor

LCA: binary lifting O(log n) per query. Tarjan's offline O(n + q). Recursive: if root is p or q return root; recurse left and right; if both non-null return root.

## Binary Tree Right Side View

BFS: last node of each level. DFS: visit right first, add when depth first seen. O(n).
