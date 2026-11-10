"""Assign Cookies at 3 * 10^4 children and cookies with values up to 2^31 - 1: random, or most
cookies just too small so a greedy without sorting scans everything."""

SEEDS = 2
N = 3 * 10**4
TOP = 2**31 - 1


def generate(rng):
    if rng.random() < 0.5:
        g = [rng.randint(1, TOP) for _ in range(N)]
        s = [rng.randint(1, TOP) for _ in range(N)]
    else:
        g = [rng.randint(10**6, TOP) for _ in range(N)]
        s = [rng.randint(1, 10**6) for _ in range(N - 100)] + [TOP] * 100
        rng.shuffle(s)
    return {"g": g, "s": s}
