"""Find the Highest Altitude at n = 100 with gains in [-100, 100]."""

SEEDS = 2


def generate(rng):
    return {"gain": [rng.randint(-100, 100) for _ in range(100)]}
