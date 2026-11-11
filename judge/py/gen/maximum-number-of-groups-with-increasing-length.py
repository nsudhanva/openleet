"""Maximum Number of Groups With Increasing Length with 3 * 10^4 limits up to n / 4, so the
answer is near n / 2 and trying each group count in turn, from either end, is quadratic."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    return {"usageLimits": [rng.randint(1, N // 4) for _ in range(N)]}
