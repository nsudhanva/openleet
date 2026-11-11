"""Minimum Operations to Make Array Non-decreasing at n = 2 * 10^4 random values, so about half the
steps are drops and raising the whole suffix at each drop is quadratic."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    return {"nums": [rng.randint(1, LIMIT) for _ in range(N)]}
