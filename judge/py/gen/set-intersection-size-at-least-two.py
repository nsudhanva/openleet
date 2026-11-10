"""Set Intersection Size At Least Two with 3000 intervals in [0, 10^8]: random wide intervals,
heavily nested ones, or many short touching ones."""

from _shapes import pick_shape

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    out = []
    for _ in range(3000):
        if shape == 0:
            a = rng.randint(0, 10**8 - 1)
            b = rng.randint(a + 1, 10**8)
        elif shape == 1:
            # Nested around the middle.
            a = rng.randint(0, 5 * 10**7 - 1)
            b = rng.randint(5 * 10**7 + 1, 10**8)
        else:
            a = rng.randint(0, 10**4)
            b = a + rng.randint(1, 3)
        out.append([a, b])
    return {"intervals": out}
