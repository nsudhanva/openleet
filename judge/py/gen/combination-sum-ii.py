"""Combination Sum II at 100 candidates full of duplicates of small values with target up to
30, so backtracking without duplicate skipping explores an enormous tree."""

SEEDS = 3


def generate(rng):
    hi = rng.choice([3, 6, 10, 50])
    candidates = [rng.randint(1, hi) for _ in range(100)]
    return {"candidates": candidates, "target": rng.randint(20, 30)}
