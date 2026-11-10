"""Distribute Candies at n = 10^4: all distinct types, or only a handful of types."""

SEEDS = 2
N = 10**4


def generate(rng):
    if rng.random() < 0.5:
        candy = rng.sample(range(-(10**5), 10**5 + 1), N)
    else:
        pool = rng.sample(range(-(10**5), 10**5 + 1), rng.randint(1, 50))
        candy = [rng.choice(pool) for _ in range(N)]
    return {"candyType": candy}
