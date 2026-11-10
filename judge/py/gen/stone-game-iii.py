"""Stone Game III at n = 5 * 10^4 with values in [-1000, 1000] (deep recursion for top-down
DP), random or all negative."""

from _shapes import pick_shape

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        vals = [rng.randint(-1000, 1000) for _ in range(N)]
    elif shape == 1:
        vals = [rng.randint(-1000, -1) for _ in range(N)]
    else:
        vals = [rng.choice([-1000, 1000, 0]) for _ in range(N)]
    return {"stoneValue": vals}
