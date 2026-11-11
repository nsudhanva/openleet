"""Minimum Absolute Sum Difference at n = 2 * 10^4 with nums1 below 5 * 10^4 and nums2 above it,
so every index has a large difference but a small gain, no pruning stops early, and trying every
replacement value for every index is 4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**5


def generate(rng):
    nums1 = [rng.randint(1, LIMIT // 2) for _ in range(N)]
    nums2 = [rng.randint(LIMIT // 2 + 1, LIMIT) for _ in range(N)]
    return {"nums1": nums1, "nums2": nums2}
