"""3Sum Closest at the maximum n = 500 with random values and target, so a cubic scan does
~2 * 10^7 triples."""

SEEDS = 2


def generate(rng):
    nums = [rng.randint(-1000, 1000) for _ in range(500)]
    target = rng.randint(-(10**4), 10**4) if rng.random() < 0.5 else rng.randint(-3000, 3000)
    return {"nums": nums, "target": target}
