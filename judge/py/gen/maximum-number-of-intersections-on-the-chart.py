"""Maximum Number of Intersections on the Chart with 10^4 random points, so counting the
crossings of every candidate line separately is quadratic."""

SEEDS = 2
N = 10**4
LIMIT = 10**9


def generate(rng):
    y = [rng.randint(1, LIMIT)]
    while len(y) < N:
        v = rng.randint(1, LIMIT)
        if v != y[-1]:
            y.append(v)
    return {"y": y}
