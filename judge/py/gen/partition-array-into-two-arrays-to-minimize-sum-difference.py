"""Minimize Sum Difference at the maximum 2n = 30 values, where trying all C(30, 15) splits is
too slow and meet-in-the-middle is required."""

SEEDS = 2


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(-(10**7), 10**7) for _ in range(30)]
    else:
        nums = [rng.randint(10**7 - 1000, 10**7) * rng.choice([1, -1]) for _ in range(30)]
    return {"nums": nums}
