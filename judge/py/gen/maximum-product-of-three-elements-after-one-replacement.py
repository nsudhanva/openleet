"""Maximum Product of Three Elements After One Replacement with 2 * 10^4 random values, so trying
every pair to multiply by the replacement is quadratic."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    return {"nums": [rng.randint(-(10**5), 10**5) for _ in range(N)]}
