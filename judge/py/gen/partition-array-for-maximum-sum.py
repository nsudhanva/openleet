"""Partition Array for Maximum Sum at n = 500 with a large k, the worst case for the O(n * k)
DP and far too many partitions to enumerate."""

SEEDS = 2
N = 500


def generate(rng):
    arr = [rng.randint(0, 10**9) for _ in range(N)]
    k = rng.choice([rng.randint(100, N), N])
    return {"arr": arr, "k": k}
