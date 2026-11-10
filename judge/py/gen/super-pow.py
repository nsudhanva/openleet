"""Super Pow with a near 2^31 and a 2000-digit exponent, where converting b to an int and
calling a slow power, or skipping the modulo, is punished."""

from _shapes import pick_shape

SEEDS = 3
DIGITS = 2000


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        a = 2**31 - 1
    elif shape == 1:
        a = 1337 * rng.randint(1, 10**6)  # a multiple of the modulus
    else:
        a = rng.randint(1, 2**31 - 1)
    b = [rng.randint(1, 9)] + [rng.randint(0, 9) for _ in range(DIGITS - 1)]
    return {"a": a, "b": b}
