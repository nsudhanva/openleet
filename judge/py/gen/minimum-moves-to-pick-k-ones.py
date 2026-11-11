"""Minimum Moves to Pick K Ones at n = 10^5 with about half the cells ones, few changes and k
near the number of ones: gathering the nearest k ones afresh from every start is ~10^9 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    p = rng.uniform(0.3, 0.7)
    nums = [int(rng.random() < p) for _ in range(N)]
    max_changes = rng.randint(0, 5)
    k = max(1, sum(nums) + max_changes - rng.randint(0, 100))
    return {"nums": nums, "k": k, "maxChanges": max_changes}
