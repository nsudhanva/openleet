"""Distinct Element Sum of Squares I at the maximum n = 100, all distinct or from few values."""

SEEDS = 2
N = 100


def generate(rng):
    if rng.random() < 0.5:
        nums = rng.sample(range(1, 101), N)
    else:
        nums = [rng.randint(1, 5) for _ in range(N)]
    return {"nums": nums}
