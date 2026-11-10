"""Transpose Matrix at m * n near 10^5: a tall 1000 x 100, a wide 100 x 1000, or square."""

from _shapes import pick_shape

SEEDS = 3
LIM = 10**9


def generate(rng):
    m, n = [(1000, 100), (100, 1000), (316, 316)][pick_shape(rng)]
    return {"matrix": [[rng.randint(-LIM, LIM) for _ in range(n)] for _ in range(m)]}
