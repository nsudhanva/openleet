"""Maximum Profit From Trading Stocks With Discounts with 60 employees in a random hierarchy and
budget 160, so enumerating the affordable sets of purchases cannot finish."""

SEEDS = 2
N = 60
BUDGET = 160


def generate(rng):
    hierarchy = [[rng.randint(1, v - 1), v] for v in range(2, N + 1)]
    present = [rng.randint(1, 30) for _ in range(N)]
    future = [rng.randint(1, 50) for _ in range(N)]
    return {"n": N, "present": present, "future": future, "hierarchy": hierarchy, "budget": BUDGET}
