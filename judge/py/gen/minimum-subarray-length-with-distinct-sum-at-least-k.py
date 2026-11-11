"""Minimum Subarray Length With Distinct Sum at Least K at n = 2 * 10^4 drawn from 10^4 values, with
k the distinct sum of a window of a third or half of the array, or above the whole array's (no
answer), so growing a window from every start is quadratic against two pointers."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4
POOL = 10**4
LIMIT = 10**5


def generate(rng):
    shape = pick_shape(rng)
    pool = rng.sample(range(1, LIMIT + 1), POOL)
    nums = [rng.choice(pool) for _ in range(N)]
    if shape == 0:
        k = sum(set(nums)) + 1
    else:
        length = N // (shape + 1)
        start = rng.randrange(N - length + 1)
        k = sum(set(nums[start : start + length]))
    return {"nums": nums, "k": k}
