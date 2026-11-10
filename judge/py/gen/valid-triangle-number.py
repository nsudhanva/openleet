"""Valid Triangle Number at n = 1000, where the O(n^3) triple loop is 1.7 * 10^8 checks:
random values, values with zeros, or all equal (every triple counts)."""

from _shapes import pick_shape

SEEDS = 3
N = 1000


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        nums = [rng.randint(0, 1000) for _ in range(N)]
    elif shape == 1:
        nums = [rng.choice([0, 0, rng.randint(1, 1000)]) for _ in range(N)]
    else:
        nums = [rng.randint(900, 1000) for _ in range(N)]
    return {"nums": nums}
