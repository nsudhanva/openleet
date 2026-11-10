"""Longest Turbulent Subarray at n = 4 * 10^4: a perfect zigzag (answer n), or small random
values with frequent equal neighbors."""

SEEDS = 2
N = 4 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        arr = [rng.randint(0, 10**8) if i % 2 else rng.randint(10**8 + 1, 10**9) for i in range(N)]
    else:
        arr = [rng.randint(0, 3) for _ in range(N)]
    return {"arr": arr}
