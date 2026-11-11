"""Count Submatrices With Top-Left Element and Sum Less Than K on a 1000 x 500 grid (tall or wide)
of single digits with k about a third of the total, so adding up the rows above (or columns left
of) each cell costs 1.25-2.5 * 10^8 steps and summing each submatrix cell by cell far more."""

from _shapes import pick_shape

SEEDS = 2
M, N = 1000, 500
LIMIT = 9


def generate(rng):
    m, n = (M, N) if pick_shape(rng) == 0 else (N, M)
    grid = [[rng.randint(0, LIMIT) for _ in range(n)] for _ in range(m)]
    total = sum(map(sum, grid))
    return {"grid": grid, "k": max(1, min(10**9, total // rng.randint(2, 4)))}
