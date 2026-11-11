"""Widest Pair of Indices With Equal Range Sum at 2 * 10^4 bits whose running difference
drifts upward, so equal sums sit close together and scanning pairs widest-first is ~2 * 10^8
steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    nums1, nums2 = [], []
    for _ in range(N):
        r = rng.random()
        a, b = (1, 0) if r < 0.5 else (0, 1) if r < 0.6 else (1, 1) if r < 0.8 else (0, 0)
        nums1.append(a)
        nums2.append(b)
    return {"nums1": nums1, "nums2": nums2}
