"""Minimum Number of Coins to Be Added with 2 * 10^4 coins and target = 10^5, few of them small:
tracking every obtainable sum coin by coin is ~10^9 steps."""

SEEDS = 2
N = 2 * 10**4
TARGET = 10**5


def generate(rng):
    low = rng.randint(TARGET // 2000 + 1, TARGET // 200 + 1)
    coins = [rng.randint(low, TARGET) for _ in range(N - 3)]
    coins += [rng.randint(1, low) for _ in range(3)]
    rng.shuffle(coins)
    return {"coins": coins, "target": TARGET}
