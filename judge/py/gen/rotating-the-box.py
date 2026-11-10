"""Rotating the Box on a 500 x 500 grid of stones, obstacles and empty cells."""

SEEDS = 2


def generate(rng):
    weights = rng.choice([(0.45, 0.05, 0.5), (0.3, 0.3, 0.4), (0.7, 0.0, 0.3)])
    m, n = 500, 500
    grid = [rng.choices("#*.", weights=weights, k=n) for _ in range(m)]
    return {"boxGrid": grid}
