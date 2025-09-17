def job_scheduling_backtracking(jobs, t=0, current_profit=0, schedule=None, best=None):
    """jobs: danh sach (deadline, profit)
    t: thoi gian hien tai
    current_profit: tong loi nhuan hien tai
    schedule: danh sach cong viec da chon
    best: [profit tot nhat,danh sach cong viec chon tot nhat]
    """
    if schedule is None:
        schedule = []
    if best is None:
        best = [0, []]

    n = len(jobs)

    # Neu da xet het cong viec
    if t == n:
        if current_profit > best[0]:
            best[0] = current_profit
            best[1] = schedule.copy()
        return best

    # TH 1:bo qua cong viec t
    job_scheduling_backtracking(jobs, t + 1, current_profit, schedule, best)

    # TH 2: La cong viec t (neu truoc deadline)
    deadline, profit = jobs[t]
    if len(schedule) < deadline:  # con slot truoc deadline
        schedule.append(t)  # chon cong viec t
        job_scheduling_backtracking(jobs, t + 1, current_profit + profit, schedule, best)
        schedule.pop()  # quay lui

    return best


def solve_job_scheduling(jobs):
    """jobs: danh sách công việc (deadline, profit)"""
    return job_scheduling_backtracking(jobs)


# Danh sach cong viec: (deadline, profit)
jobs = [
    (2, 100),  # Job 0: deadline 2, profit 100
    (1, 19),  # Job 1: deadline 1, profit 19
    (2, 27),  # Job 2: deadline 2, profit 27
    (1, 25),  # Job 3: deadline 1, profit 25
    (3, 15),  # Job 4: deadline 3, profit 15
]

best_profit, best_jobs = solve_job_scheduling(jobs)

print(best_profit)
print(best_jobs)
