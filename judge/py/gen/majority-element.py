"""Majority Element at n = 5 * 10^4 with the majority holding just over half, placed in a
block at the end or scattered."""

SEEDS = 2
N = 5 * 10**4
LIMIT = 10**9


def generate(rng):
    major = rng.randint(-LIMIT, LIMIT)
    count = N // 2 + 1
    others = []
    while len(others) < N - count:
        v = rng.randint(-LIMIT, LIMIT)
        if v != major:
            others.append(v)
    if rng.random() < 0.5:
        nums = others + [major] * count
    else:
        nums = others + [major] * count
        rng.shuffle(nums)
    return {"nums": nums}
