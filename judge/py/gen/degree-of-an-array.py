"""Degree of an Array at n = 5 * 10^4: values drawn from a small pool (many ties for the
degree), or all distinct except one repeated value at both ends."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        pool = rng.sample(range(50000), rng.randint(100, 1000))
        nums = [rng.choice(pool) for _ in range(N)]
    else:
        nums = rng.sample(range(50000), N)
        nums[-1] = nums[0]
    return {"nums": nums}
