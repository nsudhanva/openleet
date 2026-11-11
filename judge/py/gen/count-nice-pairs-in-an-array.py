"""Count Nice Pairs in an Array at n = 2 * 10^4 with values of a few digits (many share
x - rev(x)) or spread up to 10^9, so testing every pair costs 2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    top = 10**4 if rng.random() < 0.5 else 10**9
    return {"nums": [rng.randint(0, top) for _ in range(N)]}
