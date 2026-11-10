"""Shortest Subarray with Sum >= K at n = 10^5 with mixed-sign values and a large k (long or no
answer), so the quadratic scan does ~5 * 10^9 work."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        nums = [rng.randint(-(10**5), 10**5) for _ in range(N)]
        k = rng.randint(10**6, 10**8)
    elif shape == 1:
        nums = [rng.randint(-50, 100) for _ in range(N)]
        k = rng.randint(10**5, 2 * 10**6)
    else:
        nums = [rng.randint(1, 10**5) for _ in range(N)]
        k = 10**9
    return {"nums": nums, "k": k}
