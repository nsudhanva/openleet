"""Count Good Numbers with n near 10^15, which needs fast modular exponentiation."""

SEEDS = 3


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        n = 10**15
    elif shape == 1:
        n = 10**15 - 1
    else:
        n = rng.randint(10**14, 10**15)
    return {"n": n}
