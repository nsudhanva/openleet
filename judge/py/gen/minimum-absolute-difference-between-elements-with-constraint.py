"""Minimum Absolute Difference Between Elements With Constraint at n = 2 * 10^4 distinct values
and a small x, so comparing every far-enough pair is about 2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9
GAP = 100


def generate(rng):
    nums = rng.sample(range(1, LIMIT + 1), N)
    return {"nums": nums, "x": rng.randint(1, GAP)}
