from typing import List


def tsp_branch_n_bound(dist_matrix: List[List[int]]) -> int:
    min_dist = 10**18
    n = len(dist_matrix)

    def bound(visited: List[int], current_dist: int) -> int:
        b = current_dist
        for i in range(n):
            if i not in visited:
                min_edge = 10**18
                for j in range(n):
                    if j != i and j not in visited:
                        min_edge = min(min_edge, dist_matrix[i][j])
                if min_edge != 10**18:
                    b += min_edge
        return b

    def branch(current_city: int, visited: List[int], current_dist: int) -> None:
        nonlocal min_dist
        if len(visited) == n:
            min_dist = min(current_dist + dist_matrix[current_city][0], min_dist)
            return
        if current_dist > min_dist:
            return
        if bound(visited, current_dist) >= min_dist:
            return

        for i in range(n):
            if i not in visited:
                branch(i, visited + [i], current_dist + dist_matrix[current_city][i])

    branch(0, [0], 0)
    return min_dist


dist_matrix = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]

print("TSP Backtracking Recursive:", tsp_branch_n_bound(dist_matrix))
