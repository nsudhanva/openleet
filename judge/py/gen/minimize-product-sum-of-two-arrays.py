"""Minimize Product Sum of Two Arrays at n = 5 * 10^4, so pairing by repeatedly scanning for
the smallest and largest remaining values is quadratic."""

SEEDS = 2
N = 5 * 10**4
LIMIT = 100


def generate(rng):
    nums1 = [rng.randint(1, LIMIT) for _ in range(N)]
    nums2 = [rng.randint(1, LIMIT) for _ in range(N)]
    return {"nums1": nums1, "nums2": nums2}
