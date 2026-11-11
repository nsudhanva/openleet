"""Maximum Product After K Increments with n = k = 5 * 10^4 and values close together, so finding
the smallest value by a scan for every increment is quadratic."""

SEEDS = 2
N = K = 5 * 10**4


def generate(rng):
    base = rng.randint(0, 10**6 - 10)
    return {"nums": [base + rng.randint(0, 10) for _ in range(N)], "k": K}
