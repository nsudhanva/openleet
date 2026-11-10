"""Partition List at the maximum 200 nodes with x in the middle of the value range."""

SEEDS = 2


def generate(rng):
    head = [rng.randint(-100, 100) for _ in range(200)]
    return {"head": head, "x": rng.randint(-50, 50)}
