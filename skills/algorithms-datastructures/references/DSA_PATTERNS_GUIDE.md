# Data Structures & Algorithms Patterns Guide

Essential patterns for coding interviews and problem-solving.

## Problem-Solving Patterns

### Two Pointers

```python
# Find pair with target sum in sorted array
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        current = arr[left] + arr[right]
        if current == target:
            return [left, right]
        elif current < target:
            left += 1
        else:
            right -= 1
    return []
```

**Use when:** Sorted arrays, finding pairs, removing duplicates

### Sliding Window

```python
# Maximum sum subarray of size k
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum

    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i-k]
        max_sum = max(max_sum, window_sum)

    return max_sum
```

**Use when:** Contiguous subarray problems, string problems

### Fast & Slow Pointers

```python
# Detect cycle in linked list
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

**Use when:** Cycle detection, finding middle element

### Merge Intervals

```python
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for current in intervals[1:]:
        if current[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], current[1])
        else:
            merged.append(current)

    return merged
```

### Binary Search Variants

```python
# Find first occurrence
def first_occurrence(arr, target):
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            right = mid - 1  # Continue searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result
```

### DFS/BFS Templates

```python
# DFS template
def dfs(node, visited):
    if not node or node in visited:
        return
    visited.add(node)
    # Process node
    for neighbor in node.neighbors:
        dfs(neighbor, visited)

# BFS template
def bfs(start):
    queue = deque([start])
    visited = {start}

    while queue:
        node = queue.popleft()
        # Process node
        for neighbor in node.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### Dynamic Programming

```python
# Fibonacci with memoization
def fib(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]

# Tabulation approach
def fib_tab(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

## Common Data Structure Operations

### Stack Applications

- Expression evaluation
- Bracket matching
- Monotonic stack problems
- Undo/redo functionality

### Queue Applications

- BFS traversal
- Level-order traversal
- Task scheduling
- Sliding window max

### Heap Applications

- Top K elements
- Merge K sorted lists
- Priority scheduling
- Median finding

## Time Complexity Cheat Sheet

| Operation | Array | Linked List | Hash Table | BST |
|-----------|-------|-------------|------------|-----|
| Access | O(1) | O(n) | N/A | O(log n) |
| Search | O(n) | O(n) | O(1)* | O(log n) |
| Insert | O(n) | O(1) | O(1)* | O(log n) |
| Delete | O(n) | O(1) | O(1)* | O(log n) |

*Average case

## Interview Tips

1. **Clarify** - Ask about input constraints
2. **Examples** - Work through examples
3. **Brute Force** - Start simple
4. **Optimize** - Identify bottlenecks
5. **Code** - Write clean code
6. **Test** - Walk through edge cases
