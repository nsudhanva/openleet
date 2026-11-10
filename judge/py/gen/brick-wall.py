"""Brick Wall at 2 * 10^4 bricks: 10^4 two-brick rows with huge widths, or ~100 rows of ~200
bricks whose edges come from a small shared pool so many line up."""

SEEDS = 2


def generate(rng):
    if rng.random() < 0.5:
        rows, per_row = 10**4, 2
    else:
        rows, per_row = 100, 200
    width = rng.randint(10**6, 2**31 - 1)
    pool = sorted(rng.sample(range(1, width), 3 * per_row))
    wall = []
    for _ in range(rows):
        cuts = sorted(rng.sample(pool, per_row - 1))
        edges = [0, *cuts, width]
        wall.append([edges[i + 1] - edges[i] for i in range(per_row)])
    return {"wall": wall}
