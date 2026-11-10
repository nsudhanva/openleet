"""Max Increase to Keep City Skyline on a 50 x 50 grid of heights in [0, 100]."""

SEEDS = 2
N = 50


def generate(rng):
    return {"grid": [[rng.randint(0, 100) for _ in range(N)] for _ in range(N)]}
