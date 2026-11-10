"""Fruit Into Baskets at n = 10^5: long two-type stretches broken by a third type, or random over
a few types."""

SEEDS = 3
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        types = rng.sample(range(N), 3)
        fruits = []
        while len(fruits) < N:
            a, b = rng.sample(types, 2)
            fruits.extend(rng.choice([a, b]) for _ in range(rng.randint(1, 20000)))
        fruits = fruits[:N]
    else:
        types = rng.sample(range(N), rng.randint(2, 6))
        fruits = [rng.choice(types) for _ in range(N)]
    return {"fruits": fruits}
