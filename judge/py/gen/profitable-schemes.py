"""Profitable Schemes at the limits n = 100, minProfit near 100, 100 crimes of 1 to 3 people:
the full O(crimes * n * minProfit) DP, with counts far past 10^9 + 7, and a DP that keeps the
uncapped profit holds ~2 * 10^5 states per crime."""

SEEDS = 2
CRIMES = 100


def generate(rng):
    group = [rng.randint(1, 3) for _ in range(CRIMES)]
    profit = [rng.randint(0, 100) for _ in range(CRIMES)]
    return {"n": 100, "minProfit": rng.randint(90, 100), "group": group, "profit": profit}
