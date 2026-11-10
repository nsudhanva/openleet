"""Minimum Size Subarray Sum at n = 10^5: a target needing a long window, or one larger than
the whole sum (answer 0), so the quadratic scan does ~5 * 10^9 steps."""

SEEDS = 3
N = 10**5


def generate(rng):
    nums = [rng.randint(1, 10**4) for _ in range(N)]
    total = sum(nums)
    target = rng.choice((total + 1, total // 2, rng.randint(1, total)))
    return {"target": min(target, 10**9), "nums": nums}
