"""Minimum Area Rectangle with 500 unique points on a few shared x and y lines, so many
axis-aligned rectangles exist and checking every 4-tuple is hopeless."""

SEEDS = 3
N = 500
TOP = 4 * 10**4


def generate(rng):
    if rng.random() < 0.3:
        cells = rng.sample(range((TOP + 1) ** 2), N)
        return {"points": [[c // (TOP + 1), c % (TOP + 1)] for c in cells]}
    xs = rng.sample(range(TOP + 1), rng.randint(23, 40))
    ys = rng.sample(range(TOP + 1), rng.randint(23, 40))
    grid = [[x, y] for x in xs for y in ys]
    return {"points": rng.sample(grid, N)}
