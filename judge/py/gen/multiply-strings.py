"""Multiply Strings at 200 x 200 digits with no leading zeros (one seed multiplies by 0)."""

SEEDS = 3


def number(rng, length):
    return str(rng.randint(1, 9)) + "".join(rng.choice("0123456789") for _ in range(length - 1))


def generate(rng):
    a = number(rng, 200)
    b = rng.choice((number(rng, 200), "0", number(rng, rng.randint(1, 200))))
    return {"num1": a, "num2": b}
