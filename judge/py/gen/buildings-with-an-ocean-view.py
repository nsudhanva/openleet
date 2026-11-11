"""Buildings With an Ocean View at n = 3 * 10^4, heights falling from left to right with a few equal
neighbours, so nearly every building sees the ocean and a scan of everything to its right is
quadratic."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    heights, h = [], 10**9
    for _ in range(N):
        heights.append(h)
        h -= 0 if rng.random() < 0.01 else rng.randint(1, 9000)
    return {"heights": heights}
