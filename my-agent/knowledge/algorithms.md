# Algorithms Reference

## Sorting Algorithms Comparison

Comparison sorts: merge O(n log n) stable, quicksort O(n log n) avg not stable, heapsort O(n log n) not stable, insertion O(n^2) stable good for small/sorted. Non-comparison: counting O(n+k), radix O(d*n), bucket O(n). Lower bound for comparison sort: Ω(n log n). Stable sort preserves relative order of equal elements.

## Search Algorithms

Linear search: O(n) for unsorted. Binary search: O(log n) for sorted array. Jump search: O(sqrt n) by jumping sqrt(n) steps. Interpolation search: O(log log n) for uniformly distributed. Exponential search: for unbounded arrays, find range then binary search. Ternary search: divide into three parts for unimodal functions.

## Recursion Base Case

Every recursive function must have base case to prevent infinite recursion. Base case returns without recursive call. Examples: factorial(0)=1, fibonacci(0)=0 fib(1)=1, list length empty list=0. Missing base case causes stack overflow. Ensure recursive case progresses toward base case.

## Memoization

Memoization caches results of expensive function calls. Top-down DP: recursive with cache. Before computing, check cache; after computing, store in cache. Transforms exponential to polynomial time. Example: Fibonacci O(2^n) to O(n). Python: @lru_cache or manual dict.

## Tabulation

Tabulation is bottom-up DP. Fill table iteratively from base cases. No recursion, avoids stack overflow. Often more space efficient. Order of filling matters: dependencies must be computed first. Example: Fibonacci dp[i] = dp[i-1] + dp[i-2], fill from 0 to n.

## Greedy Choice Property

A problem has greedy choice property if locally optimal choice leads to global optimum. Prove by: show greedy choice is in some optimal solution (exchange argument), or show optimal substructure. Not all problems have it: 0-1 knapsack fails, fractional knapsack has it.

## Master Theorem

For T(n) = aT(n/b) + f(n): Case 1: if f(n) = O(n^(log_b a - ε)), then T(n) = Θ(n^(log_b a)). Case 2: if f(n) = Θ(n^(log_b a)), then T(n) = Θ(n^(log_b a) log n). Case 3: if f(n) = Ω(n^(log_b a + ε)) and regularity, then T(n) = Θ(f(n)). Does not apply to all recurrences.

## Backtracking Template

def backtrack(path, choices): if is_complete(path): result.add(path); return. for choice in choices: if is_valid(choice): path.add(choice); backtrack(path, choices); path.remove(choice). Pruning: skip invalid choices early. Used for permutations, combinations, subset sum, N-Queens, Sudoku.

## BFS vs DFS

BFS: queue, level order, shortest path in unweighted graph. DFS: stack/recursion, explores depth first. BFS uses more memory (stores level). DFS may use less (stack depth). Cycle detection: DFS with parent. Connectivity: both work. Topological sort: DFS. Shortest path: BFS for unweighted.

## Shortest Path Algorithms

Dijkstra: non-negative weights, O(E log V). Bellman-Ford: negative weights, O(VE). Floyd-Warshall: all pairs, O(V^3). BFS: unweighted, O(V+E). A*: heuristic for graphs, best-first search. Choose based on graph properties and requirements.

## Minimum Spanning Tree

MST connects all vertices with minimum total edge weight. Prim: grow from one vertex, add min edge. Kruskal: sort edges, add if no cycle. Both produce same total weight (may differ in edges). Applications: network design, clustering, approximation for TSP.

## String Algorithms

Naive pattern matching: O(n*m). KMP: O(n+m) with prefix function. Rabin-Karp: O(n+m) average with rolling hash. Z-algorithm: O(n) for pattern in text. Suffix array: O(n log n) build, supports many queries. Applications: search, compression, bioinformatics.

## Number Theory

GCD: Euclidean algorithm O(log min(a,b)). Modular exponentiation: binary exponentiation O(log n). Prime sieve: Eratosthenes O(n log log n). Modular inverse: extended Euclidean. LCM(a,b) = a*b/GCD(a,b). Fermat's little theorem for inverse when mod is prime.

## Combinatorics

Permutations: n! arrangements. Combinations: C(n,k) = n!/(k!(n-k)!). With repetition: n^k permutations, C(n+k-1,k) combinations. Inclusion-exclusion for union of sets. Catalan numbers: valid parentheses, binary trees, paths.

## Bitmask DP

Use integer bits to represent subset. Set i: mask | (1<<i). Unset: mask & ~(1<<i). Check: mask & (1<<i). Toggle: mask ^ (1<<i). Iterate subsets: for i in range(1<<n). Traveling salesman with DP: dp[mask][i] = min cost visiting mask cities ending at i.

## Sliding Window Maximum

Find max in each sliding window of size k. Deque approach: maintain deque of indices in decreasing order of values. Front is max. When window slides, remove indices outside window, add new element (remove smaller from back). O(n) time. Similarly for minimum.

## Kadane's Algorithm

Maximum subarray sum: keep current sum, reset to 0 when negative. max_ending_here = max(arr[i], max_ending_here + arr[i]). max_so_far = max(max_so_far, max_ending_here). O(n) time, O(1) space. Variants: maximum product subarray, circular array.

## Reservoir Sampling

Select k random items from stream of unknown size n. Each item has equal probability k/n of being selected. Algorithm: keep reservoir of k items. For item i (0-indexed), with probability k/(i+1) replace random reservoir item. Used for random sampling from large datasets.

## Morris Traversal

Inorder tree traversal with O(1) space (no stack). Uses threaded binary tree: use null right pointers to point to inorder successor. Find predecessor of current, link to current, traverse left. Restore tree when done. O(n) time, O(1) space.

## Manacher's Algorithm

Finds longest palindromic substring in O(n). Uses center expansion with clever reuse of previously computed info. Maintains array of palindrome radii. Linear time by avoiding redundant comparisons. Applications: palindrome problems, string analysis.

## Edit Distance (Levenshtein)

Minimum operations (insert, delete, replace) to transform string A to B. DP: dp[i][j] = min cost to convert A[0..i] to B[0..j]. Recurrence: dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost). Cost 0 if A[i]==B[j]. O(m*n) time and space.

## Coin Change

Minimum coins to make amount: dp[i] = min coins for amount i. dp[i] = min(dp[i-c]+1) for each coin c. Initialize dp[0]=0, dp[i]=inf. Variant: number of ways: dp[i] += dp[i-c]. Unbounded vs bounded (0-1) knapsack style.

## Matrix DP

Common patterns: unique paths (dp[i][j] = dp[i-1][j] + dp[i][j-1]), min path sum, maximal square, longest common subsequence in 2D. Often can optimize space to O(n) or O(min(m,n)) by reusing rows. Direction: top-left to bottom-right or vice versa.

## Tree DP

DP on trees: often compute for subtree, combine for parent. Examples: max path sum (path through node = left + right + node), tree diameter (longest path), house robber III (alternate levels). Post-order traversal: process children before parent.

## Graph Coloring

K-coloring: assign colors so no adjacent vertices same color. Chromatic number: minimum colors. Greedy: color in order, use smallest available. Backtracking: try colors, backtrack if conflict. Bipartite: 2-colorable, use BFS/DFS to check. Applications: scheduling, register allocation.
