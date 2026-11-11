"""Sum of Beauty in the Array at n = 10^5: a rising run with a few adjacent swaps, so almost every
index has beauty 2 and checking all of the left and right side for each one is ~10^10 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    nums = list(range(1, N + 1))
    for _ in range(rng.randint(20, 200)):
        i = rng.randrange(N - 1)
        nums[i], nums[i + 1] = nums[i + 1], nums[i]
    return {"nums": nums}
