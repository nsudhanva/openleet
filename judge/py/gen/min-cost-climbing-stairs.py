"""Min Cost Climbing Stairs at the maximum 1000 steps, costs in [0, 999]."""

SEEDS = 2


def generate(rng):
    return {"cost": [rng.randint(0, 999) for _ in range(1000)]}
