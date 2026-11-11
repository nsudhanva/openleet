"""Minimize the Difference Between Target and Chosen Elements on a 12 x 70 matrix of even values
and an odd target, so no choice hits it and trying every choice per row is 70^12."""

SEEDS = 2
ROWS = 12
COLS = 70
LIMIT = 70


def generate(rng):
    # Every sum is even and the target odd, so no search can stop early at difference 0.
    mat = [[2 * rng.randint(1, LIMIT // 2) for _ in range(COLS)] for _ in range(ROWS)]
    return {"mat": mat, "target": 2 * rng.randint(ROWS * LIMIT // 6, ROWS * LIMIT // 3) + 1}
