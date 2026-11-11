"""Make Lexicographically Smallest Array at n = 3 * 10^4 whose sorted values step by at most limit,
shuffled, so all of them form one swap group and linking every pair, or taking each position's
minimum out of its group one at a time, is ~4.5 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4
LIMIT = (10**4, 3 * 10**4)


def generate(rng):
    limit = rng.randint(*LIMIT)
    value = rng.randint(1, 10**6)
    nums = []
    for _ in range(N):
        nums.append(value)
        value += rng.randint(0, limit)
    rng.shuffle(nums)
    return {"nums": nums, "limit": limit}
