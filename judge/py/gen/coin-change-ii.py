"""Coin Change II with up to 300 distinct coins and amount up to 5000 (the full O(amount *
coins) DP), with the amount chosen as large as possible while the answer still fits in 32
bits."""

SEEDS = 3
CAP = 2**31 - 1


def generate(rng):
    lo = rng.choice([1, 50, 200])
    coins = rng.sample(range(lo, 5001), rng.choice([300, 100, 30]))
    dp = [0] * 5001
    dp[0] = 1
    for c in coins:
        for a in range(c, 5001):
            dp[a] = min(CAP + 1, dp[a] + dp[a - c])
    fits = [a for a in range(5001) if dp[a] <= CAP]
    top = [a for a in fits if a > fits[-1] - 200 and dp[a] > 0] or [fits[-1]]
    return {"amount": rng.choice(top), "coins": coins}
