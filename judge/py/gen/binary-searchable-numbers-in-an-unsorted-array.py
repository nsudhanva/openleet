"""Binary Searchable Numbers at n = 5 * 10^4 distinct values: sorted with a few adjacent swaps,
so almost every number is searchable and checking each against everything on both sides is
~2.5 * 10^9 steps."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    nums = sorted(rng.sample(range(-(10**5), 10**5 + 1), N))
    for _ in range(rng.choice([3, 30])):
        i = rng.randrange(N - 1)
        nums[i], nums[i + 1] = nums[i + 1], nums[i]
    return {"nums": nums}
