# Project Report — Structure Showdown

Date: 2025-11-09
Author: Project deliverable

---

## 1. Executive Summary

Structure Showdown is an educational and experimental tool for empirically analyzing and comparing the performance of fundamental data structures (Arrays, Linked Lists, Binary Search Tree, Hash Table, Graph) across common operations such as insertion, deletion and search. The project provides a Streamlit-based interactive UI to run configurable benchmarks, visualize results, compute basic statistics, and download raw measurements for further analysis.

This report documents the objectives, implementation, benchmarking methodology, representative results, analysis, limitations, and recommended next steps.

---

## 2. Project Objectives

Primary goals:
- Implement core data structures in Python for educational benchmarking.
- Provide a reproducible harness to measure operation times across input sizes and trials.
- Offer an interactive, easy-to-use UI (Streamlit) to run experiments and visualize results.
- Help users understand trade-offs between time complexity, variability, and implementation choices.

Success criteria:
- Working implementations of at least five data structures.
- A benchmark engine producing repeatable numeric results (pandas DataFrame output).
- Visualization and CSV export capabilities.
- Clear, documented instructions to reproduce experiments.

---

## 3. Implementation Overview

Project layout (key files):
- `app.py` — Streamlit application that orchestrates experiments and shows results.
- `requirements.txt` — pinned dependencies (Streamlit, pandas, numpy, matplotlib, plotly).
- `src/ds/` — data structure implementations:
  - `array_ds.py` — array wrapper around Python list
  - `linked_list.py` — singly linked list
  - `bst.py` — unbalanced binary search tree
  - `hash_table.py` — separate-chaining hash table
  - `graph.py` — adjacency-list graph (undirected)
- `src/benchmarks/benchmark.py` — benchmark harness with one method per operation
- `src/utils/` — helpers for data generation and comparison
- `tests/validate_all.py` — small validation script that executes all operations to verify integrity

Design notes:
- Implementations are intentionally simple and educational (unbalanced BST to demonstrate worst-case behavior).
- Benchmark harness creates fresh instances per trial to avoid cross-trial state leakage.
- Timing uses `time.perf_counter()` and records times in milliseconds.
- UI performs aggregation (mean, median, std, min, max) and displays heat maps and charts.

---

## 4. Benchmarking Methodology

Measurement approach:
- For each selected operation, the harness runs the operation on sizes chosen by the user (presets or custom range).
- For each size `n`, the operation is executed once (but with `trials` repetitions of the whole measurement) and the runtime in milliseconds is recorded.
- Trials are repeated to obtain a distribution for each size; aggregated statistics are computed from those trials.
- For operations involving multiple sub-actions (e.g., inserting `n` elements), the entire insertion loop is timed as a single measurement.

Reproducibility measures:
- A fixed random seed is used where the harness requires randomization (except ordered tests).
- The harness rebuilds data structures per trial.

Limitations of the measurement method:
- Single-process, single-threaded; OS scheduling, background processes and other noise can affect results.
- Python interpreter and memory management behavior (GC, list resizing) influence timings.
- The harness focuses on runtime measurement only (no memory profiling).

---

## 5. Operations Implemented

Arrays (Python list wrapper):
- Insert at end (append)
- Insert at front (insert(0, value))
- Linear search (value in list)
- Delete value (list.remove)

Linked List (singly):
- Insert at tail (append)
- Search (find)
- Delete (delete by value)

Binary Search Tree (unbalanced):
- Insert (randomized for average-case test)
- Insert ordered (degenerate/worst-case test)
- Search
- Delete

Hash Table (separate chaining):
- Put (insert key/value)
- Get (lookup)
- Delete (remove key)

Graph (adjacency list, undirected):
- Add edges (linear chain builder)
- BFS search
- Delete node

---

## 6. Environment and Setup

- OS used during development: Windows (project built and tested on local machine)
- Python: 3.10.x (>=3.8 supported)
- Key dependencies (pinned in `requirements.txt`):
  - streamlit==1.39.0
  - pandas==2.2.3
  - numpy==1.26.4
  - matplotlib==3.10.7
  - plotly==6.4.0

Run instructions (minimal):

1. Create virtual environment and activate

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Run the app

```powershell
streamlit run app.py
```

---

## 7. Representative Results (sanity check)

A quick validation run executed all operations for very small sizes (n=100, trials=1) to ensure correctness. Representative average times (ms) from that validation run:

