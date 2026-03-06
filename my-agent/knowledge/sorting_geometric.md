# Sorting Algorithms and Geometric Algorithms

## Shell Sort

Shell sort (1959, Donald Shell): generalization of insertion sort. Sort elements at gaps (n/2, n/4, ...). Reduces inversions. Gap sequence affects performance. Best known: Knuth's 1,4,13,40... or Sedgewick's. Average O(n^1.25) to O(n^1.5). Not stable.

## Comb Sort

Comb sort: improvement of bubble sort. Compare elements at gap; gap shrinks by factor 1.3. Removes turtles (small values at end). O(n^2) worst, O(n log n) average. Simple, in-place.

## Cocktail Shaker Sort

Cocktail sort: bidirectional bubble sort. Pass forward then backward. Moves small elements up faster. O(n^2). Slight improvement over bubble.

## Gnome Sort

Gnome sort: like insertion sort. Compare with neighbor, swap if wrong order, step back. O(n^2). Simple, few lines of code.

## Tim Sort

Tim sort (Tim Peters, 2002): hybrid of merge sort and insertion sort. Used in Python, Java. Finds runs (ascending/descending), uses insertion sort for small runs, merge for combining. O(n log n), stable. Optimized for real-world data.

## Introsort

Introsort (Musser, 1997): hybrid quicksort. Starts with quicksort, switches to heapsort if recursion too deep. Guarantees O(n log n). Used in C++ std::sort.

## Patience Sorting

Patience sort: deal cards into piles, each pile decreasing. Number of piles = length of longest increasing subsequence. Can extract LIS. O(n log n) with binary search.

## Pigeonhole Sort

Pigeonhole sort: when range of keys is small (0 to k). Create k+1 holes, place elements, concatenate. O(n + k). Not comparison-based.

## Bucket Sort

Bucket sort: distribute into buckets by range, sort each bucket (insertion sort), concatenate. O(n + k) when uniform distribution. Good for floating point in [0,1).

## Proxmap Sort

Proxmap sort: maps keys to positions. Uses auxiliary array. O(n) when keys uniformly distributed.

## Flash Sort

Flash sort: estimate distribution, permute in one pass. O(n) when distribution known. Minimal comparisons.

## Pancake Sorting

Pancake sort: can only flip prefix. Find max, flip to front, flip to position. O(n^2) flips. Bill Gates published improved bound.

## Stooge Sort

Stooge sort: recursive, if first > last swap; if 3+ elements, recursively sort first 2/3, last 2/3, first 2/3. O(n^2.71). Educational.

## Bogosort

Bogosort: shuffle until sorted. O(n!) average, unbounded worst. Permutation sort. Joke algorithm.

## Lower Bound Comparison Sort

Any comparison-based sort requires Ω(n log n) comparisons. Decision tree has n! leaves (permutations). Height at least log2(n!) = Ω(n log n). Radix and counting sort beat this by not comparing.

## Convex Hull

Convex hull: smallest convex polygon containing all points. Graham scan: O(n log n) - sort by angle, process with stack. Jarvis march (gift wrapping): O(nh) where h is hull size. Quickhull: O(n log n) average.

## Graham Scan

Graham scan for convex hull: pick lowest point, sort others by polar angle, process with stack. Left turn: keep; right turn: pop. O(n log n) for sort. Robust with collinear handling.

## Jarvis March

Jarvis march (gift wrapping): start from leftmost, repeatedly find point with smallest polar angle. O(nh). Output-sensitive. Good when hull is small.

## Closest Pair of Points

Closest pair: divide and conquer. Split by x, recurse, combine. Strip of width 2d around midline, sort by y, check 7 neighbors. O(n log n).

## Line Segment Intersection

Line sweep: sweep vertical line, maintain active segments. Event points: segment endpoints. O((n+k) log n) for n segments, k intersections. Bentley-Ottmann algorithm.

## Voronoi Diagram

Voronoi diagram: partition plane by nearest site. Fortune's sweep: O(n log n). Dual to Delaunay triangulation. Applications: nearest neighbor, mesh generation.

## Delaunay Triangulation

Delaunay triangulation: triangulation maximizing minimum angle. Dual of Voronoi. O(n log n) with sweep. Used in mesh generation, interpolation.

## Range Minimum Query (RMQ)

RMQ: find minimum in range. Sparse table: O(n log n) preprocess, O(1) query. Segment tree: O(n) build, O(log n) query. Cartesian tree + LCA: O(n) preprocess, O(1) query.

## Sparse Table

Sparse table for RMQ: precompute min for all ranges of length 2^k. Query: combine two overlapping ranges. O(n log n) space, O(1) query. Idempotent operations (min, max, gcd).

## Sweep Line Algorithm

Sweep line: imaginary line sweeps across plane. Process events (points, segment endpoints). Maintain data structure (BST, segment tree). Used for intersection, visibility, many geometry problems.

## Bentley-Ottmann

Bentley-Ottmann: sweep line for segment intersection. O((n+k) log n). Maintain active segments in BST. Handle three event types.

## Point in Polygon

Point in polygon: ray casting - count intersections of horizontal ray with polygon. Odd = inside. O(n). Winding number: sum of signed angles. More robust.

## Polygon Area

Shoelace formula: area = |sum(x_i(y_{i+1} - y_{i-1}))| / 2. O(n). Signed area for orientation.

## Rotating Calipers

Rotating calipers: two parallel lines rotating around convex polygon. Finds diameter (farthest pair), width, minimum area bounding rectangle. O(n).

## Half-Plane Intersection

Half-plane intersection: intersection of n half-planes. Convex polygon or empty. O(n log n) with sort and incremental. Used in linear programming.

## 2D Range Tree

2D range tree: primary tree by x, secondary trees by y. Range query: O(log^2 n + k). Fractional cascading improves to O(log n + k).

## k-Nearest Neighbors

k-NN: find k closest points. k-d tree: O(sqrt(n) + k) average. Brute force: O(n). Space partitioning for high dimensions.

## Minimum Enclosing Circle

Smallest circle enclosing points. Welzl's algorithm: O(n) expected with randomization. Randomized incremental.

## Polygon Triangulation

Triangulate polygon: O(n) with ear clipping. Every polygon has at least two ears. Used for rendering, mesh generation.
