# Bài toán Knapsack

## Mô tả
- Có `n` vật phẩm, mỗi vật có:
  - `w[i]`: trọng lượng
  - `v[i]`: giá trị
- Balo có sức chứa tối đa `W`.
- Mỗi vật chỉ được chọn **0 hoặc 1 lần**.
- Mục tiêu: chọn tập vật phẩm sao cho tổng trọng lượng ≤ `W` và tổng giá trị là **lớn nhất**.

## Ví dụ
Với `w = [2, 3, 4]`, `v = [3, 4, 5]`, `W = 5`
→ Kết quả tối ưu: chọn vật 0 và 1, tổng giá trị = **7**.

## Brute Force (Backtracking)
- Thử tất cả các cách chọn/bỏ.
- Độ phức tạp: `O(2^n)`.
- Code:

```python
def knapsack_backtracking(w, v, W):
    n = len(w)
    best = 0
    def backtrack(i, cur_w, cur_v):
        nonlocal best
        if cur_w > W: return
        if i == n:
            best = max(best, cur_v)
            return
        backtrack(i+1, cur_w, cur_v)
        backtrack(i+1, cur_w + w[i], cur_v + v[i])
    backtrack(0, 0, 0)
    return best

print(knapsack_backtracking([2,3,4],[3,4,5],5))  # 7
```


## Branch and Bound
- Ý tưởng:
  - Mỗi node biểu diễn trạng thái (các vật đã xét).
  - Dùng **cận trên (upper bound)** từ giải pháp fractional để ước lượng giá trị tối đa có thể đạt được từ node đó.
  - Duyệt theo **best-first search** (node có bound cao nhất trước).
  - Cắt bỏ (prune) các nhánh có bound ≤ giá trị tốt nhất hiện tại.
- Độ phức tạp: worst-case `O(2^n)`, nhưng thực tế nhanh hơn nhiều khi có pruning.

```python
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
```
