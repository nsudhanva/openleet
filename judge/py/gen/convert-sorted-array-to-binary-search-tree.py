"""Convert Sorted Array to Binary Search Tree with 2^13 - 1 = 8191 strictly increasing values:
every subarray has odd length, so left- and right-middle choices build the same tree."""

SEEDS = 2
N = 2**13 - 1


def generate(rng):
    if rng.random() < 0.5:
        nums = sorted(rng.sample(range(-(10**4), 10**4 + 1), N))
    else:
        start = rng.randint(-(10**4), 0)
        nums = list(range(start, start + N))
    return {"nums": nums}
