"""Cherry Pickup II at the maximum 70 x 70 with values up to 100: random, or a grid where the
two robots compete for the same column."""

SEEDS = 2
N = 70


def generate(rng):
    if rng.random() < 0.5:
        grid = [[rng.randint(0, 100) for _ in range(N)] for _ in range(N)]
    else:
        col = rng.randrange(N)
        grid = [[100 if c == col else rng.randint(0, 5) for c in range(N)] for _ in range(N)]
    return {"grid": grid}
