"""Daily Temperatures at n = 10^5: long flat or slowly falling stretches where a forward scan
for a warmer day runs to the end, or random values."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        t = [rng.randint(30, 100) for _ in range(N)]
    elif shape == 1:
        v = rng.randint(30, 99)
        t = [v] * (N - 1) + [v + 1]
    else:
        t = sorted((rng.randint(30, 100) for _ in range(N)), reverse=True)
    return {"temperatures": t}
