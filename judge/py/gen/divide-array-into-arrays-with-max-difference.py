"""Divide Array Into Arrays With Max Difference at n = 99,999 (the largest multiple of 3 allowed)
built from triples no wider than k, so the grouping exists. Most seeds list the values from the
largest to the smallest, where bisect.insort moves ~10^5 items per value (2.6 s a seed against
0.1 s for the reference); the others are shuffled. A quadratic sort does ~5 * 10^9 steps."""

from _shapes import pick_shape

SEEDS = 5
N = 99999


def generate(rng):
    k = rng.randint(1, 50)
    nums = []
    for _ in range(N // 3):
        base = rng.randint(1, 10**5 - k)
        nums += [base + rng.randint(0, k) for _ in range(3)]
    if pick_shape(rng) == 1:
        rng.shuffle(nums)
    else:
        nums.sort(reverse=True)
    return {"nums": nums, "k": k}
