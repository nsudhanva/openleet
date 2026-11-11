"""Collecting Chocolates at the maximum n = 1000 with a small rotation cost x (at most 1000), so
rotating keeps paying off and taking each type's window minimum afresh for every rotation count
costs ~n^3 / 2 steps with no early exit."""

SEEDS = 3
N = 1000


def generate(rng):
    nums = [rng.randint(1, 10**9) for _ in range(N)]
    return {"nums": nums, "x": rng.randint(1, 1000)}
