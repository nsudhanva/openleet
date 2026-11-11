"""Kth Smallest Subarray Sum at n = 4000 with k in the middle of the 8 * 10^6 subarrays, so
listing subarray sums in increasing order reaches ~4 * 10^6 of them."""

SEEDS = 2
N = 4000


def generate(rng):
    nums = [rng.randint(1, 5 * 10**4) for _ in range(N)]
    total = N * (N + 1) // 2
    return {"nums": nums, "k": rng.randint(total * 2 // 5, total * 3 // 5)}
