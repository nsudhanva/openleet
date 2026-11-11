"""Count Number of Special Subsequences at n = 2 * 10^4 values in 0..2, loosely sorted so the
answer is huge, so a DP summing over every earlier index costs ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    nums = sorted(rng.randint(0, 2) for _ in range(N))
    for _ in range(N // 10):
        i, j = rng.randrange(N), rng.randrange(N)
        nums[i], nums[j] = nums[j], nums[i]
    return {"nums": nums}
