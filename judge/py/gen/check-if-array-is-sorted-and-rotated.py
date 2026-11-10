"""Check if Array Is Sorted and Rotated at length 100: a rotated sorted array with duplicates
(true), the same with one swap (usually false), or random."""

SEEDS = 3


def generate(rng):
    nums = sorted(rng.randint(1, 100) for _ in range(100))
    k = rng.randrange(100)
    nums = nums[k:] + nums[:k]
    r = rng.random()
    if r < 0.33:
        i, j = rng.sample(range(100), 2)
        nums[i], nums[j] = nums[j], nums[i]
    elif r < 0.5:
        nums = [rng.randint(1, 100) for _ in range(100)]
    return {"nums": nums}
