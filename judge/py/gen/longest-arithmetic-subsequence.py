"""Longest Arithmetic Subsequence at the maximum n = 1500: random values with a planted
progression, all one value, or only 0 and 1, so extending every pair greedily over the rest of
the array costs ~10^9 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 1500


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        # Every pair extends through the whole array.
        return {"nums": [rng.randint(0, 500)] * N}
    if shape == 1:
        # Two values: the pairs with difference 0 extend through half the array.
        lo = rng.randint(0, 499)
        return {"nums": [lo + rng.randint(0, 1) for _ in range(N)]}
    nums = [rng.randint(0, 500) for _ in range(N)]
    # One planted progression spread over the array, longer than any random one.
    d = rng.randint(1, 4)
    start = rng.randint(0, 500 - 40 * d)
    pos = sorted(rng.sample(range(N), 40))
    for i, p in enumerate(pos):
        nums[p] = start + d * i
    return {"nums": nums}
