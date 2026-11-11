"""Minimum Operations to Make Binary Array Elements Equal to One I at n = 5 * 10^4, made by
flipping a random half of the triples of an all-ones array, so ~2.5 * 10^4 flips are needed and
rescanning from the start for the first zero before each flip is quadratic."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    nums = [1] * N
    for i in range(N - 2):
        if rng.random() < 0.5:
            for j in range(i, i + 3):
                nums[j] ^= 1
    return {"nums": nums}
