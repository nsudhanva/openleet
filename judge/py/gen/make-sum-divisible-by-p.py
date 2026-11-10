"""Make Sum Divisible by P at n = 10^5 with values up to 10^9 and varied p, where checking
every subarray is quadratic."""

SEEDS = 3
N = 10**5


def generate(rng):
    nums = [rng.randint(1, 10**9) for _ in range(N)]
    p = rng.choice([1, rng.randint(2, 100), rng.randint(10**5, 10**9), 10**9])
    return {"nums": nums, "p": p}
