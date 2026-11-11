"""Maximum Area Rectangle With Point Constraints II at about 4 * 10^4 points: either a grid of 141
random lines each way with a few removed, or two far columns sharing 10^4 rows below 4 * 10^7
with 2 * 10^4 points between them above it, so checking each candidate against the points
between its columns is ~2 * 10^8 steps."""

from _shapes import pick_shape

SEEDS = 2
SIDE = 141
ROWS = 10**4
FILL = 2 * 10**4
LIMIT = 8 * 10**7


def generate(rng):
    if pick_shape(rng) == 0:
        xs = sorted(rng.sample(range(LIMIT + 1), SIDE))
        ys = sorted(rng.sample(range(LIMIT + 1), SIDE))
        points = [(x, y) for x in xs for y in ys if rng.random() < 0.995]
    else:
        # Every row pair spans both columns and is empty; the filler sits above all of them.
        mid = LIMIT // 2
        seen = set()
        for y in rng.sample(range(mid), ROWS):
            seen.add((0, y))
            seen.add((LIMIT, y))
        while len(seen) < 2 * ROWS + FILL:
            seen.add((rng.randint(1, LIMIT - 1), rng.randint(mid + 1, LIMIT)))
        points = sorted(seen)
    rng.shuffle(points)
    return {"xCoord": [p[0] for p in points], "yCoord": [p[1] for p in points]}
