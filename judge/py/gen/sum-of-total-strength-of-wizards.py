"""Sum of Total Strength of Wizards at n = 2 * 10^4, so extending every subarray while tracking its
minimum and sum is ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    hi = rng.choice((10**9, 1000))
    return {"strength": [rng.randint(1, hi) for _ in range(N)]}
