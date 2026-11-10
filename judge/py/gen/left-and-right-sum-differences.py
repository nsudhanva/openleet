"""Left and Right Sum Differences at n = 1000 with values up to 10^5."""

SEEDS = 2


def generate(rng):
    return {"nums": [rng.randint(1, 10**5) for _ in range(1000)]}
