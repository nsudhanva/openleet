"""Median of Two Sorted Arrays at the maximum m = n = 1000 (or one side empty), sorted
values over [-10^6, 10^6]."""

SEEDS = 3


def generate(rng):
    m = rng.choice((1000, 0, rng.randint(1, 999)))
    n = 1000 if m != 1000 else rng.choice((1000, 0, rng.randint(0, 1000)))
    nums1 = sorted(rng.randint(-(10**6), 10**6) for _ in range(m))
    nums2 = sorted(rng.randint(-(10**6), 10**6) for _ in range(n))
    return {"nums1": nums1, "nums2": nums2}
