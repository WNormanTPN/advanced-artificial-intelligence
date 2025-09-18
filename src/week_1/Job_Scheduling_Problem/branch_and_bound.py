import heapq
from typing import List, Tuple


class Node:
    def __init__(self, level: int, profit: int, bound: int, schedule: List[Tuple[int, int]]):
        self.level = level        # cấp của node trong cây (đang xét job thứ mấy)
        self.profit = profit      # lợi nhuận hiện tại
        self.bound = bound        # cận trên (bound)
        self.schedule = schedule  # danh sách công việc đã chọn

    # Định nghĩa so sánh để dùng trong max-heap (ưu tiên bound lớn hơn)
    def __lt__(self, other: "Node") -> bool:
        return self.bound > other.bound


def bound(node: Node, jobs: List[Tuple[int, int]], max_deadline: int) -> int:
    """Tính cận trên (bound) của một node."""
    if node.level >= len(jobs):
        return 0

    profit_bound = node.profit
    j = node.level + 1
    total_time = len(node.schedule)

    # duyệt tiếp các job còn lại, miễn là còn slot thời gian
    while j < len(jobs) and total_time < max_deadline:
        profit_bound += jobs[j][1]  # cộng thêm profit
        total_time += 1
        j += 1

    return profit_bound


def job_scheduling_branch_and_bound(jobs: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]]]:
    """Giải bài toán lập lịch bằng Branch and Bound.

    jobs: danh sách tuple (deadline, profit)
    Trả về: (max_profit, best_schedule).
    """
    # Sắp xếp công việc theo profit giảm dần
    jobs = sorted(jobs, key=lambda x: x[1], reverse=True)
    max_deadline = max(job[0] for job in jobs)

    # Hàng đợi ưu tiên (max-heap)
    pq: List[Node] = []

    # Root node
    root = Node(level=-1, profit=0, bound=0, schedule=[])
    root.bound = bound(root, jobs, max_deadline)
    heapq.heappush(pq, root)

    max_profit = 0
    best_schedule: List[Tuple[int, int]] = []

    while pq:
        node = heapq.heappop(pq)

        if node.bound > max_profit and node.level < len(jobs) - 1:
            next_level = node.level + 1
            job = jobs[next_level]

            # Nhánh 1: chọn job này (nếu còn slot trước deadline)
            if len(node.schedule) < job[0]:
                new_schedule = node.schedule + [job]
                profit_with_job = node.profit + job[1]
                child1 = Node(
                    level=next_level,
                    profit=profit_with_job,
                    bound=0,
                    schedule=new_schedule,
                )
                child1.bound = bound(child1, jobs, max_deadline)

                if profit_with_job > max_profit:
                    max_profit = profit_with_job
                    best_schedule = new_schedule

                if child1.bound > max_profit:
                    heapq.heappush(pq, child1)

            # Nhánh 2: bỏ qua job này
            child2 = Node(
                level=next_level,
                profit=node.profit,
                bound=0,
                schedule=node.schedule.copy(),
            )
            child2.bound = bound(child2, jobs, max_deadline)

            if child2.bound > max_profit:
                heapq.heappush(pq, child2)

    return max_profit, best_schedule


if __name__ == "__main__":
    # ví dụ
    jobs = [(2, 100), (1, 19), (2, 27), (1, 25), (3, 15)]
    max_profit, schedule = job_scheduling_branch_and_bound(jobs)

    print("Max Profit:", max_profit)
    print("Best Schedule:", schedule)
