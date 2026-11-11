"""Tuple with Same Product at n = 600 distinct values, half of them 7-smooth so many products
repeat, so pairing each pair with every third value is ~10^8 steps."""

SEEDS = 2
N = 600
LIMIT = 10**4


def generate(rng):
    smooth = [v for v in range(1, LIMIT + 1) if _smooth(v)]
    picked = set(rng.sample(smooth, N // 2))
    rest = [v for v in range(1, LIMIT + 1) if v not in picked]
    nums = [*picked, *rng.sample(rest, N - len(picked))]
    rng.shuffle(nums)
    return {"nums": nums}


def _smooth(v):
    for p in (2, 3, 5, 7):
        while v % p == 0:
            v //= p
    return v == 1
