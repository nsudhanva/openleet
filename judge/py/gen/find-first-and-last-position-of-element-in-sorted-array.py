"""Search Range on 10^5 sorted values with long runs of duplicates; the target is a long run, a
single value at an edge, or absent."""

SEEDS = 3
N = 10**5


def generate(rng):
    distinct = rng.choice([5, 300, 50_000])
    vals = sorted(rng.sample(range(-(10**9), 10**9 + 1), distinct))
    nums = sorted(rng.choice(vals) for _ in range(N))
    mode = rng.randrange(3)
    if mode == 0:
        target = nums[N // 2]
    elif mode == 1:
        target = nums[-1]
    else:
        target = nums[rng.randrange(N)] + 1
        if target > 10**9:
            target = -(10**9)
    return {"nums": nums, "target": target}
