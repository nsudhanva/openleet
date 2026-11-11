"""Maximize Distance to Closest Person on the maximum 2 * 10^4 seats: one empty run of over half
the row (at the start, the end or inside) beside seats half taken, so scanning out from each
empty seat and measuring each empty seat against every person are both ~10^8 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    gap = rng.randint(N // 2, 3 * N // 5)
    rest = [1 if rng.random() < 0.5 else 0 for _ in range(N - gap)]
    rest[0] = rest[-1] = 1
    if shape == 0:
        seats = [0] * gap + rest
    elif shape == 1:
        seats = rest + [0] * gap
    else:
        cut = rng.randrange(1, len(rest) - 1)
        seats = rest[:cut] + [0] * gap + rest[cut:]
    return {"seats": seats}
