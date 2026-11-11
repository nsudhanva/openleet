"""Number of Black Blocks at 10^4 black cells on a ~10^5 x 10^5 grid: one ~45 % dense 150 x 150
patch, or two ~50 % dense 100 x 100 patches in opposite corners. Counting each touched block's
black cells by scanning the coordinate list is ~10^9 steps, and visiting every block inside the
bounding box is 10^10 on the two-corner shape."""

from _shapes import pick_shape

SEEDS = 2
N = 10**4
SIDE = 150
PATCH = 100
GRID = 10**5


def generate(rng):
    m = GRID - rng.randrange(min(10, GRID - SIDE))
    n = GRID - rng.randrange(min(10, GRID - SIDE))
    if pick_shape(rng) == 0:
        top, left = rng.randrange(m - SIDE + 1), rng.randrange(n - SIDE + 1)
        cells = rng.sample(range(SIDE * SIDE), N)
        return {"m": m, "n": n, "coordinates": [[top + c // SIDE, left + c % SIDE] for c in cells]}
    half = N // 2
    coordinates = []
    for top, left in ((rng.randrange(10), rng.randrange(10)), (m - PATCH, n - PATCH)):
        cells = rng.sample(range(PATCH * PATCH), half)
        coordinates += [[top + c // PATCH, left + c % PATCH] for c in cells]
    rng.shuffle(coordinates)
    return {"m": m, "n": n, "coordinates": coordinates}
