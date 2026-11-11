"""pref of 5 * 10^4 values, so rebuilding each element by xoring all the earlier ones costs
~1.25 * 10^9 steps."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    return {"pref": [rng.randint(0, 10**6) for _ in range(N)]}
