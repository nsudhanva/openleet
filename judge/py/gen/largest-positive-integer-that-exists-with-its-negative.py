"""Largest K With Its Negative on 1000 nonzero values in [-1000, 1000]: random values, or
values whose negatives are almost all missing."""

SEEDS = 2
N = 1000


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.choice([-1, 1]) * rng.randint(1, 1000) for _ in range(N)]
    else:
        nums = [rng.randint(1, 1000) for _ in range(N - 1)]
        nums.append(-rng.choice(nums))
        rng.shuffle(nums)
    return {"nums": nums}
