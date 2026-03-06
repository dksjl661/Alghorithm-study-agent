# Algorithm Analysis and Theory

## Asymptotic Notation

Big O: f(n) = O(g(n)) means f(n) <= c*g(n) for n > n0. Upper bound. Big Omega: lower bound, f = Ω(g) means f >= c*g. Big Theta: tight bound, f = Θ(g) means f = O(g) and f = Ω(g). Little o: f = o(g) means f/g -> 0. Little omega: f = ω(g) means f/g -> infinity.

## Recurrence Relations

Recurrence: equation defining T(n) in terms of smaller inputs. Substitution: guess and verify. Recursion tree: visualize levels, sum. Master theorem: T(n) = aT(n/b) + f(n). Akra-Bazzi: generalization for non-standard recurrences.

## Master Theorem Cases

Case 1: f(n) = O(n^(log_b a - ε)), then T(n) = Θ(n^(log_b a)). Case 2: f(n) = Θ(n^(log_b a)), then T(n) = Θ(n^(log_b a) log n). Case 3: f(n) = Ω(n^(log_b a + ε)) and af(n/b) <= cf(n), then T(n) = Θ(f(n)). Does not cover all: e.g. f(n) = Θ(n^(log_b a) log^k n).

## Amortized Analysis

Amortized: average cost per operation over worst-case sequence. Aggregate: total cost / n. Accounting: assign amortized cost, use credits. Potential: Φ(D) before and after, amortized = actual + ΔΦ. Dynamic array: O(1) amortized append. Binary counter: O(1) amortized increment.

## Potential Method

Potential function Φ maps state to nonnegative real. Amortized cost = actual cost + Φ(D') - Φ(D). Choose Φ so amortized costs are small. Sum telescopes: total actual = sum amortized - Φ(final) + Φ(initial).

## Competitive Analysis

Competitive ratio: online algorithm cost / optimal offline cost. Paging: LRU is k-competitive for k pages. Sleator-Tarjan theorem. No deterministic algorithm better than k-competitive.

## Randomized Algorithms

Randomized: use random choices. Las Vegas: always correct, running time random. Monte Carlo: may have error, fixed time. Quicksort with random pivot: O(n log n) expected. Randomized selection: O(n) expected.

## Probabilistic Analysis

Probabilistic: assume input distribution. Average-case vs worst-case. Birthday paradox: O(sqrt(n)) for collision. Hashing: uniform hashing assumption.

## Approximation Algorithms

Approximation: polynomial algorithm with guaranteed ratio. Vertex cover: 2-approximation. TSP metric: Christofides 1.5-approximation. Set cover: ln n approximation. PTAS: (1+ε)-approximation, time poly(n) for fixed ε.

## PTAS and FPTAS

PTAS: polynomial-time approximation scheme. For any ε > 0, (1+ε)-approximation in poly(n) time. FPTAS: poly(n, 1/ε). Knapsack has FPTAS. Some problems have PTAS but not FPTAS.

## NP-Completeness

NP-complete: in NP and every NP problem reduces to it. Cook-Levin: SAT is NP-complete. To prove: show in NP, reduce from known NP-complete. Reduction: transform instance of A to instance of B in poly time.

## NP-Hard

NP-hard: at least as hard as NP-complete. May not be in NP (e.g. halting problem). Optimization version of NP-complete is NP-hard. TSP, knapsack optimization.

## Reduction Techniques

Karp reduction: A <= B means B as hard as A. Show A in NP, give poly reduction to known NP-complete. Restriction: B is special case of A. Local replacement: replace components. Component design: construct gadgets.

## P vs NP Problem

P: solvable in polynomial time. NP: verifiable in polynomial time. P ⊆ NP. Open: P = NP? Million dollar question. Most believe P ≠ NP. Implications for cryptography, optimization.

## Space Complexity

L: logarithmic space. NL: nondeterministic log space. PSPACE: polynomial space. L ⊆ NL ⊆ P ⊆ NP ⊆ PSPACE. Savitch: NSPACE(f) ⊆ SPACE(f^2). PSPACE-complete: QBF.

## Decision vs Optimization

Decision: yes/no answer. Optimization: find best value. Often equivalent: binary search on answer. Decision in NP implies optimization is NP-hard.

## Parameterized Complexity

Parameter k besides input size n. FPT: O(f(k) * poly(n)). Kernelization: reduce to size f(k). Fixed-parameter tractable. Vertex cover: O(2^k * n). Different from approximation.

## Branch and Bound

Branch and bound: systematic search with pruning. Branch: split into subproblems. Bound: prune if bound worse than best found. Used for TSP, integer programming. Combines enumeration with pruning.

## Local Search

Local search: start with solution, improve by local moves. 2-opt for TSP: swap two edges. Simulated annealing: allow worse moves with probability. May get stuck in local optimum.

## Simulated Annealing

Simulated annealing: accept worse move with probability exp(-ΔE/T). T decreases over time. Escapes local optima. Cooling schedule critical. Used for optimization, placement.

## Genetic Algorithms

Genetic algorithms: population of solutions, selection, crossover, mutation. Evolutionary approach. Not guaranteed optimal. Used for complex optimization.

## Greedy Approximation Proofs

Prove approximation ratio: show greedy solution <= c * optimal. Exchange argument: any optimal can be transformed to greedy without worsening. Dual fitting: linear programming dual.

## Linear Programming

LP: maximize c^T x subject to Ax <= b, x >= 0. Simplex: exponential worst case, good in practice. Ellipsoid: polynomial. Duality: max = min for primal and dual. Used for scheduling, flow, approximation.

## Integer Linear Programming

ILP: LP with integer variables. NP-hard. Relaxation: drop integrality, round solution. Branch and cut. Used for scheduling, resource allocation.

## Duality

LP duality: primal max c^T x, dual min b^T y. Weak duality: primal <= dual. Strong duality: equal if both feasible. Complementary slackness. Used in approximation proofs.
