"""Maximum Subarray Sum with One Deletion at n = 10^5 over [-10^4, 10^4], one seed all
negative; trying every deletion is quadratic."""

SEEDS = 3
N = 10**5


def generate(rng):
    high = rng.choice((10**4, -1))
    return {"arr": [rng.randint(-(10**4), high) for _ in range(N)]}
