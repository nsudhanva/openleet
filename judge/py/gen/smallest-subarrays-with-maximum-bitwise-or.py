"""Smallest Subarrays With Maximum Bitwise OR at n = 2 * 10^4, the high bits appearing only in the
last few elements, so extending each start until its OR stops growing scans ~n / 2 elements."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    low = rng.choice([10, 20])
    nums = [rng.randrange(1 << low) for _ in range(N)]
    for bit in range(low, 29):
        nums[N - 1 - rng.randrange(20)] |= 1 << bit
    return {"nums": nums}
