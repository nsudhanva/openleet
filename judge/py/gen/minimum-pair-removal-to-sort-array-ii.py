"""Minimum Pair Removal to Sort Array II at n = 2 * 10^4 random values in [-10^9, 10^9], which take
n - 1 merges to sort, so finding each minimum-sum pair by a scan of the array is quadratic."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    return {"nums": [rng.randint(-LIMIT, LIMIT) for _ in range(N)]}
