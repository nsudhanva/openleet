"""Count Submatrices With Equal Frequency of X and Y on a 1000 x 250 grid (tall or wide), so
adding up the rows above (or columns left of) each cell costs 3 * 10^7-1.25 * 10^8 steps and
recounting each top-left submatrix cell by cell far more."""

from _shapes import pick_shape

SEEDS = 2
M, N = 1000, 250


def generate(rng):
    m, n = (M, N) if pick_shape(rng) == 0 else (N, M)
    dots = rng.uniform(0.2, 0.8)
    grid = [["." if rng.random() < dots else rng.choice("XY") for _ in range(n)] for _ in range(m)]
    return {"grid": grid}
