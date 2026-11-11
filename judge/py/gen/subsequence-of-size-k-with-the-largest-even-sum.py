"""Subsequence of Size K With the Largest Even Sum at n = 2 * 10^4 and k = n / 2 with an odd
top-k sum, so trying every swap of a chosen and an unchosen number is ~10^8 pairs."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**5


def generate(rng):
    k = N // 2
    while True:
        nums = [rng.randint(0, LIMIT) for _ in range(N)]
        if sum(sorted(nums)[-k:]) % 2:
            return {"nums": nums, "k": k}
