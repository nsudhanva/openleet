"""Rotate Function at n = 10^5 with values in [-100, 100], so an O(n^2) evaluation of every
rotation does 10^10 work."""

SEEDS = 2


def generate(rng):
    n = 10**5
    if rng.random() < 0.5:
        return {"nums": [rng.randint(-100, 100) for _ in range(n)]}
    return {"nums": [rng.choice([-100, 100]) for _ in range(n)]}
