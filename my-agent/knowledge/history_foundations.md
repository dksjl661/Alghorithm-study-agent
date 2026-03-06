# History and Foundations of Data Structures and Algorithms

## Origins of Algorithms

The word algorithm derives from the name of Persian mathematician Muhammad ibn Musa al-Khwarizmi (9th century), whose works introduced Hindu-Arabic numerals and systematic methods for solving equations. The concept of an algorithm as a finite, well-defined procedure predates computers. Euclid's algorithm for GCD (circa 300 BCE) is one of the oldest algorithms still in use today.

## Turing Machine

Alan Turing (1936) defined the Turing machine: an abstract model of computation with infinite tape, read-write head, and finite state control. A Turing machine can compute any function that is algorithmically computable (Church-Turing thesis). Halting problem: no algorithm can determine whether an arbitrary program halts. Turing completeness: a system can simulate a Turing machine.

## Lambda Calculus

Alonzo Church (1936) developed lambda calculus as a formal system for defining functions. Lambda calculus is Turing-complete and equivalent to Turing machines. Used as foundation for functional programming. Church numerals, Y combinator for recursion. Influenced Lisp, Haskell, and modern functional languages.

## Von Neumann Architecture

John von Neumann (1945) described stored-program computer architecture: program and data in same memory. Fetch-decode-execute cycle. Enables general-purpose computation. Influenced all modern computer design. Von Neumann bottleneck: memory bandwidth limits performance.

## Big O Notation

Paul Bachmann (1894) introduced O-notation; Edmund Landau popularized it. Big O describes upper bound: f(n) = O(g(n)) means f grows at most as fast as g. Big Omega: lower bound. Big Theta: tight bound. Little o: strictly smaller. Used for asymptotic analysis of algorithms. Standard notation: O(1), O(log n), O(n), O(n log n), O(n^2), O(2^n), O(n!).

## Computational Complexity Theory

Complexity theory studies resources (time, space) required to solve problems. P: problems solvable in polynomial time. NP: problems verifiable in polynomial time. NP-complete: hardest problems in NP; if any is in P, all are. NP-hard: at least as hard as NP-complete. Cook-Levin theorem (1971): SAT is NP-complete. Reduction: transform one problem to another to prove hardness.

## Donald Knuth

Donald Knuth (1938-) authored The Art of Computer Programming. Introduced rigorous analysis of algorithms. Created TeX, METAFONT. Knuth-Morris-Pratt string matching. Analysis of hashing. Big-O notation standardization. Emphasized mathematical correctness and elegance.

## Edsger Dijkstra

Edsger Dijkstra (1930-2002) invented Dijkstra's shortest path algorithm (1956). Contributed to structured programming. Semaphore for concurrency. Shortest path first. Dijkstra's algorithm: greedy, non-negative weights, O(E log V) with heap. Influenced algorithm design and software engineering.

## Tony Hoare

Tony Hoare (1934-) invented quicksort (1959). Developed Hoare logic for program correctness. CSP (Communicating Sequential Processes) for concurrency. Quicksort: divide and conquer, average O(n log n), pivot selection critical. Null reference: called it his billion-dollar mistake.

## John McCarthy

John McCarthy (1927-2011) invented Lisp (1958). Introduced recursion, garbage collection, conditional expressions. Lisp pioneered recursion as primary control structure. Influenced AI research and functional programming. Recursion in programming languages.

## Robert Tarjan

Robert Tarjan (1948-) developed Tarjan's SCC algorithm, Union-Find with path compression. Tarjan's algorithm for strongly connected components. Fibonacci heap. Amortized analysis. Won Turing Award for graph algorithms and data structures.

## Adelson-Velsky and Landis

G.M. Adelson-Velsky and E.M. Landis (1962) invented AVL tree. First self-balancing binary search tree. Balance factor: height difference of subtrees. Rotations: LL, RR, LR, RL. Guarantees O(log n) operations. Foundation for balanced tree research.

## Rudolf Bayer

Rudolf Bayer (1972) invented red-black tree with Ed McCreight. B-tree (1972) for disk-based storage. Red-black tree: balanced BST with color invariants. B-tree: multi-way tree for databases. Used in database systems, file systems.

## Michael Fredman and Robert Tarjan

Fredman and Tarjan (1987) invented Fibonacci heap. Amortized O(1) decrease-key, O(log n) extract-min. Improves Dijkstra to O(E + V log V). Theoretical importance; binary heap often faster in practice. Sophisticated amortized analysis.

## Invention of Hash Table

Hans Peter Luhn (1953) used hash coding for indexing. IBM researchers developed hash tables for information retrieval. Hash function maps keys to indices. Collision resolution: chaining, open addressing. Fundamental for databases, caches, sets.

## Invention of Linked List

Linked list concept emerged in 1955-1956. Allen Newell, Cliff Shaw, Herbert Simon used linked structures in IPL (Information Processing Language). Each node stores data and pointer to next. Dynamic allocation, no need for contiguous memory. Foundation for dynamic data structures.

## Invention of Stack and Queue

Stack: Alan Turing (1946) used for subroutine calls. LIFO for expression evaluation. Queue: early batch processing systems. FIFO for task scheduling. Both fundamental to computer architecture and algorithms.

## Algorithm Design Paradigms

Brute force: try all possibilities. Greedy: local optimal choices. Divide and conquer: split, solve, combine. Dynamic programming: overlapping subproblems. Backtracking: try, backtrack if fail. Branch and bound: prune search space. Reduction: transform to known problem.

## Correctness Proofs

Loop invariant: property true before each iteration. Precondition and postcondition. Induction for recursion. Termination: prove progress toward base case. Hoare logic: {P} S {Q}. Formal verification of algorithms.

## Amortized Analysis

Amortized analysis: average cost over sequence of operations. Aggregate method: total cost divided by operations. Accounting method: assign credits. Potential method: potential function. Binary counter: n increments O(n) total, O(1) amortized per increment. Dynamic array: doubling gives O(1) amortized append.
