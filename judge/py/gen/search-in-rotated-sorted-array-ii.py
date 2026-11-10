"""Search in Rotated Sorted Array II at n = 5000 with heavy duplicates (almost all one value,
the worst case for binary search), or a random sorted array with repeats rotated."""

SEEDS = 3


def generate(rng):
    n = 5000
    if rng.random() < 0.6:
        base = rng.randint(-(10**4), 10**4 - 1)
        values = [base] * (n - 1) + [base + 1]
        target = rng.choice([base + 1, base - 1 if base > -(10**4) else base + 1])
    else:
        values = sorted(rng.randint(-100, 100) for _ in range(n))
        target = rng.randint(-150, 150)
    k = rng.randrange(n)
    return {"nums": values[k:] + values[:k], "target": target}
