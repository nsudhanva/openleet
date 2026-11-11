"""Shortest Bridge on a 100 x 100 grid with two islands of ~4500 cells each, a few cells apart
across a diagonal, vertical or horizontal gap, so trying every pair of cells costs ~2 * 10^7."""

from _shapes import pick_shape

SEEDS = 3
N = 100


def walk(rng, lo, hi):
    """N heights in [lo, hi], each within one of the last."""
    h = [rng.randint(lo, hi)]
    for _ in range(N - 1):
        h.append(min(hi, max(lo, h[-1] + rng.randint(-1, 1))))
    return h


def generate(rng):
    shape = pick_shape(rng)
    gap = rng.randint(2, 8)
    grid = [[0] * N for _ in range(N)]
    if shape == 0:
        # Two triangles either side of an empty diagonal band.
        for r in range(N):
            for c in range(N):
                if r + c < N - 1 - gap // 2 or r + c > N - 1 + (gap - gap // 2):
                    grid[r][c] = 1
    else:
        # Two slabs, each column (or row) a run from its edge, with jagged facing borders.
        top = walk(rng, N * 35 // 100, N // 2 - gap)
        bottom = [t + gap + rng.randint(0, 3) for t in top]
        for c in range(N):
            for r in range(N):
                if r < top[c] or r > bottom[c]:
                    if shape == 1:
                        grid[r][c] = 1
                    else:
                        grid[c][r] = 1
    return {"grid": grid}
