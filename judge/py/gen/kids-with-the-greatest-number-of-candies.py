"""Kids With the Greatest Number of Candies at the maximum n = 100."""

SEEDS = 2


def generate(rng):
    lo = rng.choice([1, 60])
    return {
        "candies": [rng.randint(lo, 100) for _ in range(100)],
        "extraCandies": rng.randint(1, 50),
    }
