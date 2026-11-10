"""K-th Smallest Pair Distance at n = 10^4 (about 5 * 10^7 pairs), values clustered or spread
over [0, 10^6], k anywhere in range."""

SEEDS = 3
N = 10**4


def generate(rng):
    hi = rng.choice([100, 10**6])
    nums = [rng.randint(0, hi) for _ in range(N)]
    total = N * (N - 1) // 2
    k = rng.choice([1, total, rng.randint(1, total)])
    return {"nums": nums, "k": k}
