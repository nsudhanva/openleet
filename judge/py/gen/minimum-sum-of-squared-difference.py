"""Minimum Sum of Squared Difference at n = 10^5 with k1 + k2 up to 2 * 10^9: enough to zero
everything, or just short, so decrementing one unit at a time is hopeless."""

SEEDS = 3
N = 10**5


def generate(rng):
    nums1 = [rng.randint(0, 10**5) for _ in range(N)]
    nums2 = [rng.randint(0, 10**5) for _ in range(N)]
    total = sum(abs(a - b) for a, b in zip(nums1, nums2, strict=True))
    budget = max(0, rng.choice((total, total - 1, total // 3, 0)))
    k1 = rng.randint(0, min(budget, 10**9))
    k2 = min(budget - k1, 10**9)
    return {"nums1": nums1, "nums2": nums2, "k1": k1, "k2": k2}
