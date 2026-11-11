"""Maximum Length of Subarray With Positive Product at n = 2 * 10^4 with rare zeros, so tracking
the sign from every start is 2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def value(rng):
    if rng.random() < 0.0005:
        return 0
    return rng.randint(1, LIMIT) * rng.choice((1, -1))


def generate(rng):
    return {"nums": [value(rng) for _ in range(N)]}
