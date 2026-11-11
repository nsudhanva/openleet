"""Max Value of Equation at 2 * 10^4 random points with k covering every pair, or 4 * 10^4 points
whose y - x falls along the line with k half the x range, so the window's best point expires every
step: checking every pair, or rescanning the window when its best leaves, is >= 2 * 10^8 steps."""

from _shapes import pick_shape

SEEDS = 3
N = (2 * 10**4, 4 * 10**4)
LIMIT = 10**8


def generate(rng):
    if pick_shape(rng) == 0:
        xs = sorted(rng.sample(range(-LIMIT, LIMIT + 1), N[0]))
        points = [[x, rng.randint(-LIMIT, LIMIT)] for x in xs]
        return {"points": points, "k": rng.randint(xs[-1] - xs[0], 2 * LIMIT)}
    xs = sorted(rng.sample(range(-LIMIT, LIMIT + 1), N[1]))
    points = [[x, -x // 2 + rng.randint(-1000, 1000)] for x in xs]
    return {"points": points, "k": (xs[-1] - xs[0]) // 2}
