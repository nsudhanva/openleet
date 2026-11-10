"""Array Nesting at n = 10^5: one permutation that is a single 10^5-long cycle (so restarting
the walk from every index is quadratic), or a random permutation."""

SEEDS = 2
N = 10**5


def generate(rng):
    nums = list(range(N))
    if rng.random() < 0.5:
        for i in range(N - 1, 0, -1):  # Sattolo: a uniformly random single cycle
            j = rng.randrange(i)
            nums[i], nums[j] = nums[j], nums[i]
    else:
        rng.shuffle(nums)
    return {"nums": nums}
