"""Maximum Non Negative Product in a Matrix on a full 15 x 15 grid of mostly non-zero values, so
walking every one of the C(28, 14) ~ 4 * 10^7 paths cannot finish."""

SEEDS = 2
M = N = 15


def generate(rng):
    cells = [v for v in range(-4, 5) if v]
    grid = [[0 if rng.random() < 0.02 else rng.choice(cells) for _ in range(N)] for _ in range(M)]
    return {"grid": grid}
