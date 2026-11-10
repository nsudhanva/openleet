"""Image Smoother on the maximum 200 x 200 image (or a single row) with values in [0, 255]."""

SEEDS = 3


def generate(rng):
    m, n = rng.choice([(200, 200), (1, 200), (200, 1)])
    return {"img": [[rng.randint(0, 255) for _ in range(n)] for _ in range(m)]}
