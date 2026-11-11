"""Number of Sub-arrays With Odd Sum at 2 * 10^4 values, so summing every subarray costs
2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    return {"arr": [rng.randint(1, 100) for _ in range(N)]}
