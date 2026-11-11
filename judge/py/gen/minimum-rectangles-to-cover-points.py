"""Minimum Rectangles to Cover Points with 2 * 10^4 points spread over x in [0, 10^9] and w up to
10^4, so nearly every point needs its own rectangle and finding the leftmost uncovered point by
a scan each time is quadratic."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9
WIDTH = 10**4


def generate(rng):
    points = set()
    while len(points) < N:
        points.add((rng.randint(0, LIMIT), rng.randint(0, LIMIT)))
    points = [list(p) for p in points]
    rng.shuffle(points)
    return {"points": points, "w": rng.randint(0, WIDTH)}
