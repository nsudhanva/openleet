"""Convex Polygon with 6000 vertices: a convex lattice polygon walked in unit steps along 16
directions (so many vertices are collinear), or the same with one vertex pushed inward and
placed last, so checking every edge against every vertex costs ~3.6 * 10^7 steps."""

import math

SEEDS = 2
N = 6000
LIMIT = 10**4
UPPER = ((1, 0), (2, 1), (1, 1), (1, 2), (0, 1), (-1, 2), (-1, 1), (-2, 1))


def generate(rng):
    dent = rng.random() < 0.5
    cuts = sorted(rng.sample(range(1, N // 2), len(UPPER) - 1))
    counts = [b - a for a, b in zip([0, *cuts], [*cuts, N // 2], strict=True)]
    steps = [(d, k) for d, k in zip(UPPER, counts, strict=True)]
    steps += [((-a, -b), k) for (a, b), k in steps]
    steps.sort(key=lambda s: math.atan2(s[0][1], s[0][0]))
    points, x, y = [], 0, 0
    for (a, b), k in steps:
        for _ in range(k):
            points.append([x, y])
            x, y = x + a, y + b
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    dx = rng.randint(-LIMIT - min(xs), LIMIT - max(xs))
    dy = rng.randint(-LIMIT - min(ys), LIMIT - max(ys))
    points = [[px + dx, py + dy] for px, py in points]
    last = rng.randrange(N)
    if dent:
        # A vertex whose neighbours both lie along the same step, pushed one unit to the left of
        # that step: inside the polygon, so only its own two edges see it as a dent.
        while True:
            last = rng.randrange(N)
            p, q, r = points[last - 1], points[last], points[(last + 1) % N]
            a, b = q[0] - p[0], q[1] - p[1]
            if (r[0] - q[0], r[1] - q[1]) == (a, b):
                break
        points[last] = [q[0] - b, q[1] + a]
    points = points[last + 1 :] + points[: last + 1]
    if rng.random() < 0.5:
        points = points[-2::-1] + points[-1:]
    return {"points": points}
