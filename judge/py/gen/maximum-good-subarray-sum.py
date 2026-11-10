"""Maximum Good Subarray Sum at n = 10^5: values on a lattice spaced k apart so many pairs
differ by exactly k (pair scans are quadratic), or random values with no good pair."""

SEEDS = 3
N = 10**5
LIMIT = 10**9


def generate(rng):
    if rng.random() < 0.7:
        k = rng.randint(1, 10**4)
        base = rng.randint(-(10**5), 10**5)
        nums = [base + k * rng.randint(-20, 20) for _ in range(N)]
    else:
        k = rng.randint(1, LIMIT)
        nums = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    return {"nums": nums, "k": k}
