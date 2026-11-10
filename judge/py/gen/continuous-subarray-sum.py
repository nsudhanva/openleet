"""Continuous Subarray Sum at n = 10^5 with sum below 2^31: all ones with k > n (answer false
after checking every subarray), or random small values with a large k."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        nums = [1] * N
        k = rng.randint(N + 1, 2**31 - 1)
    else:
        nums = [rng.randint(0, 20000) for _ in range(N)]
        k = rng.randint(10**9, 2**31 - 1)
    return {"nums": nums, "k": k}
