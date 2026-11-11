"""Minimum Number of Coins to Be Added. Seed 1: 2 * 10^4 coins and target = 10^5, few of them
small, so tracking every obtainable sum coin by coin is ~10^9 steps. Seeds 0, 2, 3 and 4:
~9.5 * 10^4 coins of value 1 and a few of 2 to 50 that fall short of target = 10^5 (the answer is
1), so tracking the sums as a 10^5-bit integer shifts ~10^5 bits ~10^5 times per seed."""

from _shapes import pick_shape

SEEDS = 5
N = 2 * 10**4
TARGET = 10**5


def generate(rng):
    if pick_shape(rng) == 2:
        low = rng.randint(TARGET // 2000 + 1, TARGET // 200 + 1)
        coins = [rng.randint(low, TARGET) for _ in range(N - 3)]
        coins += [rng.randint(1, low) for _ in range(3)]
    else:
        coins = [1] * rng.randint(94000, 96000)
        coins += [rng.randint(2, 50) for _ in range(rng.randint(10, 40))]
    rng.shuffle(coins)
    return {"coins": coins, "target": TARGET}
