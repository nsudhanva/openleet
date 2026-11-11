"""Squirrel Simulation with 5,000 nuts on a 100 by 100 garden, so trying each nut first and
summing every trip again is ~2.5 * 10^7 distance terms."""

SEEDS = 2
H = W = 100
NUTS = 5000


def generate(rng):
    def cell():
        return [rng.randint(0, H), rng.randint(0, W)]

    return {
        "height": H,
        "width": W,
        "tree": cell(),
        "squirrel": cell(),
        "nuts": [cell() for _ in range(NUTS)],
    }
