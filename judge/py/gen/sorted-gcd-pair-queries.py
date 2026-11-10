"""Sorted GCD Pair Queries at n = 10^5 values up to 5 * 10^4 with 10^5 queries over the ~5 * 10^9
pairs, so listing the pairs is impossible."""

from _shapes import pick_shape

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    n = 10**5
    if shape == 0:
        nums = [rng.randint(1, 5 * 10**4) for _ in range(n)]
    elif shape == 1:
        nums = [rng.choice([5 * 10**4, 2 * 3 * 5 * 7 * 11 * 13, 2**15, 3**9]) for _ in range(n)]
    else:
        nums = [rng.randint(1, 10) * rng.choice([1, 2, 4, 8, 16]) for _ in range(n)]
    total = n * (n - 1) // 2
    queries = [rng.choice([0, total - 1, rng.randrange(total)]) for _ in range(10**5)]
    return {"nums": nums, "queries": queries}
