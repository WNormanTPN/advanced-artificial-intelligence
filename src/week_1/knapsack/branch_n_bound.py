from dataclasses import dataclass, field
from typing import List


@dataclass
class Item:
    weight: int
    value: int
    ratio: float = field(init=False)

    def __post_init__(self):
        self.ratio = self.weight / self.value


def knapsack_branch_n_bound(items: List[Item], W: int) -> int:
    n = len(items)
    max_value = 0
    items.sort(key=lambda x: x.ratio)

    def bound(i: int, current_weight: int, current_value: int) -> int:
        total_weight, total_value = current_weight, current_value
        for j in range(i, n):
            if total_weight + items[j].weight > W:
                break
            total_weight += items[j].weight
            total_value += items[j].value
        return total_value

    def branch(i: int, current_weight: int, current_value: int) -> None:
        nonlocal max_value
        if current_weight > W:
            return
        if i == n:
            max_value = max(max_value, current_value)
        if bound(i, current_weight, current_value) <= max_value:
            return

        # Not choose i
        branch(i + 1, current_weight, current_value)
        # Choose i
        branch(i + 1, current_weight + items[i].weight, current_value + items[i].value)

    branch(0, 0, 0)
    return max_value


items = [Item(1, 2), Item(2, 3), Item(3, 4)]
W = 5
print(knapsack_branch_n_bound(items, W))
