"""Longest Continuous Increasing Subsequence at n = 10^4: strictly increasing throughout, or
random values with wide range."""

SEEDS = 2
N = 10**4
LIMIT = 10**9


def generate(rng):
    if rng.random() < 0.5:
        nums = sorted(rng.sample(range(-LIMIT, LIMIT + 1), N))
    else:
        nums = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    return {"nums": nums}
