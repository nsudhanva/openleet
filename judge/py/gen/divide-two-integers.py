"""Divide Two Integers with a huge dividend and a tiny divisor (repeated subtraction needs
~2^31 steps), including the -2^31 / -1 overflow case."""

SEEDS = 3


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        return {"dividend": -(2**31), "divisor": rng.choice([-1, 1, 2, -3])}
    dividend = rng.choice([2**31 - 1, -(2**31)]) if shape == 1 else rng.randint(10**9, 2**31 - 1)
    divisor = rng.randint(1, 7) * rng.choice([1, -1])
    return {"dividend": dividend, "divisor": divisor}
