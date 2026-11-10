"""Find All Numbers Disappeared at n = 10^5: many missing values (heavy repeats), or a
permutation with a single value missing."""

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(1, N) for _ in range(N)]
    else:
        nums = list(range(1, N + 1))
        nums[rng.randrange(N)] = rng.randint(1, N)
        rng.shuffle(nums)
    return {"nums": nums}
