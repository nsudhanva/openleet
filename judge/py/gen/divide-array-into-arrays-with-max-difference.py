"""Divide Array Into Arrays With Max Difference at n = 99,999 (the largest multiple of 3 allowed)
built from triples no wider than k, shuffled, so the grouping exists and a quadratic sort does
~5 * 10^9 steps."""

SEEDS = 2
N = 99999


def generate(rng):
    k = rng.randint(1, 50)
    nums = []
    for _ in range(N // 3):
        base = rng.randint(1, 10**5 - k)
        nums += [base + rng.randint(0, k) for _ in range(3)]
    rng.shuffle(nums)
    return {"nums": nums, "k": k}
