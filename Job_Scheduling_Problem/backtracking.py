import sys
sys.stdout.reconfigure(encoding='utf-8')
def job_scheduling_backtracking(jobs, t=0, current_profit=0, schedule=None, best=None):
    """
    jobs: danh sách (deadline, profit)
    t: thời gian hiện tại
    current_profit: tổng lợi nhuận hiện tại
    schedule: danh sách công việc đã chọn
    best: [profit tốt nhất, danh sách công việc tốt nhất]
    """
    if schedule is None:
        schedule = []
    if best is None:
        best = [0, []]

    n = len(jobs)

    # Nếu đã xét hết công việc
    if t == n:
        if current_profit > best[0]:
            best[0] = current_profit
            best[1] = schedule.copy()
        return best

    # Trường hợp 1: Bỏ qua công việc t
    job_scheduling_backtracking(jobs, t+1, current_profit, schedule, best)

    # Trường hợp 2: Làm công việc t (nếu trước deadline)
    deadline, profit = jobs[t]
    if len(schedule) < deadline:  # còn slot trước deadline
        schedule.append(t)  # chọn công việc t
        job_scheduling_backtracking(jobs, t+1, current_profit + profit, schedule, best)
        schedule.pop()  # quay lui

    return best


def solve_job_scheduling(jobs):
    """
    jobs: danh sách công việc (deadline, profit)
    """
    return job_scheduling_backtracking(jobs)
# Danh sách công việc: (deadline, profit)
jobs = [
    (2, 100),   # Job 0: deadline 2, profit 100
    (1, 19),    # Job 1: deadline 1, profit 19
    (2, 27),    # Job 2: deadline 2, profit 27
    (1, 25),    # Job 3: deadline 1, profit 25
    (3, 15)     # Job 4: deadline 3, profit 15
]

best_profit, best_jobs = solve_job_scheduling(jobs)

print("Tổng lợi nhuận tối đa:", best_profit)
print("Công việc được chọn:", best_jobs)