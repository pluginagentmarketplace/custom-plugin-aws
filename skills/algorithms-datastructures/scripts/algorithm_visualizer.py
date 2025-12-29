#!/usr/bin/env python3
"""
Algorithm Visualizer
Demonstrates common algorithms with step-by-step output.
"""

from typing import List, Tuple, Optional
from collections import deque


class AlgorithmVisualizer:
    """Visualize algorithm execution."""

    @staticmethod
    def binary_search(arr: List[int], target: int, verbose: bool = True) -> int:
        """Binary search with visualization."""
        left, right = 0, len(arr) - 1
        step = 0

        while left <= right:
            mid = (left + right) // 2
            step += 1

            if verbose:
                print(f"Step {step}: left={left}, right={right}, mid={mid}")
                print(f"  Checking arr[{mid}] = {arr[mid]}")

            if arr[mid] == target:
                if verbose:
                    print(f"  Found! Target {target} at index {mid}")
                return mid
            elif arr[mid] < target:
                if verbose:
                    print(f"  {arr[mid]} < {target}, searching right half")
                left = mid + 1
            else:
                if verbose:
                    print(f"  {arr[mid]} > {target}, searching left half")
                right = mid - 1

        return -1

    @staticmethod
    def quicksort(arr: List[int], verbose: bool = True) -> List[int]:
        """Quicksort with visualization."""
        if len(arr) <= 1:
            return arr

        def partition(low: int, high: int) -> int:
            pivot = arr[high]
            i = low - 1

            if verbose:
                print(f"Partitioning [{low}:{high}], pivot={pivot}")

            for j in range(low, high):
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]

            arr[i + 1], arr[high] = arr[high], arr[i + 1]

            if verbose:
                print(f"  After partition: {arr}, pivot index={i + 1}")

            return i + 1

        def sort(low: int, high: int):
            if low < high:
                pi = partition(low, high)
                sort(low, pi - 1)
                sort(pi + 1, high)

        result = arr.copy()
        sort(0, len(result) - 1)
        return result

    @staticmethod
    def bfs(graph: dict, start: str, verbose: bool = True) -> List[str]:
        """BFS traversal with visualization."""
        visited = set()
        queue = deque([start])
        result = []

        while queue:
            vertex = queue.popleft()

            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)

                if verbose:
                    print(f"Visiting: {vertex}")
                    print(f"  Queue: {list(queue)}")
                    print(f"  Visited: {visited}")

                for neighbor in graph.get(vertex, []):
                    if neighbor not in visited:
                        queue.append(neighbor)

        return result

    @staticmethod
    def dfs(graph: dict, start: str, verbose: bool = True) -> List[str]:
        """DFS traversal with visualization."""
        visited = set()
        result = []

        def explore(vertex: str, depth: int = 0):
            if vertex in visited:
                return

            visited.add(vertex)
            result.append(vertex)

            if verbose:
                indent = "  " * depth
                print(f"{indent}Visiting: {vertex}")

            for neighbor in graph.get(vertex, []):
                if neighbor not in visited:
                    explore(neighbor, depth + 1)

        explore(start)
        return result

    @staticmethod
    def dijkstra(graph: dict, start: str, verbose: bool = True) -> dict:
        """Dijkstra's shortest path."""
        import heapq

        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        pq = [(0, start)]
        visited = set()

        while pq:
            current_dist, current = heapq.heappop(pq)

            if current in visited:
                continue

            visited.add(current)

            if verbose:
                print(f"Processing: {current} (distance={current_dist})")

            for neighbor, weight in graph[current].items():
                distance = current_dist + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

                    if verbose:
                        print(f"  Updated distance to {neighbor}: {distance}")

        return distances


def main():
    """Demo algorithms."""
    viz = AlgorithmVisualizer()

    print("=== Binary Search ===")
    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    result = viz.binary_search(arr, 7)
    print(f"Result: {result}\n")

    print("=== Quicksort ===")
    arr = [64, 34, 25, 12, 22, 11, 90]
    sorted_arr = viz.quicksort(arr.copy())
    print(f"Sorted: {sorted_arr}\n")

    print("=== BFS ===")
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    bfs_result = viz.bfs(graph, 'A')
    print(f"BFS order: {bfs_result}\n")

    print("=== Dijkstra ===")
    weighted_graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'C': 2, 'D': 5},
        'C': {'A': 4, 'B': 2, 'D': 1},
        'D': {'B': 5, 'C': 1}
    }
    distances = viz.dijkstra(weighted_graph, 'A')
    print(f"Shortest distances from A: {distances}")


if __name__ == "__main__":
    main()
