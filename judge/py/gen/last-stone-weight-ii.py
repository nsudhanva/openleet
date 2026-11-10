"""Last Stone Weight II with 30 stones, where enumerating all 2^30 sign choices times out."""

SEEDS = 2


def generate(rng):
    return {"stones": [rng.randint(1, 100) for _ in range(30)]}
