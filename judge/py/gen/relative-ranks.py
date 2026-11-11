"""Relative Ranks at n = 10^4 unique scores across the full range."""

SEEDS = 2
N = 10**4


def generate(rng):
    score = rng.sample(range(10**6 + 1), N)
    if rng.random() < 0.5:
        score.sort()
    return {"score": score}
