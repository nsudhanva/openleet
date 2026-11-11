"""Count Number of Distinct Integers After Reverse Operations at n = 10^5 distinct values, so a
list-based dedupe scans ~2 * 10^10 entries."""

SEEDS = 2
N = 10**5
LIMIT = 10**6


def generate(rng):
    return {"nums": rng.sample(range(1, LIMIT + 1), N)}
