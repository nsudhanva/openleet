"""Minimum Difference in Sums After Removal of Elements at n = 30,000 (90,000 values over the full
range): keeping both sides sorted and re-summing them at each of the n + 1 split points is
~10^9 element moves."""

SEEDS = 2
N = 30000


def generate(rng):
    return {"nums": [rng.randint(1, 10**5) for _ in range(3 * N)]}
