"""Remove One Element to Make the Array Strictly Increasing at the maximum 1000 elements, rising
until the last one or two, so checking every removal costs ~10^6 steps."""

SEEDS = 2
N = 1000


def generate(rng):
    drops = rng.choice((1, 2))
    nums = sorted(rng.sample(range(1, 1001), N - drops))
    # One drop at the very end: only cutting it (or its left neighbour) works. Two drops: nothing
    # does.
    a = rng.randint(drops, nums[-1] - 1)
    nums.append(a)
    if drops == 2:
        nums.append(rng.randint(1, a - 1))
    return {"nums": nums}
