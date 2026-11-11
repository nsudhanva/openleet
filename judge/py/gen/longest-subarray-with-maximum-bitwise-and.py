"""Longest Subarray With Maximum Bitwise AND at n = 5 * 10^4, all the maximum value except one to
three smaller ones, so extending or ANDing every subarray costs ~10^9 steps."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    top = rng.randint(5 * 10**5, 10**6)
    nums = [top] * N
    for i in rng.sample(range(N), rng.randint(1, 3)):
        nums[i] = rng.randint(1, top - 1)
    return {"nums": nums}
