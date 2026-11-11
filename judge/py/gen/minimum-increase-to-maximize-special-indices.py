"""Minimum Increase to Maximize Special Indices at an even n = 6 * 10^4 over the full value
range: the one spare slot can sit after any of n / 2 peaks, and re-summing the peak costs for
each placement is ~10^9 additions."""

SEEDS = 2
N = 6 * 10**4


def generate(rng):
    return {"nums": [rng.randint(1, 10**9) for _ in range(N)]}
