from typing import List


def knapsack_backtracking(w: List[int], v: List[int], W: int) -> int:
    n = len(w)
    max_value = 0

    def backtrack(i: int, current_weight: int, current_value: int) -> None:
        nonlocal max_value
        if current_weight > W:
            return
        if i == n:
            max_value = max(max_value, current_value)
            return
        # Not choose i
        backtrack(i + 1, current_weight, current_value)
        # Choose i
        backtrack(i + 1, current_weight + w[i], current_value + v[i])

    backtrack(0, 0, 0)
    return max_value


# Example
w = [2, 3, 4]
v = [3, 4, 5]
W = 5
print(knapsack_backtracking(w, v, W))
