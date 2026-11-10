"""Minimum Falling Path Sum on the largest 100 x 100 matrix; exploring all paths is 3^100."""

SEEDS = 2


def generate(rng):
    return {"matrix": [[rng.randint(-100, 100) for _ in range(100)] for _ in range(100)]}
