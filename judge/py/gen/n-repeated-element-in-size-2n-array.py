"""N-Repeated Element in Size 2N Array at n = 5000: the repeated value shuffled in, or spaced
as far apart as possible (every other slot)."""

SEEDS = 3
N = 5000


def generate(rng):
    values = rng.sample(range(10**4 + 1), N + 1)
    repeated, others = values[0], values[1:]
    if rng.random() < 0.5:
        nums = [repeated] * N + others
        rng.shuffle(nums)
    else:
        rng.shuffle(others)
        nums = [x for other in others for x in (repeated, other)]
        cut = rng.randrange(2 * N)
        nums = nums[cut:] + nums[:cut]
    return {"nums": nums}
