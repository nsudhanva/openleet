"""Maximum Balanced Subsequence Sum at n = 2 * 10^4 over the full value range, so the quadratic
DP over every earlier index is 2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    return {"nums": [rng.randint(-LIMIT, LIMIT) for _ in range(N)]}
