"""Erect the Fence II at the maximum 3000 trees: the ~450 convex-hull vertices of a lattice disk
plus random trees inside it, shuffled, so trying every pair and triple of trees (or of hull
vertices) as the circle's boundary is over 10^10 checks."""

import math

SEEDS = 2
N = 3000
TOP = 3000


def hull(pts):
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    pts = sorted(pts)
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def generate(rng):
    c = TOP / 2 + rng.random() - 0.5
    r = TOP / 2 - 1
    # The outermost lattice point of each column inside the circle; their hull has ~450 vertices.
    edge = []
    for x in range(TOP + 1):
        dx = x - c
        if dx * dx <= r * r:
            h = math.isqrt(int(r * r - dx * dx))
            edge += [(x, y) for y in (int(c) + h, int(c) - h) if 0 <= y <= TOP]
    rim = hull(edge)
    trees = set(rng.sample(rim, N) if len(rim) > N else rim)
    while len(trees) < N:
        x, y = rng.randint(0, TOP), rng.randint(0, TOP)
        if (x - c) ** 2 + (y - c) ** 2 <= (0.9 * r) ** 2:
            trees.add((x, y))
    trees = [list(t) for t in sorted(trees)]
    rng.shuffle(trees)
    return {"trees": trees}
