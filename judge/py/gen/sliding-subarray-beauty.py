"""Sliding Subarray Beauty at n = 4 * 10^4 with k = 2 * 10^4, so sorting every window costs
~2 * 10^4 sorts of 2 * 10^4 values."""

SEEDS = 2
N = 4 * 10**4
K = 2 * 10**4


def generate(rng):
    nums = [rng.randint(-50, 50) for _ in range(N)]
    x = rng.choice([rng.randint(1, K), K - rng.randrange(10)])
    return {"nums": nums, "k": K, "x": x}
