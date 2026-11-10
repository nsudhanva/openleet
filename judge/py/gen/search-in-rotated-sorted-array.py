"""Search in Rotated Sorted Array at n = 5000 distinct values, rotated at a random pivot,
target present or absent."""

SEEDS = 3


def generate(rng):
    present = rng.random() < 0.6
    n = 5000
    values = sorted(rng.sample(range(-(10**4), 10**4 + 1), n))
    k = rng.randrange(n)
    nums = values[k:] + values[:k]
    if present:
        target = rng.choice(nums)
    else:
        seen = set(nums)
        target = rng.randint(-(10**4), 10**4)
        while target in seen:
            target = rng.randint(-(10**4), 10**4)
    return {"nums": nums, "target": target}
