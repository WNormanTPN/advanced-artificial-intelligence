def knapsack_branch_and_bound(values, weights, W):
    n = len(values)

    items = sorted([(values[i], weights[i], i) for i in range(n)], key=lambda x: x[0] / x[1], reverse=True)

    best_value = 0
    best_items = []

    def bound(i, current_weight, current_value):
        if current_weight > W:
            return 0
        total_value = current_value
        total_weight = current_weight

        while i < n and total_weight + items[i][1] <= W:
            total_weight += items[i][1]
            total_value += items[i][0]
            i += 1

        if i < n:
            total_value += (W - total_weight) * (items[i][0] / items[i][1])
        return total_value

    def backtrack(i, current_weight, current_value, chosen):
        nonlocal best_value, best_items

        if current_weight > W:
            return

        if i == n:
            if current_value > best_value:
                best_value = current_value
                best_items = chosen.copy()
            return

        upper = bound(i, current_weight, current_value)
        if upper <= best_value:
            return

        chosen.append(items[i][2])
        backtrack(i + 1, current_weight + items[i][1], current_value + items[i][0], chosen)
        chosen.pop()

        backtrack(i + 1, current_weight, current_value, chosen)

    backtrack(0, 0, 0, [])

    return best_value, best_items


values = [60, 100, 120]
weights = [10, 20, 30]
W = 50

best_value, best_items = knapsack_branch_and_bound(values, weights, W)
print(best_value)
print(best_items)
