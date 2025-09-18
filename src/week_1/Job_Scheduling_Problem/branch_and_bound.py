
import heapq

class Node:
    def __init__(self, level, profit, bound, schedule):
        self.level = level      # cấp của node trong cây (công việc thứ mấy)
        self.profit = profit    # lợi nhuận hiện tại
        self.bound = bound      # cận trên của node này
        self.schedule = schedule  # danh sách công việc đã chọn

    # định nghĩa so sánh để dùng trong max-heap
    def __lt__(self, other):
        return self.bound > other.bound


def bound(node, jobs, max_deadline):
    """Tính cận trên (bound) của một node"""
    if node.level >= len(jobs):
        return 0

    profit_bound = node.profit
    j = node.level + 1
    total_time = len(node.schedule)

    # duyệt tiếp các job còn lại
    while j < len(jobs) and total_time < max_deadline:
        profit_bound += jobs[j][1]  # cộng thêm profit
        total_time += 1
        j += 1
    return profit_bound


def job_scheduling_branch_and_bound(jobs):
    """
    jobs: danh sách tuple (deadline, profit)
    Trả về: (max_profit, best_schedule)
    """
    # sắp xếp công việc theo profit giảm dần
    jobs = sorted(jobs, key=lambda x: x[1], reverse=True)
    max_deadline = max(job[0] for job in jobs)

    # khởi tạo hàng đợi ưu tiên
    pq = []
    root = Node(level=-1, profit=0, bound=0, schedule=[])
    root.bound = bound(root, jobs, max_deadline)
    heapq.heappush(pq, root)

    max_profit = 0
    best_schedule = []

    while pq:
        node = heapq.heappop(pq)

        if node.bound > max_profit and node.level < len(jobs) - 1:
            next_level = node.level + 1
            job = jobs[next_level]

            # Nhánh 1: chọn job này (nếu còn slot)
            if len(node.schedule) < job[0]:
                new_schedule = node.schedule + [job]
                profit_with_job = node.profit + job[1]
                child = Node(
                    level=next_level,
                    profit=profit_with_job,
                    bound=bound(Node(next_level, profit_with_job, 0, new_schedule), jobs, max_deadline),
                    schedule=new_schedule
                )
                if profit_with_job > max_profit:
                    max_profit = profit_with_job
                    best_schedule = new_schedule
                if child.bound > max_profit:
                    heapq.heappush(pq, child)

            # Nhánh 2: bỏ qua job này
            child = Node(
                level=next_level,
                profit=node.profit,
                bound=bound(Node(next_level, node.profit, 0, node.schedule), jobs, max_deadline),
                schedule=node.schedule
            )
            if child.bound > max_profit:
                heapq.heappush(pq, child)

    return max_profit, best_schedule


if __name__ == "__main__":
    # ví dụ
    jobs = [(2, 100), (1, 19), (2, 27), (1, 25), (3, 15)]
    max_profit, schedule = job_scheduling_branch_and_bound(jobs)

    print( max_profit)
    print( schedule)
