"""Bricks Falling When Hit on a 200 x 200 grid with 4 * 10^4 unique hits: dense bricks hit in a
random order (every cell hit once), or the top row hit first so huge regions drop; per-hit
flood fill is far too slow."""

SEEDS = 2
SIZE = 200


def generate(rng):
    m = n = SIZE
    density = rng.choice([0.9, 1.0])
    grid = [[1 if rng.random() < density else 0 for _ in range(n)] for _ in range(m)]
    cells = [[r, c] for r in range(m) for c in range(n)]
    rng.shuffle(cells)
    if rng.random() < 0.5:
        cells.sort(key=lambda rc: rc[0] != 0)  # top row first, rest in random order
    return {"grid": grid, "hits": cells[: 4 * 10**4]}
