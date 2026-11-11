"""Minimum Skips to Arrive at Meeting on Time at n = 1000 (the limit) with every road under an hour
and about n / 2 hours to spare, so ~500 skips are needed and rerunning the skip DP for each
skip budget 0, 1, 2, ... is cubic against the one quadratic DP."""

SEEDS = 2
N = 1000
DIST = 10**5
SPEED = 10**6


def generate(rng):
    speed = rng.randint(SPEED // 2, SPEED)
    dist = [rng.randint(1, DIST) for _ in range(N)]
    return {"dist": dist, "speed": speed, "hoursBefore": N // 2 + rng.randint(-N // 10, N // 10)}
