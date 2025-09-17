import sys
sys.stdout.reconfigure(encoding='utf-8')
def knapsack_branch_and_bound(values, weights, W):
    n = len(values)

    # Sắp xếp các đồ vật theo tỉ lệ value/weight giảm dần (để tính cận tốt hơn)
    items = sorted([(values[i], weights[i], i) for i in range(n)], key=lambda x: x[0]/x[1], reverse=True)

    best_value = 0
    best_items = []

    def bound(i, current_weight, current_value):
        """Tính cận trên (upper bound) cho nhánh hiện tại"""
        if current_weight > W:
            return 0
        total_value = current_value
        total_weight = current_weight
        # Thêm dần các vật còn lại (cho đến khi đầy túi)
        while i < n and total_weight + items[i][1] <= W:
            total_weight += items[i][1]
            total_value += items[i][0]
            i += 1
        # Nếu còn chỗ nhưng không đủ cho vật kế tiếp → lấy theo tỉ lệ (fractional)
        if i < n:
            total_value += (W - total_weight) * (items[i][0] / items[i][1])
        return total_value

    def backtrack(i, current_weight, current_value, chosen):
        nonlocal best_value, best_items

        # Nếu quá tải → bỏ
        if current_weight > W:
            return

        # Nếu đã xét hết vật
        if i == n:
            if current_value > best_value:
                best_value = current_value
                best_items = chosen.copy()
            return

        # Tính cận trên
        upper = bound(i, current_weight, current_value)
        if upper <= best_value:
            return  # cắt nhánh (không thể tốt hơn best hiện tại)

        # Trường hợp 1: chọn vật i
        chosen.append(items[i][2])  # lưu chỉ số gốc của vật
        backtrack(i+1, current_weight + items[i][1], current_value + items[i][0], chosen)
        chosen.pop()

        # Trường hợp 2: bỏ vật i
        backtrack(i+1, current_weight, current_value, chosen)

    backtrack(0, 0, 0, [])

    return best_value, best_items
values = [60, 100, 120]
weights = [10, 20, 30]
W = 50

best_value, best_items = knapsack_branch_and_bound(values, weights, W)
print("Giá trị tối đa:", best_value)
print("Đồ vật được chọn:", best_items)