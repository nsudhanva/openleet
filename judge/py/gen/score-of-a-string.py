"""Score of a String on 100 random lowercase letters."""

SEEDS = 2


def generate(rng):
    return {"s": "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(100))}
