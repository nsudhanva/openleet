"""Maximum Median Sum of Subsequences of Size 3 with 3 * 10^4 random values, so removing the
largest and smallest by repeated scans is quadratic."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    return {"nums": [rng.randint(1, 10**9) for _ in range(N)]}
