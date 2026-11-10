"""Profitable Schemes at the limits n = 100, minProfit = 100, 100 crimes: the full
O(crimes * n * minProfit) DP, with counts far past 10^9 + 7."""

SEEDS = 2


def generate(rng):
    small = rng.random() < 0.5
    group = [rng.randint(1, 5 if small else 100) for _ in range(100)]
    profit = [rng.randint(0, 100) for _ in range(100)]
    return {"n": 100, "minProfit": rng.randint(90, 100), "group": group, "profit": profit}
