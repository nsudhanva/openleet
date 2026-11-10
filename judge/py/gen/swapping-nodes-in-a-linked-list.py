"""Swapping Nodes in a Linked List at n = 10^5 with k near the middle, the ends, or exactly
the centre of an odd list."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5


def generate(rng):
    shape = pick_shape(rng)
    n = N - 1 if shape == 2 else N
    head = [rng.randint(0, 100) for _ in range(n)]
    if shape == 0:
        k = rng.choice([1, n])
    elif shape == 1:
        k = rng.randint(1, n)
    else:
        k = (n + 1) // 2
    return {"head": head, "k": k}
