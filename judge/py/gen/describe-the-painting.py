"""Describe the Painting with 2 * 10^4 long, heavily overlapping segments over [1, 10^5], so
painting unit by unit or summing the covering segments for each piece costs ~10^9 steps."""

SEEDS = 2
N = 2 * 10**4
TOP = 10**5


def generate(rng):
    colors = rng.sample(range(1, 10**9 + 1), N)
    segments = []
    for color in colors:
        a, b = rng.randint(1, TOP), rng.randint(1, TOP)
        while a == b:
            b = rng.randint(1, TOP)
        segments.append([min(a, b), max(a, b), color])
    return {"segments": segments}
