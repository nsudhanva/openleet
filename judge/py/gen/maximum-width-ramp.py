"""Maximum Width Ramp at n = 5 * 10^4: strictly decreasing values (answer 0, so brute force
checks every pair) or random values."""

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        return {"nums": list(range(N, 0, -1))}
    return {"nums": [rng.randint(0, N) for _ in range(N)]}
