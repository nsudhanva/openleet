"""Plus One at the maximum 100 digits, all nines so the carry ripples through every digit."""

SEEDS = 2


def generate(rng):
    if rng.random() < 0.5:
        digits = [9] * 100
    else:
        digits = [rng.randint(1, 9)] + [rng.randint(0, 9) for _ in range(90)] + [9] * 9
    return {"digits": digits}
