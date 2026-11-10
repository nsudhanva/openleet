"""Non-decreasing Array at n = 10^4: a sorted array with zero, one, or two violations placed
near the end, including the case that needs nums[i] lowered vs nums[i+1] raised."""

SEEDS = 3
N = 10**4


def generate(rng):
    nums = sorted(rng.randint(-(10**5), 10**5) for _ in range(N))
    for _ in range(rng.choice((0, 1, 1, 2))):
        i = rng.randint(N - 500, N - 1)
        nums[i] = rng.randint(-(10**5), 10**5)
    return {"nums": nums}
