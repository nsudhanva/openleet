"""Duplicate Zeros at n = 10^4 dense with zeros, punishing insert-and-shift approaches."""

SEEDS = 2
N = 10**4


def generate(rng):
    p = rng.choice([0.5, 0.9])
    return {"arr": [0 if rng.random() < p else rng.randint(1, 9) for _ in range(N)]}
