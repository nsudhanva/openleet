"""Count Covered Buildings with ~5 * 10^4 buildings in a 10^4 x 10^4 city, listed in sorted order:
four long rows and four long columns of 6000 buildings each plus a random scatter, so scanning the
row and column of each building, even stopping at the first neighbour on each side, costs ~10^8
steps."""

SEEDS = 2
N = 10**4
LINES = 4
LENGTH = 6000
SCATTER = 2000


def generate(rng):
    cells = set()
    for x in rng.sample(range(1, N + 1), LINES):
        cells.update((x, y) for y in rng.sample(range(1, N + 1), LENGTH))
    for y in rng.sample(range(1, N + 1), LINES):
        cells.update((x, y) for x in rng.sample(range(1, N + 1), LENGTH))
    while len(cells) < LINES * LENGTH * 2 + SCATTER - LINES * LINES:
        cells.add((rng.randint(1, N), rng.randint(1, N)))
    buildings = [list(c) for c in sorted(cells)]
    if rng.random() < 0.5:
        buildings.reverse()
    return {"n": N, "buildings": buildings}
