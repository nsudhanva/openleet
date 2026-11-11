"""Minimum Cost to Equalize Array at n = 10^4 with values up to 10^4 and one value of 1, so
pricing every target in [max, 2 max) with a pass over the array is 10^8 steps."""

SEEDS = 2
N = 10**4
LIMIT = 10**4
COST = 10**6


def generate(rng):
    nums = [1] + [rng.randint(LIMIT // 2, LIMIT) for _ in range(N - 1)]
    rng.shuffle(nums)
    cost1 = rng.randint(COST // 2, COST)
    cost2 = rng.randint(1, 2 * cost1 - 1)
    return {"nums": nums, "cost1": cost1, "cost2": cost2}
