"""Largest Submatrix With Rearrangements at 2000 x 50 (the maximum 10^5 cells), almost all 1s,
so measuring each cell's column of 1s by walking up costs ~5 * 10^7 steps."""

SEEDS = 2
M = 2000
N = 50
ZEROS = (0.0002, 0.0008)


def generate(rng):
    zero = rng.choice(ZEROS)
    return {"matrix": [[int(rng.random() >= zero) for _ in range(N)] for _ in range(M)]}
