"""Coin Change II at amount up to 5000 with the coin 1, three of 2 to 6 and up to 20 large ones,
the amount the largest whose nonzero answer fits in 32 bits, so plain recursion explores ~10^8
ways and trying every count of each coin costs over 1.5 * 10^7 steps."""

SEEDS = 3
CAP = 2**31 - 1


def generate(rng):
    coins = [1, *rng.sample(range(2, 7), 3), *rng.sample(range(2500, 5001), rng.randint(0, 20))]
    rng.shuffle(coins)
    dp = [0] * 5001
    dp[0] = 1
    for c in coins:
        for a in range(c, 5001):
            dp[a] = min(CAP + 1, dp[a] + dp[a - c])
    fits = [a for a in range(5001) if 0 < dp[a] <= CAP]
    return {"amount": rng.choice(fits[-50:]), "coins": coins}
