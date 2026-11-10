"""Minimum Number of Arrows at 10^5 balloons spanning the full 32-bit range, including the
extreme endpoints -2^31 and 2^31 - 1 (overflow traps)."""

SEEDS = 3
N = 10**5
LOW, HIGH = -(2**31), 2**31 - 1


def generate(rng):
    span = rng.choice((10, 10**6, 2**32))
    points = []
    for _ in range(N):
        a = rng.randint(LOW, HIGH - 1)
        points.append([a, rng.randint(a + 1, min(HIGH, a + span))])
    points[rng.randrange(N)] = [LOW, rng.randint(LOW + 1, HIGH)]
    points[rng.randrange(N)] = [rng.randint(LOW, HIGH - 1), HIGH]
    return {"points": points}
