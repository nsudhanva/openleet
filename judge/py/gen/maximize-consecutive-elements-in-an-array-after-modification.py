"""Maximize Consecutive Elements in an Array After Modification at n = 3 * 10^4: values climb by
steps of 0 or 1, so one run spans them all and growing a run from every possible start is
~3 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4
TOP = 10**6


def generate(rng):
    v = rng.randint(1, TOP - N)
    nums = []
    for _ in range(N):
        nums.append(v)
        v += rng.choices((0, 1), (1, 4))[0]
    rng.shuffle(nums)
    return {"nums": nums}
