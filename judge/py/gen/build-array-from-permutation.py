"""Build Array from Permutation at the maximum length 1000: a random permutation."""

SEEDS = 2


def generate(rng):
    nums = list(range(1000))
    rng.shuffle(nums)
    return {"nums": nums}
