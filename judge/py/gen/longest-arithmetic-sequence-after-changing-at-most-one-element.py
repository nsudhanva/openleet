"""Longest Arithmetic Sequence After Changing At Most One Element at n = 2 * 10^4: long arithmetic
runs with single broken elements, or short runs that break at nearly every position, so trying
each change and rescanning the array costs ~10^8.5 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    lo, hi = (N // 50, N // 5) if shape == 0 else (3, 6) if shape == 1 else (2, 12)
    nums = []
    while len(nums) < N:
        d = rng.randint(-3, 3)
        run = rng.randint(lo, hi)
        start = rng.randint(1, 10**5)
        if not 1 <= start + d * (run - 1) <= 10**5:
            continue
        nums += [start + d * i for i in range(run)]
        # A single broken element inside a long run, mended by changing it.
        if shape == 0 and run > 4:
            k = len(nums) - run + rng.randint(1, run - 2)
            nums[k] = rng.randint(1, 10**5)
    return {"nums": nums[:N]}
