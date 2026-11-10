"""Single Number II at n = 29,998: 9,999 values three times each (full 32-bit range, negatives
included) plus one single."""

SEEDS = 2


def generate(rng):
    values = set()
    while len(values) < 10000:
        values.add(rng.randint(-(2**31), 2**31 - 1))
    values = sorted(values)
    rng.shuffle(values)
    nums = values[:-1] * 3 + [values[-1]]
    rng.shuffle(nums)
    return {"nums": nums}
