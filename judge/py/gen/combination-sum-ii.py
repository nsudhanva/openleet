"""Combination Sum II at the maximum 100 candidates, all duplicates of a few small values, with
target 20 to 30, so backtracking without skipping equal values explores an enormous tree."""

SEEDS = 2


def generate(rng):
    hi = rng.choice([3, 6, 10])
    candidates = [rng.randint(1, hi) for _ in range(100)]
    return {"candidates": candidates, "target": rng.randint(20, 30)}
