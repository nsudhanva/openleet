"""Projection Area at the maximum 50 x 50 grid with heights up to 50 and some empty cells."""

SEEDS = 2


def generate(rng):
    zero = rng.choice([0.0, 0.3])
    grid = [
        [0 if rng.random() < zero else rng.randint(1, 50) for _ in range(50)] for _ in range(50)
    ]
    return {"grid": grid}
