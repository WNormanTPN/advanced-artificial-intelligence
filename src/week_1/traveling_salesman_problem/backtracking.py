from typing import List


def tsp_backtracking(dist_matrix: List[List[int]]) -> int:
    min_dist = 10**18
    n = len(dist_matrix)

    def backtrack(current_city: int, visited: List[int], current_dist: int) -> None:
        nonlocal min_dist
        if len(visited) == n:
            min_dist = min(current_dist + dist_matrix[current_city][0], min_dist)
            return
        if current_dist > min_dist:
            return
        for i in range(n):
            if i not in visited:
                backtrack(i, visited + [i], current_dist + dist_matrix[current_city][i])

    backtrack(0, [0], 0)
    return min_dist


dist_matrix = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]

print("TSP Backtracking Recursive:", tsp_backtracking(dist_matrix))
