"""Count Pairs That Form a Complete Day II at n = 2 * 10^4 hours, so checking every pair costs
2 * 10^8 tests."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    return {"hours": [rng.randint(1, LIMIT) for _ in range(N)]}
