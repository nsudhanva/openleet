"""Split Array into Consecutive Subsequences at n = 10^4 sorted values in [-1000, 1000]: built
from overlapping runs of length >= 3 (true), the same with one value removed (often false), or
random sorted."""

from _shapes import pick_shape

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    if shape == 2:
        return {"nums": sorted(rng.randint(-1000, 1000) for _ in range(10**4))}
    nums = []
    while True:
        length = rng.randint(3, 60)
        start = rng.randint(-1000, 1000 - length + 1)
        if len(nums) + length > 10**4:
            break
        nums += range(start, start + length)
    nums.sort()
    if shape == 1:
        nums.pop(rng.randrange(len(nums)))
    return {"nums": nums}
