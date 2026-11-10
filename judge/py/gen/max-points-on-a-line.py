"""Max Points on a Line with 300 unique points: several dense lines (including vertical and
horizontal) mixed with noise, or points on a small grid where many slopes tie."""

SEEDS = 2
N = 300
LIMIT = 10**4


def generate(rng):
    points = set()
    if rng.random() < 0.5:
        side = 18
        while len(points) < N:
            points.add((rng.randint(0, side - 1), rng.randint(0, side - 1)))
    else:
        for _ in range(rng.randint(3, 6)):
            x0, y0 = rng.randint(-100, 100), rng.randint(-100, 100)
            dx, dy = rng.choice([(1, 0), (0, 1), (1, 1), (2, -3), (7, 5), (-1, 4)])
            for t in range(rng.randint(20, 60)):
                x, y = x0 + dx * t, y0 + dy * t
                if -LIMIT <= x <= LIMIT and -LIMIT <= y <= LIMIT:
                    points.add((x, y))
                if len(points) >= N:
                    break
        while len(points) < N:
            points.add((rng.randint(-LIMIT, LIMIT), rng.randint(-LIMIT, LIMIT)))
    pts = [list(p) for p in sorted(points)]
    rng.shuffle(pts)
    return {"points": pts}
