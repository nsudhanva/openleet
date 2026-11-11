"""Shortest Subarray With OR at Least K II at n = 3 * 10^4: k needs bits 28 and 29, which appear
only in the first and last quarters, so extending every start until its OR reaches k scans ~n /
2."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    nums = [rng.randrange(1 << 28) for _ in range(N)]
    q = N // 4
    for _ in range(5):
        nums[rng.randrange(q)] |= 1 << 29
        nums[N - 1 - rng.randrange(q)] |= 1 << 28
    k = (1 << 29) | (1 << 28)
    if rng.random() < 0.5:
        k |= rng.randrange(1 << 20)
    return {"nums": nums, "k": k}
