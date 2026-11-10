"""Best Time to Buy and Sell Stock at n = 10^5: random, or descending with the best buy and
sell at the very end."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        prices = [rng.randint(0, 10**4) for _ in range(N)]
    else:
        prices = [10**4 - i * 10**4 // N for i in range(N - 2)] + [0, 10**4]
    return {"prices": prices}
