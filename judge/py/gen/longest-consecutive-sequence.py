"""Longest Consecutive Sequence at n = 10^5: one long shuffled run with duplicates (sorting is
fine, but starting a walk from every element is quadratic), or random wide values."""

SEEDS = 2
N = 10**5
LIMIT = 10**9


def generate(rng):
    if rng.random() < 0.5:
        start = rng.randint(-LIMIT, LIMIT - N)
        nums = [start + i for i in range(N - 1000)]
        nums += [rng.choice(nums) for _ in range(1000)]
        rng.shuffle(nums)
    else:
        nums = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    return {"nums": nums}
