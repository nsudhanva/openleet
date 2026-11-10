"""Best Time to Buy and Sell Stock II at n = 3 * 10^4: a zigzag with a profit every other day,
or random prices."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        prices = [rng.randint(0, 10**4) for _ in range(N)]
    else:
        prices = [rng.randint(0, 100) if i % 2 == 0 else rng.randint(9900, 10**4) for i in range(N)]
    return {"prices": prices}
