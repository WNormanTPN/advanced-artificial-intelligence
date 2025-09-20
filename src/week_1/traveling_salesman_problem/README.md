# Bài toán Traveling Salesman Problem (TSP)

## Mô tả
- Có `n` thành phố.
- `dist_matrix[i][j]`: khoảng cách từ thành phố `i` đến thành phố `j`.
- Xuất phát từ thành phố 0, đi qua mỗi thành phố đúng **1 lần**, rồi quay lại điểm xuất phát.
- Mục tiêu: tìm hành trình có tổng khoảng cách **nhỏ nhất**.

## Ví dụ
Với ma trận khoảng cách:
```
[[0, 10, 15, 20],
[10, 0, 35, 25],
[15, 35, 0, 30],
[20, 25, 30, 0]]
```
→ Kết quả tối ưu: 80.

## Brute Force (Backtracking)
**Ý tưởng**
- Xây dựng hành trình bằng đệ quy: tại mỗi bước, chọn 1 thành phố chưa đi và tiếp tục.
- Khi đã đi hết `n` thành phố, cộng thêm quãng đường quay về thành phố xuất phát.
- Cập nhật lời giải tốt nhất (min distance).
- Có thể cắt nhánh khi tổng quãng đường tạm thời đã lớn hơn nghiệm hiện tại.

```python
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

dist_matrix = [[0, 10, 15, 20],
               [10, 0, 35, 25],
               [15, 35, 0, 30],
               [20, 25, 30, 0]]

print("TSP Backtracking Recursive:", tsp_backtracking(dist_matrix))
```

## Branch and Bound
**Ý tưởng**
- Dùng cây tìm kiếm tương tự backtracking.
- Với mỗi trạng thái, tính cận dưới (lower bound) bằng cách cộng chi phí hiện tại với ước lượng tối thiểu để đi qua các thành phố còn lại.
- Nếu bound ≥ nghiệm tốt nhất hiện có → cắt nhánh (không cần xét tiếp).
- Nhờ vậy, số lượng trạng thái cần duyệt giảm nhiều so với brute force.

```python
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

dist_matrix = [[0, 10, 15, 20],
               [10, 0, 35, 25],
               [15, 35, 0, 30],
               [20, 25, 30, 0]]

print("TSP Branch and Bound:", tsp_branch_n_bound(dist_matrix))
```
