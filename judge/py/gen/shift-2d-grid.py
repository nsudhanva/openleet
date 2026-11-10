"""Shift 2D Grid on a 50 x 50 grid with k up to 100."""

SEEDS = 2


def generate(rng):
    m, n = 50, rng.choice([50, 1, 37])
    grid = [[rng.randint(-1000, 1000) for _ in range(n)] for _ in range(m)]
    return {"grid": grid, "k": rng.choice([100, rng.randint(0, 100)])}