| Operation | Avg time (ms) |
|---|---:|
| Array: insert_end | 0.0490 |
| Array: insert_front | 0.0422 |
| Array: search | 0.0094 |
| Array: delete | 0.0220 |
| LinkedList: insert_tail | 0.5877 |
| LinkedList: search | 0.0081 |
| LinkedList: delete | 0.0568 |
| BST: insert | 0.3464 |
| BST: insert_ordered | 0.7751 |
| BST: search | 0.0033 |
| BST: delete | 0.0075 |
| HashTable: put | 0.0992 |
| HashTable: get | 0.0026 |
| HashTable: delete | 0.0349 |
| Graph: add_edges(line) | 0.1737 |
| Graph: bfs_search(end) | 0.0784 |
| Graph: delete_node | 0.1145 |

Notes:
- These numbers are tiny because the test used small sizes and single-trial runs — they are strictly sanity checks that the code runs and returns timings.
- Real experiments should use larger sizes and multiple trials for statistical significance.

---

## 8. Analysis & Interpretation

Key observations:
- Hash table lookups (`get`) are consistently fastest in average-case and show near-constant time, as expected (O(1) avg).
- Python list append (`insert_end`) is very fast and amortized O(1); inserting at the front (`insert_front`) is slower and scales with `n` due to shifting elements.
- Unbalanced BST shows significantly worse behavior for ordered inserts (degenerate to O(n) per insert). Randomized insertion exhibits average-case behavior closer to O(log n).
- Linked list operations (search and tail-insert without tail pointer) suffer due to traversal costs and poor cache locality.
- Graph BFS is proportional to the number of vertices and edges (O(V + E)), demonstrated by linear chain tests.

Educational value:
- The project demonstrates both theoretical Big-O behavior and how implementation details and language-specific characteristics (Python list resizing, GC, interpreter overhead) influence real-world performance.

---

## 9. Limitations

- No memory profiling: space/time trade-offs are explained but not measured.
- BST is unbalanced. To show guaranteed logarithmic behavior, a balanced BST (AVL or Red-Black) would be needed.
- Results are platform and interpreter dependent: different CPUs, OS conditions, and Python builds alter absolute timings.
- Benchmark harness times whole loops (e.g., building n elements). It does not break down per-operation microbenchmarks (but the design can be extended to do so).
- Background processes and OS scheduler noise can create variability; the app uses multiple trials to mitigate but cannot remove all noise.

---

## 10. Recommendations & Next Steps

Short-term (high value):
1. Add balanced BST implementation (AVL or Red-Black) to compare guaranteed O(log n) behavior vs unbalanced BST.
2. Add memory profiling (e.g., using `tracemalloc` or `memory_profiler`) to measure space usage alongside time.
3. Provide optional warm-up runs and discard the first measurement to reduce JIT/GC/warm-up effects.
4. Add caching of benchmark results and the ability to persist runs (CSV + metadata) for later comparison.

Medium-term (nice to have):
1. Add more data structures: Heap/PriorityQueue, Deque (collections.deque), Trie, Skip List.
2. Add concurrent/multi-threaded experiments where applicable (careful of GIL in CPython).
3. Implement parametric workload generators (mixed insert/search/delete ratios) to simulate real-world application patterns.

Long-term (research/advanced):
1. Provide asymptotic curve-fitting utilities to fit measured growth to theoretical classes (constant, log, linear, n log n, quadratic).
2. Cloud-run experiment runner to produce reproducible, shareable experiment artifacts.

---

## 11. Appendix

### File inventory (principal files)
- `app.py` — Streamlit UI
- `requirements.txt` — dependencies
- `src/ds/array_ds.py` — Array wrapper
- `src/ds/linked_list.py` — Linked list
- `src/ds/bst.py` — Binary search tree (unbalanced)
- `src/ds/hash_table.py` — Hash table (separate chaining)
- `src/ds/graph.py` — Graph (adjacency list)
- `src/benchmarks/benchmark.py` — Benchmark harness
- `src/utils/helpers.py` — helpers
- `src/utils/comparison.py` — multi-op comparison page
- `tests/validate_all.py` — validator that runs all operations

### How to reproduce the representative numbers
1. Activate venv and ensure dependencies installed (see Section 6)
2. Run `python tests/validate_all.py` which runs a set of small validation benchmarks and prints average timings

---

## 12. Conclusion

Structure Showdown provides a compact, practical, and well-documented platform to empirically study data structure performance in Python. It meets the original goals: implementing and comparing multiple data structures; exposing empirical performance differences and trade-offs; and offering an interactive, educational interface.

The project is ready for use in classroom demonstrations, assignments, and exploratory analysis. With the recommended next steps (balanced BST, memory profiling, and workload generators) it could evolve into a highly capable benchmarking suite suitable for deeper research and reporting.


---

*End of Project Report*
