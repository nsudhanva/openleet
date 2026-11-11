"""Bitwise XOR of All Pairings at ~10^4 values per array (odd lengths, or one odd and one even),
so XORing every pair is ~10^8 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    m = N + rng.choice([0, 1])
    nums1 = [rng.randint(0, 10**9) for _ in range(N + 1)]
    return {"nums1": nums1, "nums2": [rng.randint(0, 10**9) for _ in range(m)]}
