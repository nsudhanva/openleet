"""atoi at the maximum length of 200: leading spaces, a sign, leading zeros and a long digit
run that overflows (or just fits), followed by junk."""

from _shapes import pick_shape

SEEDS = 3
N = 200


def generate(rng):
    s = " " * rng.randint(0, 40) + rng.choice(["", "+", "-"]) + "0" * rng.randint(0, 60)
    shape = pick_shape(rng)
    if shape == 0:
        digits = str(rng.randint(1, 9)) + "".join(rng.choice("0123456789") for _ in range(80))
    elif shape == 1:
        digits = str(rng.choice([2147483647, 2147483648, 2147483646, 2147483649]))
    else:
        digits = str(rng.randint(0, 2**31 - 1))
    s += digits
    junk = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 +-."
    while len(s) < N:
        s += rng.choice(junk)
    return {"s": s[:N]}
