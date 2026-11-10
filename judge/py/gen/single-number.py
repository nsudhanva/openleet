"""Single Number at n = 29,999: 14,999 shuffled pairs and one single value."""

SEEDS = 2


def generate(rng):
    values = rng.sample(range(-3 * 10**4, 3 * 10**4 + 1), 15000)
    nums = values[:-1] * 2 + [values[-1]]
    rng.shuffle(nums)
    return {"nums": nums}
