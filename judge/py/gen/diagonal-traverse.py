"""Diagonal Traverse with m * n = 10^4: square 100 x 100, or a single long row or column."""

SEEDS = 3


def generate(rng):
    m, n = rng.choice([(100, 100), (1, 10**4), (10**4, 1), (50, 200)])
    return {"mat": [[rng.randint(-(10**5), 10**5) for _ in range(n)] for _ in range(m)]}
