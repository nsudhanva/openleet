"""Kth Smallest Product of Two Sorted Arrays at 4000 values each with mixed signs and k in the
middle, so merging the 1.6 * 10^7 products in order reaches ~8 * 10^6 of them."""

SEEDS = 2
N = 4000
LIMIT = 10**5


def generate(rng):
    nums1 = sorted(rng.randint(-LIMIT, LIMIT) for _ in range(N))
    nums2 = sorted(rng.randint(-LIMIT, LIMIT) for _ in range(N))
    k = rng.randint(N * N * 2 // 5, N * N * 3 // 5)
    return {"nums1": nums1, "nums2": nums2, "k": k}
