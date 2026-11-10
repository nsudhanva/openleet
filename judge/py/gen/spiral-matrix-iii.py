"""Spiral Matrix III on a 100 x 100 grid starting at a corner or edge, so the spiral walks
about four times the area outside the grid."""

SEEDS = 3


def generate(rng):
    rows, cols = rng.choice(
        [(100, 100), (1, 100), (100, 1), (rng.randint(50, 100), rng.randint(50, 100))]
    )
    r = rng.choice([0, rows - 1, rng.randrange(rows)])
    c = rng.choice([0, cols - 1, rng.randrange(cols)])
    return {"rows": rows, "cols": cols, "rStart": r, "cStart": c}
