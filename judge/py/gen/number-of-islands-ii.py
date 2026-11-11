"""Number of Islands II at the maximum 10^4 cells and 10^4 additions: every cell of a 100 x 100
grid once in random order, or a single row (with 10^3 repeated additions) or column of cells
added in order so each addition joins one island of every earlier cell. Recounting the islands
with a flood fill after each addition, or relabelling the joined island's cells one by one, costs
~5 * 10^7 steps."""

from _shapes import pick_shape

SEEDS = 3
CELLS = 10**4
SIDE = 100
REPEATS = 10**3


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        m = n = SIDE
        positions = [[i, j] for i in range(m) for j in range(n)]
        rng.shuffle(positions)
    elif shape == 1:
        m, n = 1, CELLS - REPEATS
        positions = [[0, j] for j in range(n)]
        for _ in range(REPEATS):
            positions.insert(rng.randrange(1, len(positions)), [0, rng.randrange(n)])
        positions = positions[:CELLS]
    else:
        m, n = CELLS, 1
        positions = [[i, 0] for i in range(m)]
    return {"m": m, "n": n, "positions": positions}
