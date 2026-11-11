"""Combination Sum IV with up to 200 distinct numbers and the target whose count is largest
while still fitting in 32 bits (at least 2^28), so naive recursion without memo makes at least
that many calls."""

SEEDS = 2
CAP = 2**31 - 1


def generate(rng):
    while True:
        lo = rng.choice([1, 10, 50])
        nums = rng.sample(range(lo, 1001), rng.choice([200, 50]))
        dp = [0] * 1001
        dp[0] = 1
        for t in range(1, 1001):
            dp[t] = sum(dp[t - v] for v in nums if v <= t)
        target = max(range(1, 1001), key=lambda t: dp[t] if dp[t] <= CAP else -1)
        if dp[target] >= 2**28:
            return {"nums": nums, "target": target}
