"""New 21 Game at n, k, maxPts up to 10^4, so the plain O(n * maxPts) DP does 10^8 steps."""

SEEDS = 3
TOP = 10**4


def generate(rng):
    n = rng.choice((TOP, rng.randint(1, TOP)))
    k = rng.choice((n, rng.randint(0, n)))
    return {"n": n, "k": k, "maxPts": rng.choice((TOP, rng.randint(1, TOP)))}
