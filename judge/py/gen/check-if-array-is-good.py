"""Check if Array is Good at the maximum length 100: a shuffled base[99] permutation (true) or
one with a single value changed (false)."""

SEEDS = 3


def generate(rng):
    n = 99
    nums = [*range(1, n + 1), n]
    if rng.random() < 0.5:
        nums[rng.randrange(len(nums))] = rng.randint(1, 200)
    rng.shuffle(nums)
    return {"nums": nums}
