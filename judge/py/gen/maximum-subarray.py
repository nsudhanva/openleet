"""Maximum Subarray at n = 10^5 over [-10^4, 10^4], one shape all negative, so the quadratic
scan does 5 * 10^9 steps."""

SEEDS = 3
N = 10**5


def generate(rng):
    high = rng.choice((10**4, -1))
    return {"nums": [rng.randint(-(10**4), high) for _ in range(N)]}
