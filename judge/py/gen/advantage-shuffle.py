"""Advantage Shuffle at n = 10^5 with distinct values, so a quadratic matching does ~10^10
comparisons."""

SEEDS = 2
N = 10**5


def generate(rng):
    values = rng.sample(range(10**9 + 1), 2 * N)
    rng.shuffle(values)
    return {"nums1": values[:N], "nums2": values[N:]}
