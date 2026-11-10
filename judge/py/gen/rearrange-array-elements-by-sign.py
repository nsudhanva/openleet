"""Rearrange by Sign at n = 2 * 10^5: all positives first then all negatives, the worst order
for in-place shifting."""

SEEDS = 2
N = 2 * 10**5


def generate(rng):
    pos = [rng.randint(1, 10**5) for _ in range(N // 2)]
    neg = [-rng.randint(1, 10**5) for _ in range(N // 2)]
    if rng.random() < 0.5:
        nums = pos + neg
    else:
        nums = pos + neg
        rng.shuffle(nums)
    return {"nums": nums}
