"""Split Array Largest Sum at n = 1000 with values up to 10^6 and k up to 50, so the O(k * n^2)
DP is slow and sums exceed 32 bits."""

from _shapes import pick_shape

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    n = 1000
    if shape == 0:
        nums = [rng.randint(0, 10**6) for _ in range(n)]
    elif shape == 1:
        nums = [10**6] * n
    else:
        nums = [rng.choice([0, 0, 0, 10**6]) for _ in range(n)]
    return {"nums": nums, "k": rng.choice([50, 1, rng.randint(2, 49)])}
