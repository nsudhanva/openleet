"""Maximum Number of Coins You Can Get with 3 * 10^4 random piles, so taking each triple by
repeated scans for the largest and smallest is quadratic."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    return {"piles": [rng.randint(1, 10**4) for _ in range(N)]}
