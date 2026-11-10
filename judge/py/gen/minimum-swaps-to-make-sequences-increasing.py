"""Minimum Swaps To Make Sequences Increasing at n = 10^5, built from two strictly increasing
sequences with random columns swapped, so a valid answer always exists."""

SEEDS = 3
N = 10**5
TOP = 2 * 10**5


def generate(rng):
    a = sorted(rng.sample(range(TOP + 1), N))
    b = sorted(rng.sample(range(TOP + 1), N))
    rate = rng.choice((0.5, 0.1))
    for i in range(N):
        if rng.random() < rate:
            a[i], b[i] = b[i], a[i]
    return {"nums1": a, "nums2": b}
