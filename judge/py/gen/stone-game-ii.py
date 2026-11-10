"""Stone Game II at the maximum 100 piles, values up to 10^4 (exponential without memoization)."""

SEEDS = 2


def generate(rng):
    return {"piles": [rng.randint(1, 10**4) for _ in range(100)]}
