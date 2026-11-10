"""Longest Harmonious Subsequence at n = 2 * 10^4: values from a small cluster (big answer),
or wide random values near the limits."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    if rng.random() < 0.5:
        base = rng.randint(-LIMIT, LIMIT - 10)
        nums = [base + rng.randint(0, 10) for _ in range(N)]
    else:
        nums = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    return {"nums": nums}
