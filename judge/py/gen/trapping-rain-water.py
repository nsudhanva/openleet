"""Trapping Rain Water at n = 2 * 10^4: a deep valley between two tall walls, a sawtooth, or
random heights, punishing the per-bar left/right max scan."""

SEEDS = 3
N = 2 * 10**4
TOP = 10**5


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        height = [TOP] + [rng.randint(0, 10) for _ in range(N - 2)] + [TOP - 1]
    elif shape == 1:
        height = [(i % 100) * 1000 for i in range(N)]
    else:
        height = [rng.randint(0, TOP) for _ in range(N)]
    return {"height": height}
