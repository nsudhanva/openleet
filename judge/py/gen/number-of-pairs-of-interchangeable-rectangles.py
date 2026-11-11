"""Number of Pairs of Interchangeable Rectangles at 2 * 10^4 rectangles drawn from a few dozen
ratios, so comparing every pair costs 2 * 10^8 checks."""

from math import gcd

SEEDS = 2
N = 2 * 10**4
TOP = 10**5


def generate(rng):
    ratios = []
    while len(ratios) < 40:
        p, q = rng.randint(1, 30), rng.randint(1, 30)
        if gcd(p, q) == 1 and (p, q) not in ratios:
            ratios.append((p, q))
    rectangles = []
    for _ in range(N):
        if rng.random() < 0.1:
            rectangles.append([rng.randint(1, TOP), rng.randint(1, TOP)])
        else:
            p, q = rng.choice(ratios)
            k = rng.randint(1, TOP // max(p, q))
            rectangles.append([p * k, q * k])
    return {"rectangles": rectangles}
