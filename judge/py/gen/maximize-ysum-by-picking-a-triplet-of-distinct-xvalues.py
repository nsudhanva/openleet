"""Maximize Y-Sum by Picking a Triplet of Distinct X-Values at n = 5 * 10^4: either x and y
uniform over [1, 10^6] (nearly every x distinct), or nearly every x one of two values with a
single third x of the smallest y, or a few low-y ones."""

from _shapes import pick_shape

SEEDS = 3
N = 5 * 10**4
LIMIT = 10**6


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        x = [rng.randint(1, LIMIT) for _ in range(N)]
        y = [rng.randint(1, LIMIT) for _ in range(N)]
        return {"x": x, "y": y}
    a, b, c = rng.sample(range(1, LIMIT + 1), 3)
    x = [rng.choice((a, b)) for _ in range(N)]
    y = [rng.randint(LIMIT // 2, LIMIT) for _ in range(N)]
    if shape == 1:
        i = rng.randrange(N)
        x[i], y[i] = c, 1
    else:
        for i in rng.sample(range(N), 5):
            x[i], y[i] = c, rng.randint(1, 10)
    return {"x": x, "y": y}
