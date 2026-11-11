"""Split Array into Consecutive Subsequences at n = 10^4 sorted values: ~3000 runs of length 3
or 4 piled on a window of 3 to 5 values (or that plus a lone last value, false), so a greedy
that scans its list of subsequences for every value does ~10^7 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4


def generate(rng):
    shape = pick_shape(rng)
    width = (4, 5, 3)[shape]
    longest = min(width, 4)
    base = rng.randint(-1000, 1000 - width - 2)
    nums = []
    while True:
        length = rng.randint(3, longest)
        start = base + rng.randint(0, width - length)
        if len(nums) + length > N:
            break
        nums += range(start, start + length)
    nums.sort()
    if shape == 1:
        # A lone value past the window ends the list, so no split exists.
        nums[-1] = base + width + 1
    return {"nums": nums}
