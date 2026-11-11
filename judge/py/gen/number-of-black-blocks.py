"""Number of Black Blocks at 10^4 black cells packed ~45% dense into a 150 x 150 patch of a
10^5 x 10^5 grid, so counting each touched block's black cells by scanning the coordinate list
is ~10^9 steps."""

SEEDS = 2
N = 10**4
SIDE = 150
GRID = 10**5


def generate(rng):
    m = GRID - rng.randrange(min(10, GRID - SIDE))
    n = GRID - rng.randrange(min(10, GRID - SIDE))
    top, left = rng.randrange(m - SIDE + 1), rng.randrange(n - SIDE + 1)
    cells = rng.sample(range(SIDE * SIDE), N)
    return {"m": m, "n": n, "coordinates": [[top + c // SIDE, left + c % SIDE] for c in cells]}
