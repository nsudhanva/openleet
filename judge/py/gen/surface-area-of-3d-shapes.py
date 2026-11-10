"""Surface Area of 3D Shapes on the maximum 50 x 50 grid with towers up to 50, random or with
many empty cells."""

SEEDS = 2
N = 50


def generate(rng):
    zero = rng.choice([0.0, 0.4])
    grid = [[0 if rng.random() < zero else rng.randint(0, 50) for _ in range(N)] for _ in range(N)]
    return {"grid": grid}
