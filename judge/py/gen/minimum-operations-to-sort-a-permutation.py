"""Minimum Operations to Sort a Permutation at n = 5 * 10^4: the sorted or reversed order rotated
near the middle, or that with two neighbours swapped (no answer), so trying every rotation with
and without reversals and comparing the whole array is quadratic."""

from _shapes import pick_shape

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    nums = list(range(N)) if shape != 1 else list(range(N - 1, -1, -1))
    z = rng.randrange(N // 4, 3 * N // 4)
    nums = nums[z:] + nums[:z]
    if shape == 2:
        i = rng.randrange(N - 1)
        nums[i], nums[i + 1] = nums[i + 1], nums[i]
    return {"nums": nums}
