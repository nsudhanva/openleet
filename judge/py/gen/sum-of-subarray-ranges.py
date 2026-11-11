"""Sum of Subarray Ranges at the full n = 1000, so taking the max and min of every subarray afresh
is ~3 * 10^8 element steps."""

SEEDS = 2
N = 1000


def generate(rng):
    return {"nums": [rng.randint(-(10**9), 10**9) for _ in range(N)]}
