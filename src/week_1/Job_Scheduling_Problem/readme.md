# Bài toán Lập lịch (Job Scheduling Problem)

## 1. Mô tả bài toán
- Có `n` công việc.  
- Mỗi công việc `i` có:
  - **Deadline** `d[i]`: thời hạn phải hoàn thành.
  - **Profit** `p[i]`: lợi nhuận nếu hoàn thành đúng hạn.
- Mỗi công việc mất đúng **1 đơn vị thời gian**.
- Chỉ làm được **1 công việc tại một thời điểm**.
- Mục tiêu: chọn lịch làm việc để **tối đa hóa lợi nhuận**.

---

## 2. Giải bằng Vét cạn Quay lui (Brute Force Backtracking)

### Ý tưởng
- Với mỗi công việc, ta có 2 lựa chọn:
  1. **Làm** (nếu trước deadline).
  2. **Bỏ qua**.
- Thử tất cả các khả năng để tìm phương án tốt nhất.

### Code

```python
def job_scheduling_backtracking(jobs, t=0, current_profit=0, schedule=None, best=None):
    """
    jobs: danh sách công việc (deadline, profit)
    t: chỉ số công việc đang xét
    current_profit: lợi nhuận hiện tại
    schedule: công việc đã chọn
    best: [profit tốt nhất, danh sách công việc tốt nhất]
    """
    if schedule is None:
        schedule = []
    if best is None:
        best = [0, []]

    n = len(jobs)

    # Nếu xét hết công việc
    if t == n:
        if current_profit > best[0]:
            best[0] = current_profit
            best[1] = schedule.copy()
        return best

    # 1. Bỏ qua công việc t
    job_scheduling_backtracking(jobs, t+1, current_profit, schedule, best)

    # 2. Làm công việc t (nếu trước deadline)
    deadline, profit = jobs[t]
    if len(schedule) < deadline:  # còn slot trước deadline
        schedule.append(t)
        job_scheduling_backtracking(jobs, t+1, current_profit + profit, schedule, best)
        schedule.pop()

    return best


def solve_job_scheduling_backtracking(jobs):
    return job_scheduling_backtracking(jobs)
# Job Scheduling Problem - Branch and Bound

## 📌 Mô tả bài toán
Cho một tập `n` công việc. Mỗi công việc gồm:
- `deadline`: hạn chót để hoàn thành (tính theo slot thời gian).
- `profit`: lợi nhuận nếu hoàn thành công việc trước hạn.

**Mục tiêu**:  
- Chọn ra tập công việc và thứ tự thực hiện sao cho **tổng lợi nhuận lớn nhất**.
- Không có công việc nào trễ hạn.

---

## 📌 Ý tưởng giải thuật Branch and Bound
- Xây dựng cây tìm kiếm, mỗi **node** biểu diễn trạng thái của một tập công việc:
  - **Chọn công việc** (nếu còn thời gian trống).
  - **Bỏ qua công việc**.
- Tính **cận trên (bound)** cho mỗi node để dự đoán lợi nhuận tối đa có thể đạt được từ node đó.
- Sử dụng **Priority Queue (max-heap)** để duyệt các node có bound cao nhất trước.
- Cắt bỏ (prune) các nhánh không thể mang lại kết quả tốt hơn nghiệm hiện tại.

---

## 📌 Code Python

```python
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

    print("Lợi nhuận tối đa:", max_profit)
    print("Lịch công việc tối ưu:", schedule)
Phương pháp	
Brute Force Backtracking	
Độ phức tạp: O(2^n)	
Đặc điểm: Duyệt hết, dễ cài đặt nhưng chậm khi n lớn
Phương pháp
Branch & Bound
Độ phức tạp:	O(2^n) worst-case, nhanh hơn trong thực tế
Đặc điểm:	Cắt bớt nhánh không cần thiết, hiệu quả hơn nhiều