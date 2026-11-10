"""Unique XOR Triplets at n = 10^5: a shuffled permutation of 1..n, far too many triplets to
enumerate."""

SEEDS = 2


def generate(rng):
    n = rng.choice([10**5, rng.randint(9 * 10**4, 10**5)])
    nums = list(range(1, n + 1))
    rng.shuffle(nums)
    return {"nums": nums}
