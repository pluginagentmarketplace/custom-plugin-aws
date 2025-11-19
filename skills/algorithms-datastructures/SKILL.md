---
name: algorithms-datastructures
description: Master algorithms and data structures including arrays, linked lists, trees, graphs, sorting, searching, and complexity analysis for optimal performance.
---

# Algorithms & Data Structures

## Quick Start

Understand Big O notation and common data structure operations.

```
Time Complexity Legend:
O(1) - Constant time
O(log n) - Logarithmic
O(n) - Linear
O(n log n) - Linearithmic
O(n²) - Quadratic
O(2ⁿ) - Exponential
```

## Fundamental Data Structures

### Linear Structures

**Arrays & Dynamic Arrays**
- Access: O(1)
- Search: O(n)
- Insertion/Deletion: O(n)

**Linked Lists**
- Access: O(n)
- Search: O(n)
- Insertion/Deletion: O(1) if position known

**Stacks & Queues**
- Push/Pop: O(1)
- Peek: O(1)
- Use cases: DFS, BFS, browser history

### Tree Structures

**Binary Search Trees**
- Search: O(log n) average, O(n) worst
- Insertion/Deletion: O(log n) average
- Traversal: Inorder, preorder, postorder

**Balanced Trees (AVL, Red-Black)**
- Guaranteed O(log n) operations
- Self-balancing during modifications

**Heaps**
- Priority queue implementation
- Min-heap, max-heap
- Operations: O(log n)

**Trie (Prefix Tree)**
- String prefix search: O(m) where m is string length
- Autocomplete implementation

### Hash Structures

**Hash Tables**
- Search/Insert/Delete: O(1) average, O(n) worst
- Collision resolution: chaining, open addressing
- Load factor management

**Hash Maps/Dictionaries**
- Key-value pair storage
- Efficient lookups

### Graph Structures

**Adjacency List vs Adjacency Matrix**
- List: O(V + E) space
- Matrix: O(V²) space
- Choose based on edge density

## Core Algorithms

### Sorting Algorithms

| Algorithm | Time (Avg) | Time (Worst) | Space | Stable |
|-----------|-----------|-------------|-------|--------|
| Quick Sort | O(n log n) | O(n²) | O(log n) | No |
| Merge Sort | O(n log n) | O(n log n) | O(n) | Yes |
| Heap Sort | O(n log n) | O(n log n) | O(1) | No |
| Bubble Sort | O(n²) | O(n²) | O(1) | Yes |
| Insertion Sort | O(n²) | O(n²) | O(1) | Yes |

### Searching Algorithms

**Linear Search:** O(n)
**Binary Search:** O(log n) on sorted arrays

### Graph Algorithms

**Traversal:**
- Depth-First Search (DFS): O(V + E)
- Breadth-First Search (BFS): O(V + E)

**Shortest Path:**
- Dijkstra's: O((V + E) log V) with min-heap
- Bellman-Ford: O(VE)

**Minimum Spanning Tree:**
- Kruskal's: O(E log E)
- Prim's: O(V²) or O(E log V)

### Dynamic Programming

- Memoization (top-down)
- Tabulation (bottom-up)
- Common patterns: Fibonacci, Knapsack, Longest Common Subsequence

## Problem Solving Framework

1. **Understand the problem** - Read carefully, clarify ambiguities
2. **Think of examples** - Simple and edge cases
3. **Brute force solution** - Get it working first
4. **Optimize** - Improve time/space complexity
5. **Test** - Edge cases, boundary conditions

## Practice Resources

- LeetCode (https://leetcode.com) - Problem bank with solutions
- HackerRank (https://www.hackerrank.com) - Structured learning
- Project Euler (https://projecteuler.net) - Mathematical problems
- Interview Bit (https://www.interviewbit.com) - Interview focused

## Roadmap

- Data Structures & Algorithms (https://roadmap.sh/datastructures-and-algorithms)
