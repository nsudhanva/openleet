"""As Far from Land as Possible on a 100 x 100 grid: half land at random (~2.5 * 10^7
water-land pairs to compare) or a few land cells in one corner (a search out of every water
cell scans ~10^8 cells)."""

SEEDS = 2
N = 100


def generate(rng):
    if rng.random() < 0.5:
        grid = [[int(rng.random() < 0.5) for _ in range(N)] for _ in range(N)]
    else:
        grid = [[0] * N for _ in range(N)]
        for _ in range(rng.randint(1, 3)):
            grid[rng.randrange(3)][rng.randrange(3)] = 1
    return {"grid": grid}
