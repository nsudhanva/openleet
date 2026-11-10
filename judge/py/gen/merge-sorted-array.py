"""Merge Sorted Array at m + n = 200, sorted values over [-10^9, 10^9], nums1 padded with n
zeros."""

SEEDS = 3


def generate(rng):
    m = rng.choice((0, 200, rng.randint(1, 199)))
    n = 200 - m
    nums1 = sorted(rng.randint(-(10**9), 10**9) for _ in range(m)) + [0] * n
    nums2 = sorted(rng.randint(-(10**9), 10**9) for _ in range(n))
    return {"nums1": nums1, "m": m, "nums2": nums2, "n": n}
