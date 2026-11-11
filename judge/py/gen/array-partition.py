"""Array Partition at the maximum 2 * 10^4 values, reverse sorted with duplicates, so a
quadratic sort such as insertion sort shifts every value past every smaller one."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    nums = sorted((rng.randint(-(10**4), 10**4) for _ in range(N)), reverse=True)
    return {"nums": nums}
