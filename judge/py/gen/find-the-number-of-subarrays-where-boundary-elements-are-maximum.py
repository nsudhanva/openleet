"""Find the Number of Subarrays Where Boundary Elements Are Maximum at n = 10^4, either a
non-increasing run of 2-4 values or the maximum at every other index, so extending each start
until a larger value, or pairing up equal values, is quadratic."""

SEEDS = 2
N = 10**4


def generate(rng):
    if rng.random() < 0.5:
        levels = [rng.randint(1, 10**9) for _ in range(rng.randint(2, 4))]
        return {"nums": sorted((rng.choice(levels) for _ in range(N)), reverse=True)}
    top = rng.randint(10**8, 10**9)
    return {"nums": [top if i % 2 == 0 else rng.randint(1, top - 1) for i in range(N)]}
