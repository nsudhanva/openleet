"""Campus Bikes at n = m = 1000: workers on three anti-diagonals in one corner and bikes beyond them
at distinct coordinate sums, so every worker ranks the bikes alike, each assignment takes every
other worker's nearest bike, and both rescanning for the closest free pair and re-finding a worker's
nearest bike are cubic."""

SEEDS = 2
N = M = 1000
SIDE = 1000
L = 450


def generate(rng):
    # Every bike lies above and to the right of every worker, so a worker's distance to a bike
    # is the bike's x + y minus the worker's, nearly the same for all workers.
    band = [(x, s - x) for s in (L - 3, L - 2, L - 1) for x in range(s + 1)]
    points = rng.sample(band, N)
    for s in sorted(rng.sample(range(2 * L, 2 * SIDE - 1), M)):
        x = rng.randint(max(L, s - SIDE + 1), min(SIDE - 1, s - L))
        points.append((x, s - x))
    bikes = points[N:]
    rng.shuffle(bikes)
    # Mirroring the plane keeps every distance and moves the band to another corner.
    fx, fy = rng.randrange(2), rng.randrange(2)
    points = [[SIDE - 1 - x if fx else x, SIDE - 1 - y if fy else y] for x, y in points[:N] + bikes]
    return {"workers": points[:N], "bikes": points[N:]}
