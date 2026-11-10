"""Number of Closed Islands on a 100 x 100 grid: random land and water, or a lattice of many
small closed islands with one long snake that touches the border."""

SEEDS = 3
SIZE = 100


def generate(rng):
    if rng.random() < 0.5:
        p = rng.choice((0.5, 0.6))
        grid = [[1 if rng.random() < p else 0 for _ in range(SIZE)] for _ in range(SIZE)]
    else:
        grid = [[0 if r % 2 and c % 2 else 1 for c in range(SIZE)] for r in range(SIZE)]
        for r in range(1, SIZE, 4):
            for c in range(SIZE):
                grid[r][c] = 0
    rows = rng.choice((SIZE, rng.randint(1, SIZE)))
    return {"grid": [row[:] for row in grid[:rows]]}
