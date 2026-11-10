"""Array Partition at the maximum 2 * 10^4 values: random, or reverse sorted with heavy
duplicates."""

SEEDS = 2


def generate(rng):
    nums = [rng.randint(-(10**4), 10**4) for _ in range(2 * 10**4)]
    if rng.random() < 0.5:
        nums = sorted((v // 50 for v in nums), reverse=True)
    return {"nums": nums}
