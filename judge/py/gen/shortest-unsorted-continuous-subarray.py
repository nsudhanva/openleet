"""Shortest Unsorted Subarray at n = 10^4: sorted except one swap near the ends, random, or
fully sorted with duplicates."""

SEEDS = 3
N = 10**4


def generate(rng):
    shape = rng.getrandbits(6) % 3
    nums = sorted(rng.randint(-(10**5), 10**5) for _ in range(N))
    if shape == 0:
        i, j = rng.randint(0, 5), rng.randint(N - 6, N - 1)
        nums[i], nums[j] = nums[j], nums[i]
    elif shape == 1:
        rng.shuffle(nums)
    else:
        nums = sorted(rng.randint(-3, 3) for _ in range(N))
    return {"nums": nums}
