"""Trapping Rain Water II on a 200 x 200 map: a tall rim around a random basin, nested rings
of descending walls, or random heights, punishing repeated flooding passes."""

SEEDS = 3
SIZE = 200
TOP = 2 * 10**4


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    m = SIZE
    n = SIZE if rng.random() < 0.7 else rng.randint(1, SIZE)
    if shape == 0:
        grid = [[rng.randint(0, 100) for _ in range(n)] for _ in range(m)]
        for r in range(m):
            for c in range(n):
                if r in (0, m - 1) or c in (0, n - 1):
                    grid[r][c] = TOP
    elif shape == 1:
        grid = [
            [
                TOP - 200 * min(r, c, m - 1 - r, n - 1 - c)
                if min(r, c, m - 1 - r, n - 1 - c) % 2 == 0
                else 0
                for c in range(n)
            ]
            for r in range(m)
        ]
    else:
        grid = [[rng.randint(0, TOP) for _ in range(n)] for _ in range(m)]
    return {"heightMap": grid}
