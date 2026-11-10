"""Sort List at 5 * 10^4 nodes: random, reverse sorted, or few distinct values."""

from _shapes import pick_shape

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        head = [rng.randint(-(10**5), 10**5) for _ in range(N)]
    elif shape == 1:
        head = sorted((rng.randint(-(10**5), 10**5) for _ in range(N)), reverse=True)
    else:
        head = [rng.randint(-2, 2) for _ in range(N)]
    return {"head": head}
