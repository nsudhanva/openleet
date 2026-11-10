"""Longest Subarray With Absolute Diff <= Limit at n = 10^5: a slow random walk with a large
answer window (quadratic scans time out), or random values with a tight limit."""

SEEDS = 3
N = 10**5
LIMIT = 10**9


def generate(rng):
    if rng.random() < 0.5:
        cur = LIMIT // 2
        nums = []
        for _ in range(N):
            cur = min(LIMIT, max(1, cur + rng.randint(-1000, 1000)))
            nums.append(cur)
        limit = rng.randint(10**5, 10**6)
    else:
        nums = [rng.randint(1, LIMIT) for _ in range(N)]
        limit = rng.choice([0, rng.randint(0, LIMIT)])
    return {"nums": nums, "limit": limit}
