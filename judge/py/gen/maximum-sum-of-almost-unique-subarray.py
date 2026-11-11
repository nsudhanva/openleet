"""Maximum Sum of Almost Unique Subarray at the maximum n = 2 * 10^4 with k = n / 2: k distinct
small values, then large sorted values with at most 90 distinct, so window sums keep rising while
only the early windows qualify, and counting a window's distinct values afresh costs ~10^8."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    k = N // 2
    first = rng.sample(range(1, 10**6), k)
    late = sorted(rng.choice(range(10**8, 10**9, 10**7)) for _ in range(N - k))
    return {"nums": [*first, *late], "m": rng.randint(k // 3, k // 2), "k": k}
