"""Cyclically Rotating a Grid on a 50 x 50 (or wide even) grid with k near 10^9, so rotating
one step at a time is hopeless."""

SEEDS = 2


def generate(rng):
    m, n = rng.choice([(50, 50), (2, 50), (50, 4)])
    grid = [[rng.randint(1, 5000) for _ in range(n)] for _ in range(m)]
    return {"grid": grid, "k": rng.randint(9 * 10**8, 10**9)}
