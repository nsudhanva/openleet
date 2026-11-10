"""Valid Permutations for DI Sequence at the maximum n = 200, where only the O(n^2) prefix-sum
DP is fast."""

from _shapes import pick_shape

SEEDS = 3
N = 200


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        s = "".join(rng.choice("ID") for _ in range(N))
    elif shape == 1:
        s = "ID" * (N // 2)
    else:
        s = "".join("D" if rng.random() < 0.8 else "I" for _ in range(N))
    return {"s": s}
