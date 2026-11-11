"""Number of Equivalent Domino Pairs at 2 * 10^4 dominoes over all 45 unordered value pairs, so
comparing every pair of dominoes costs 2 * 10^8 checks."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    return {"dominoes": [[rng.randint(1, 9), rng.randint(1, 9)] for _ in range(N)]}
