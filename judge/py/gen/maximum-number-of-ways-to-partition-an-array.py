"""Maximum Number of Ways to Partition an Array with 2 * 10^4 values in (a, -a) pairs, so the
prefix sum returns to 0 after every pair and recounting the pivots after each change is
quadratic."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    nums = []
    for _ in range(N // 2):
        a = rng.randint(1, 10**5)
        nums += [a, -a] if rng.random() < 0.5 else [-a, a]
    return {"nums": nums, "k": rng.randint(-(10**5), 10**5)}
