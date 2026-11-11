"""Line Reflection at the maximum n = 10^4 with every point on one horizontal line (repeats
included), symmetric or with one mirror pair broken at the end of the list, so searching for
each point's mirror among the points costs ~5 * 10^7 comparisons."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4
LIMIT = 10**8


def generate(rng):
    shape = pick_shape(rng)
    mid = rng.randint(-LIMIT // 10, LIMIT // 10)
    y = rng.randint(-LIMIT, LIMIT)
    dxs = rng.sample(range(1, LIMIT // 2), N // 2)
    if shape == 1:
        # Some points are repeated.
        for i in rng.sample(range(1, N // 2), N // 40):
            dxs[i] = dxs[i - 1]
    points = []
    for dx in dxs:
        points += [[mid - dx, y], [mid + dx, y]]
    rng.shuffle(points)
    if shape == 2:
        # Move one point that is not an extreme by one step, then put it and its old mirror last.
        lo = min(p[0] for p in points)
        hi = max(p[0] for p in points)
        i = next(i for i, p in enumerate(points) if lo < p[0] < hi)
        x = points[i][0]
        j = next(j for j, p in enumerate(points) if p[0] == 2 * mid - x)
        bad = [[x + 1, y], points[j]]
        points = [p for k, p in enumerate(points) if k not in (i, j)] + bad
    return {"points": points}
