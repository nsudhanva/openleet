"""Set Mismatch at n = 10^4: a shuffled permutation of 1..n with one value duplicated in place
of another."""

SEEDS = 3


def generate(rng):
    n = 10**4
    nums = list(range(1, n + 1))
    missing = rng.choice([1, n, rng.randint(1, n)])
    dup = rng.randint(1, n)
    while dup == missing:
        dup = rng.randint(1, n)
    nums[missing - 1] = dup
    if rng.random() < 0.7:
        rng.shuffle(nums)
    return {"nums": nums}
