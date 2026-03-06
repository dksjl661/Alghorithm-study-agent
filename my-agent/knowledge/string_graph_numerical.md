# String Algorithms, Graph Algorithms, and Numerical Algorithms

## Aho-Corasick Algorithm

Aho-Corasick: multi-pattern matching. Build trie of patterns, add failure links (like KMP). Search text in one pass. O(n + m + z) for text length n, pattern total m, z matches. Used in virus scanning, intrusion detection.

## KMP Failure Function

KMP prefix function (failure function): longest proper prefix that is also suffix. Build: O(m). pi[i] = length of longest border of prefix of length i+1. Enables O(n) text scan.

## Rabin-Karp Rolling Hash

Rabin-Karp: rolling hash. Hash of window = (hash - old_char * base^(m-1)) * base + new_char. O(n+m) average. Can have false positives; verify with comparison. Good for multiple pattern lengths.

## Z-Algorithm

Z-algorithm: Z[i] = longest substring of s starting at i that is also prefix of s. Build Z-array: O(n). Pattern matching: O(n+m). Simpler than KMP for some problems.

## Boyer-Moore Algorithm

Boyer-Moore: scan pattern from right to left. Bad character rule: shift by pattern length if character not in pattern. Good suffix rule: shift by matched suffix. Often sublinear in practice. O(n/m) best case.

## Longest Palindromic Substring

Manacher's algorithm: O(n) with center expansion and reuse. LPS array. DP: O(n^2) with dp[i][j] = palindrome from i to j.

## Suffix Array Construction

Suffix array: sort suffixes. O(n log n) with binary search on prefixes. O(n) with SA-IS or DC3. LCP array: longest common prefix of adjacent suffixes.

## Burrows-Wheeler Transform

BWT: reversible transform. Sort rotations, take last column. Used in bzip2. Enables run-length encoding. Inverse: LF mapping.

## Lempel-Ziv Compression

LZ77: sliding window, find longest match. LZ78: dictionary of phrases. LZW: LZ78 variant. Foundation of gzip, PNG.

## Maximum Flow

Max flow: maximum amount from source to sink. Ford-Fulkerson: find augmenting path, repeat. Edmonds-Karp: BFS for path gives O(VE^2). Dinic: O(V^2 E). Push-relabel: O(V^3).

## Ford-Fulkerson Method

Ford-Fulkerson: while augmenting path exists, push flow. Residual capacity. Max flow = min cut. May not terminate with irrational capacities. Pseudo-polynomial.

## Edmonds-Karp

Edmonds-Karp: Ford-Fulkerson with BFS for shortest augmenting path. O(VE^2). Guarantees polynomial time.

## Dinic's Algorithm

Dinic: level graph + blocking flow. O(V^2 E). In unit capacity: O(E sqrt(V)). Often fastest in practice.

## Min-Cut Max-Flow Theorem

Max flow value = min cut capacity. Min cut: partition (S, T) with source in S, sink in T, minimum capacity sum of edges from S to T.

## Bipartite Matching

Bipartite matching: max flow from source to left, left to right (capacity 1), right to sink. Hopcroft-Karp: O(E sqrt(V)). Augmenting path algorithm.

## Hungarian Algorithm

Hungarian algorithm: assignment problem (min cost perfect matching in bipartite). O(n^3). Kuhn-Munkres. Modify potentials.

## Bellman-Ford Negative Cycle

Bellman-Ford: relax V-1 times. If V-th relaxation improves, negative cycle exists. Can find cycle by tracing predecessors.

## Johnson's Algorithm

Johnson: all-pairs shortest path with negative weights. Reweight with Bellman-Ford, then Dijkstra from each vertex. O(V^2 log V + VE). Converts negative to non-negative.

## A* Search

A*: best-first search with heuristic f(n) = g(n) + h(n). Admissible heuristic: never overestimate. Consistent: h(n) <= c(n,n') + h(n'). Optimal if admissible. Used in pathfinding, games.

## Bidirectional Search

Bidirectional: search from start and goal simultaneously. Meet in middle. Reduces space and time for many problems. O(b^(d/2)) instead of O(b^d).

## Yen's K Shortest Paths

Yen's algorithm: find k shortest paths. Deviation from each previous path. O(kn(m + n log n)). Used in routing.

## Strongly Connected Components

SCC: maximal subgraph with path between any two vertices. Kosaraju: two DFS. Tarjan: one DFS with low-link. O(V+E). Applications: 2-SAT, dependency graph.

## Articulation Points

Articulation point: vertex whose removal increases connected components. DFS: low-link values. O(V+E). Bridge: edge whose removal increases components.

## Euler Path and Circuit

Euler circuit: visits every edge once, returns to start. Exists iff all vertices even degree. Euler path: start and end different; exists iff exactly 0 or 2 odd degree. Hierholzer's algorithm: O(E).

## Hamiltonian Path

Hamiltonian path: visits every vertex once. NP-complete. Backtracking, dynamic programming O(n^2 * 2^n). No efficient general algorithm.

## Traveling Salesman Problem

TSP: shortest tour visiting all cities. NP-hard. DP: O(n^2 * 2^n). Approximation: 2-opt, Christofides (1.5x for metric). Branch and bound.

## Fast Fourier Transform (FFT)

FFT: O(n log n) polynomial multiplication. Cooley-Tukey. Divide and conquer with roots of unity. Applications: signal processing, convolution, large integer multiplication.

## Karatsuba Multiplication

Karatsuba: multiply n-digit numbers in O(n^1.585). Split: (a+b)(c+d) - ac - bd = ad + bc. Reduces 4 multiplications to 3.

## Strassen Matrix Multiplication

Strassen: multiply matrices in O(n^2.807). 7 multiplications instead of 8. Divide into 2x2 blocks. Practical for large matrices.

## Modular Exponentiation

Binary exponentiation: a^b mod m in O(log b). Square and multiply. a^b = (a^(b/2))^2 or a * a^(b-1).

## Extended Euclidean Algorithm

Extended Euclidean: find x, y such that ax + by = gcd(a,b). Modular inverse: inverse of a mod m exists iff gcd(a,m)=1. O(log min(a,b)).

## Sieve of Eratosthenes

Sieve: mark multiples of primes. O(n log log n). Find all primes up to n. Optimizations: segmented sieve, wheel sieve.

## Miller-Rabin Primality

Miller-Rabin: probabilistic primality test. O(k log^3 n) for k rounds. No false negatives; small false positive rate. Deterministic for small n.

## Pollard's Rho

Pollard's rho: factorization using cycle detection. O(sqrt(p)) where p is smallest prime factor. Uses Floyd cycle detection.

## Newton's Method

Newton's method: iterative root finding. x_{n+1} = x_n - f(x_n)/f'(x_n). Quadratic convergence. Square root: x_{n+1} = (x_n + n/x_n)/2.

## Binary Search on Answer

When answer is monotonic, binary search on answer. Check function: feasible or not. O(log range) iterations. Used for optimization problems.

## Ternary Search

Ternary search: find maximum of unimodal function. Divide into thirds. O(log n) iterations. Alternative to binary search for unimodal.
