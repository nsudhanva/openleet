"""Bag of Tokens at the maximum 1000 tokens with values below 10^4 and varied starting power
(including below every token)."""

SEEDS = 3


def generate(rng):
    tokens = [rng.randint(0, 10**4 - 1) for _ in range(1000)]
    power = rng.choice([0, rng.randint(0, 10**4 - 1), min(tokens) + 1])
    return {"tokens": tokens, "power": min(power, 10**4 - 1)}
