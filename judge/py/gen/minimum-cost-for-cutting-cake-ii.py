"""Minimum Cost for Cutting Cake II on a 2 * 10^4 x 2 * 10^4 cake, so taking each next cut by
scanning for the most expensive remaining line is quadratic."""

SEEDS = 2
SIDE = 2 * 10**4
LIMIT = 10**3


def generate(rng):
    horizontal = [rng.randint(1, LIMIT) for _ in range(SIDE - 1)]
    vertical = [rng.randint(1, LIMIT) for _ in range(SIDE - 1)]
    return {"m": SIDE, "n": SIDE, "horizontalCut": horizontal, "verticalCut": vertical}
