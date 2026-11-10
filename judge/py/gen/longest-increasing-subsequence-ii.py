"""Longest Increasing Subsequence II at n = 10^5, values up to 10^5: an increasing run
(answer ~n, quadratic DP times out) or random values with varied k."""

SEEDS = 3
N = 10**5


def generate(rng):
    if rng.random() < 0.4:
        nums = sorted(rng.randint(1, 10**5) for _ in range(N))
        k = rng.randint(1, 10)
    else:
        nums = [rng.randint(1, 10**5) for _ in range(N)]
        k = rng.choice([1, rng.randint(1, 100), rng.randint(1, 10**5)])
    return {"nums": nums, "k": k}
