"""Single Number III at n = 30,000: 14,999 pairs and two singles across the full 32-bit range."""

SEEDS = 2


def generate(rng):
    values = set()
    while len(values) < 15001:
        values.add(rng.randint(-(2**31), 2**31 - 1))
    values = sorted(values)
    rng.shuffle(values)
    nums = values[:-2] * 2 + values[-2:]
    rng.shuffle(nums)
    return {"nums": nums}
