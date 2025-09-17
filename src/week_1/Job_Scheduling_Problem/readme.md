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
Phương pháp
Brute Force Backtracking
Độ phức tạp: O(2^n)
Đặc điểm: Duyệt hết, dễ cài đặt nhưng chậm khi n lớn
Phương pháp
Branch & Bound
Độ phức tạp:	O(2^n) worst-case, nhanh hơn trong thực tế
Đặc điểm:	Cắt bớt nhánh không cần thiết, hiệu quả hơn nhiều
