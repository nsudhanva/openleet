"""Largest Almost Missing Integer at n = 50 with values in [0, 50] and k across its range."""

SEEDS = 3


def generate(rng):
    hi = rng.choice([5, 50])
    nums = [rng.randint(0, hi) for _ in range(50)]
    return {"nums": nums, "k": rng.choice([1, 50, rng.randint(1, 50)])}
