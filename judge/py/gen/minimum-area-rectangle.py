"""Minimum Area Rectangle at the maximum 500 unique points: sparse on a 100 x 100 line grid,
dense on a few shared lines, or scattered around three planted rectangles, so testing every
diagonal pair against the point list is ~6 * 10^7 comparisons."""

from _shapes import pick_shape

SEEDS = 3
N = 500
GRID = 100
TOP = 4 * 10**4
PLANTED = 3


def generate(rng):
    shape = pick_shape(rng)
    if shape == 2:
        points, seen = [], set()
        for _ in range(PLANTED):
            x1, x2 = rng.sample(range(TOP + 1), 2)
            y1, y2 = rng.sample(range(TOP + 1), 2)
            for p in ((x1, y1), (x1, y2), (x2, y1), (x2, y2)):
                if p not in seen:
                    seen.add(p)
                    points.append(p)
        while len(points) < N:
            p = (rng.randint(0, TOP), rng.randint(0, TOP))
            if p not in seen:
                seen.add(p)
                points.append(p)
        rng.shuffle(points)
        return {"points": [list(p) for p in points]}
    lines = GRID if shape == 0 else rng.randint(23, 40)
    xs = rng.sample(range(TOP + 1), lines)
    ys = rng.sample(range(TOP + 1), lines)
    cells = rng.sample(range(lines * lines), N)
    return {"points": [[xs[c // lines], ys[c % lines]] for c in cells]}
