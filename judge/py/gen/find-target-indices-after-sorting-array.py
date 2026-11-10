"""Find Target Indices After Sorting at n = 100 with values in [1, 100]."""

SEEDS = 2


def generate(rng):
    hi = rng.choice([5, 100])
    nums = [rng.randint(1, hi) for _ in range(100)]
    return {"nums": nums, "target": rng.randint(1, hi)}
