"""Reverse Subarray To Maximize Array Value at n = 10^4, so trying every subarray to reverse costs
~5 * 10^7 steps."""

SEEDS = 2
N = 10**4
LIMIT = 10**5


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    else:
        nums = sorted(rng.randint(-LIMIT, LIMIT) for _ in range(N))
    return {"nums": nums}
