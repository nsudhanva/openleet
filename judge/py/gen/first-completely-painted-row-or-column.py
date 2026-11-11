"""A grid of 8 * 10^4 cells, 2 or 3 rows by tens of thousands of columns, painted row by row from
the left around one hole per column, so no line completes until the last n paints and rescanning
each painted cell's row costs ~8 * 10^8 steps."""

SEEDS = 2
CELLS = 8 * 10**4


def generate(rng):
    m = rng.randint(2, 3)
    n = CELLS // m
    # Row a holds the holes of columns 0..n-m; each other row holds one of the last m-1. Every
    # row and column keeps a hole, so the first line completes when the first hole is painted.
    a = rng.randrange(m)
    others = [r for r in range(m) if r != a]
    rng.shuffle(others)
    hole = [a] * (n - m + 1) + others
    vals = list(range(1, m * n + 1))
    rng.shuffle(vals)
    mat = [vals[r * n : (r + 1) * n] for r in range(m)]
    arr = [mat[r][c] for r in range(m) for c in range(n) if hole[c] != r]
    holes = [mat[hole[c]][c] for c in range(n)]
    rng.shuffle(holes)
    return {"arr": arr + holes, "mat": mat}
