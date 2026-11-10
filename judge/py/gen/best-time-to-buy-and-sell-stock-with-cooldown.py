"""Best Time to Buy and Sell Stock with Cooldown at n = 5000: random, or a short-period zigzag
where the cooldown changes which trades to take."""

SEEDS = 2
N = 5000


def generate(rng):
    if rng.random() < 0.5:
        prices = [rng.randint(0, 1000) for _ in range(N)]
    else:
        period = rng.choice([2, 3])
        prices = [
            rng.randint(900, 1000) if i % period == period - 1 else rng.randint(0, 100)
            for i in range(N)
        ]
    return {"prices": prices}
