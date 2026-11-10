"""Jump Game IX at n = 10^5 with values up to 10^9: random, increasing (no jumps help), or
decreasing (everything connects)."""

SEEDS = 3
N = 10**5


def generate(rng):
    nums = [rng.randint(1, 10**9) for _ in range(N)]
    shape = rng.randrange(3)
    if shape == 1:
        nums.sort()
    elif shape == 2:
        nums.sort(reverse=True)
        nums[0], nums[-1] = nums[-1], nums[0]
    return {"nums": nums}
