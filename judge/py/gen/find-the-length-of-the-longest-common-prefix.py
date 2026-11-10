"""Longest Common Prefix between two arrays of 5 * 10^4 integers up to 10^8, built from shared
long prefixes so the answer is large."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        arr1 = [rng.randint(1, 10**8) for _ in range(N)]
        arr2 = [rng.randint(1, 10**8) for _ in range(N)]
    else:
        roots = [rng.randint(10**3, 10**4 - 1) for _ in range(50)]

        def make():
            r = rng.choice(roots)
            digits = rng.randint(0, 4)
            return r * 10**digits + rng.randrange(10**digits)

        arr1 = [make() for _ in range(N)]
        arr2 = [make() for _ in range(N)]
    return {"arr1": arr1, "arr2": arr2}
