"""Sliding Window Median at n = 10^5 with k around n / 2 (even and odd) and extreme 32-bit
values whose pairwise sums overflow, so sorting each window is far too slow."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.getrandbits(6) % 3
    if shape == 0:
        nums = [rng.randint(-(2**31), 2**31 - 1) for _ in range(N)]
    elif shape == 1:
        nums = [rng.choice([2**31 - 1, 2**31 - 2, -(2**31), -(2**31) + 1]) for _ in range(N)]
    else:
        nums = [rng.randint(0, 5) for _ in range(N)]
    k = rng.choice([N // 2, N // 2 + 1, rng.randint(1, N), N])
    return {"nums": nums, "k": k}
