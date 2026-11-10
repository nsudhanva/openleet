"""Patching Array with 1000 sorted values and n near 2^31 - 1, so a set-of-sums approach is
hopeless and the greedy must patch repeatedly."""

SEEDS = 2


def generate(rng):
    if rng.random() < 0.5:
        nums = sorted(rng.randint(1, 10**4) for _ in range(1000))
    else:
        nums = sorted(rng.randint(5000, 10**4) for _ in range(1000))
    return {"nums": nums, "n": rng.randint(2**31 - 1000, 2**31 - 1)}
