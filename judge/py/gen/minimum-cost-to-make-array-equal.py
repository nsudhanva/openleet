"""Minimum Cost to Make Array Equal at n = 2 * 10^4, so pricing every element's value as the
target with a pass over the array is quadratic."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**6


def generate(rng):
    nums = [rng.randint(1, LIMIT) for _ in range(N)]
    cost = [rng.randint(1, LIMIT) for _ in range(N)]
    return {"nums": nums, "cost": cost}
