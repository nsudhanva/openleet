"""Search Insert Position on 10^4 distinct sorted values, target present, absent, or beyond
either end."""

SEEDS = 3


def generate(rng):
    shape = rng.getrandbits(6) % 3
    nums = sorted(rng.sample(range(-(10**4), 10**4 + 1), 10**4))
    present = set(nums)
    if shape == 0:
        target = rng.choice(nums)
    elif shape == 1:
        target = rng.choice([v for v in range(-(10**4), 10**4 + 1) if v not in present])
    else:
        target = 10**4 if 10**4 not in present else nums[-1]
    return {"nums": nums, "target": target}
