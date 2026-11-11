"""Maximum Alternating Subarray Sum at n = 2 * 10^4 over the full value range, so summing from
every start is 2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**5


def generate(rng):
    return {"nums": [rng.randint(-LIMIT, LIMIT) for _ in range(N)]}
