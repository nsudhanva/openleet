"""1000 points: a rising chain in the upper left and another in the lower right, so every one
of the ~2.5 * 10^5 cross pairs is valid and checking each against all points costs ~2.5 * 10^8."""

SEEDS = 2
N = 1000
LIMIT = 10**9


def generate(rng):
    a = rng.randint(N // 2 - 50, N // 2 + 50)
    b = N - a
    # Left chain: x < 0, y > 0, both rising; right chain: x >= 0, y <= 0, both rising.
    lx = sorted(rng.sample(range(-LIMIT, 0), a))
    ly = sorted(rng.sample(range(1, LIMIT + 1), a))
    rx = sorted(rng.sample(range(0, LIMIT + 1), b))
    ry = sorted(rng.sample(range(-LIMIT, 1), b))
    points = [[x, y] for x, y in zip(lx, ly, strict=True)] + [
        [x, y] for x, y in zip(rx, ry, strict=True)
    ]
    rng.shuffle(points)
    return {"points": points}
