"""atoi at the maximum length of 200: leading spaces, a sign, leading zeros and a long digit
run that overflows (or just fits), followed by junk."""

from string import ascii_letters

from _shapes import pick_shape, random_string

SEEDS = 3
N = 200


def generate(rng):
    s = " " * rng.randint(0, 40) + rng.choice(["", "+", "-"]) + "0" * rng.randint(0, 60)
    shape = pick_shape(rng)
    if shape == 0:
        digits = str(rng.randint(1, 9)) + random_string(rng, "0123456789", 80)
    elif shape == 1:
        digits = str(rng.choice([2147483647, 2147483648, 2147483646, 2147483649]))
    else:
        digits = str(rng.randint(0, 2**31 - 1))
    s += digits
    junk = ascii_letters + "0123456789 +-."
    while len(s) < N:
        s += rng.choice(junk)
    return {"s": s[:N]}
