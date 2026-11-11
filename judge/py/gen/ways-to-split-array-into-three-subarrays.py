"""Ways to Split Array Into Three Subarrays at 3 * 10^4 numbers, mostly zeros among small
values so many splits are good, and trying every pair of cut points is ~4.5 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    nums = [0 if rng.random() < 0.7 else rng.randint(0, 10) for _ in range(N)]
    return {"nums": nums}
