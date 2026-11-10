"""Combination Sum IV with 200 distinct numbers and target up to 1000, the target chosen as large
as possible while the count still fits in 32 bits; naive recursion without memo explodes."""

SEEDS = 3
CAP = 2**31 - 1


def generate(rng):
    lo = rng.choice([1, 10, 30, 100])
    nums = rng.sample(range(lo, 1001), rng.choice([200, 50]))
    dp = [0] * 1001
    dp[0] = 1
    for t in range(1, 1001):
        total = 0
        for v in nums:
            if v <= t:
                total += dp[t - v]
        dp[t] = min(CAP + 1, total)
    fits = [t for t in range(1, 1001) if dp[t] <= CAP]
    top = [t for t in fits if dp[t] > 0 and t > fits[-1] - 100] or [fits[-1]]
    return {"nums": nums, "target": rng.choice(top)}
