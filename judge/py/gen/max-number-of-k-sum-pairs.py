"""Max Number of K-Sum Pairs at n = 10^5: values drawn from a few complementary pairs (many
operations, nested scans are quadratic), or wide random values."""

SEEDS = 3
N = 10**5


def generate(rng):
    if rng.random() < 0.6:
        k = rng.randint(2, 10**9)
        pool = []
        for _ in range(rng.randint(1, 50)):
            a = rng.randint(1, k - 1) if k > 1 else 1
            pool.extend([a, k - a])
        nums = [rng.choice(pool) for _ in range(N)]
    else:
        nums = [rng.randint(1, 10**9) for _ in range(N)]
        k = rng.randint(1, 10**9)
    return {"nums": nums, "k": k}
