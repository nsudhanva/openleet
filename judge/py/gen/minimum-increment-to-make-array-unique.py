"""Minimum Increment to Make Array Unique at n = 10^5: all values equal (answer ~5 * 10^9,
so incrementing one step at a time is hopeless) or random in [0, 10^5]."""

SEEDS = 3
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        v = rng.choice((0, 10**5, rng.randint(0, 10**5)))
        return {"nums": [v] * N}
    return {"nums": [rng.randint(0, 10**5) for _ in range(N)]}
