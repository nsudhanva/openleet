"""Number of Smooth Descent Periods of a Stock at 3 * 10^4 prices made of descents by one that run
5,000 to 15,000 days, so extending a period from every day costs ~1.5 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4
LONG = 15000


def generate(rng):
    prices = []
    while len(prices) < N:
        length = min(rng.randint(LONG // 3, LONG), N - len(prices))
        top = rng.randint(length, 10**5)
        if prices and prices[-1] == top + 1:
            top -= 1
        prices += range(top, top - length, -1)
    return {"prices": prices}
